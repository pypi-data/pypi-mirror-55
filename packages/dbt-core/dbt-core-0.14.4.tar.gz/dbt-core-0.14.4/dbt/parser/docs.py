import dbt.exceptions
from dbt.node_types import NodeType
from dbt.parser.base import BaseParser
from dbt.contracts.graph.unparsed import UnparsedDocumentationFile
from dbt.contracts.graph.parsed import ParsedDocumentation
from dbt.clients.jinja import extract_toplevel_blocks, get_template
from dbt.clients import system

import jinja2.runtime
import os


class DocumentationParser(BaseParser):
    @classmethod
    def load_file(cls, package_name, root_dir, relative_dirs):
        """Load and parse documentation in a list of projects. Returns a list
        of ParsedNodes.
        """
        extension = "[!.#~]*.md"

        file_matches = system.find_matching(root_dir, relative_dirs, extension)

        for file_match in file_matches:
            file_contents = system.load_file_contents(
                file_match.get('absolute_path'),
                strip=False)

            parts = dbt.utils.split_path(file_match.get('relative_path', ''))
            name, _ = os.path.splitext(parts[-1])

            path = file_match.get('relative_path')
            original_file_path = os.path.join(
                file_match.get('searched_path'),
                path)

            yield UnparsedDocumentationFile(
                root_path=root_dir,
                resource_type=NodeType.Documentation,
                path=path,
                original_file_path=original_file_path,
                package_name=package_name,
                file_contents=file_contents
            )

    def parse(self, docfile):
        try:
            blocks = extract_toplevel_blocks(
                docfile.file_contents,
                allowed_blocks={'docs'},
                collect_raw_data=False
            )
        except dbt.exceptions.CompilationException as exc:
            if exc.node is None:
                exc.node = docfile
            raise

        for block in blocks:
            try:
                template = get_template(block.full_block, {})
            except dbt.exceptions.CompilationException as e:
                e.node = docfile
                raise
            # in python 3.x this can just be "yield from" isntead of a loop
            for d in self._parse_template_docs(template, docfile):
                yield d

    def _parse_template_docs(self, template, docfile):
        for key, item in template.module.__dict__.items():
            if type(item) != jinja2.runtime.Macro:
                continue

            if not key.startswith(dbt.utils.DOCS_PREFIX):
                continue

            name = key.replace(dbt.utils.DOCS_PREFIX, '')

            # because docs are in their own graph namespace, node type doesn't
            # need to be part of the unique ID.
            unique_id = '{}.{}'.format(docfile.package_name, name)

            merged = dbt.utils.deep_merge(
                docfile.serialize(),
                {
                    'name': name,
                    'unique_id': unique_id,
                    'block_contents': item().strip(),
                }
            )
            yield ParsedDocumentation(**merged)

    def load_and_parse(self, package_name, root_dir, relative_dirs):
        to_return = {}
        for docfile in self.load_file(package_name, root_dir, relative_dirs):
            for parsed in self.parse(docfile):
                if parsed.unique_id in to_return:
                    dbt.exceptions.raise_duplicate_resource_name(
                        to_return[parsed.unique_id], parsed
                    )
                to_return[parsed.unique_id] = parsed
        return to_return
