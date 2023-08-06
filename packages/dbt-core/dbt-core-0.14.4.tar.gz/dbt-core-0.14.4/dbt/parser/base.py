import os

import dbt.exceptions
import dbt.flags
import dbt.include
import dbt.utils
import dbt.hooks
import dbt.clients.jinja
import dbt.context.parser

from dbt.include.global_project import PROJECT_NAME as GLOBAL_PROJECT_NAME
from dbt.utils import coalesce
from dbt.logger import GLOBAL_LOGGER as logger
from dbt.contracts.graph.parsed import ParsedNode
from dbt.parser.source_config import SourceConfig
from dbt import deprecations


class BaseParser(object):
    def __init__(self, root_project_config, all_projects):
        self.root_project_config = root_project_config
        self.all_projects = all_projects

    @property
    def default_schema(self):
        return getattr(self.root_project_config.credentials, 'schema',
                       'public')

    @property
    def default_database(self):
        return getattr(self.root_project_config.credentials, 'database', 'dbt')

    def load_and_parse(self, *args, **kwargs):
        raise dbt.exceptions.NotImplementedException("Not implemented")

    @classmethod
    def get_path(cls, resource_type, package_name, resource_name):
        """Returns a unique identifier for a resource"""

        return "{}.{}.{}".format(resource_type, package_name, resource_name)

    @classmethod
    def get_fqn(cls, node, package_project_config, extra=[]):
        parts = dbt.utils.split_path(node.path)
        name, _ = os.path.splitext(parts[-1])
        fqn = ([package_project_config.project_name] +
               parts[:-1] +
               extra +
               [name])

        return fqn


class MacrosKnownParser(BaseParser):
    def __init__(self, root_project_config, all_projects, macro_manifest):
        super(MacrosKnownParser, self).__init__(
            root_project_config=root_project_config,
            all_projects=all_projects
        )
        self.macro_manifest = macro_manifest
        self._get_schema_func = None
        self._get_alias_func = None

    def get_schema_func(self):
        """The get_schema function is set by a few different things:
            - if there is a 'generate_schema_name' macro in the root project,
                it will be used.
            - if that does not exist but there is a 'generate_schema_name'
                macro in the 'dbt' internal project, that will be used
            - if neither of those exist (unit tests?), a function that returns
                the 'default schema' as set in the root project's 'credentials'
                is used
        """
        if self._get_schema_func is not None:
            return self._get_schema_func

        get_schema_macro = self.macro_manifest.find_macro_by_name(
            'generate_schema_name',
            self.root_project_config.project_name
        )
        if get_schema_macro is None:
            get_schema_macro = self.macro_manifest.find_macro_by_name(
                'generate_schema_name',
                GLOBAL_PROJECT_NAME
            )
        # this is only true in tests!
        if get_schema_macro is None:
            def get_schema(custom_schema_name=None, node=None):
                return self.default_schema
        else:
            root_context = dbt.context.parser.generate_macro(
                get_schema_macro, self.root_project_config,
                self.macro_manifest
            )
            get_schema = get_schema_macro.generator(root_context)

        self._get_schema_func = get_schema
        return self._get_schema_func

    def get_alias_func(self):
        """The get_alias function is set by a few different things:
            - if there is a 'generate_alias_name' macro in the root project,
                it will be used.
            - if that does not exist but there is a 'generate_alias_name'
                macro in the 'dbt' internal project, that will be used
            - if neither of those exist (unit tests?), a function that returns
                the 'default alias' as set in the model's filename or alias
                configuration.
        """
        if self._get_alias_func is not None:
            return self._get_alias_func

        get_alias_macro = self.macro_manifest.find_macro_by_name(
            'generate_alias_name',
            self.root_project_config.project_name
        )
        if get_alias_macro is None:
            get_alias_macro = self.macro_manifest.find_macro_by_name(
                'generate_alias_name',
                GLOBAL_PROJECT_NAME
            )

        # the generate_alias_name macro might not exist
        if get_alias_macro is None:
            def get_alias(custom_alias_name, node):
                if custom_alias_name is None:
                    return node.name
                else:
                    return custom_alias_name
        else:
            root_context = dbt.context.parser.generate_macro(
                get_alias_macro, self.root_project_config,
                self.macro_manifest
            )
            get_alias = get_alias_macro.generator(root_context)

        self._get_alias_func = get_alias
        return self._get_alias_func

    def _build_intermediate_node_dict(self, config, node_dict, node_path,
                                      package_project_config, tags, fqn,
                                      agate_table, snapshot_config,
                                      column_name):
        """Update the unparsed node dictionary and build the basis for an
        intermediate ParsedNode that will be passed into the renderer
        """
        # because this takes and returns dicts, subclasses can safely override
        # this and mutate its results using super() both before and after.
        if agate_table is not None:
            node_dict['agate_table'] = agate_table

        # Set this temporarily. Not the full config yet (as config() hasn't
        # been called from jinja yet). But the Var() call below needs info
        # about project level configs b/c they might contain refs.
        # TODO: Restructure this?
        config_dict = coalesce(snapshot_config, {})
        config_dict.update(config.config)

        empty = (
            'raw_sql' in node_dict and len(node_dict['raw_sql'].strip()) == 0
        )

        node_dict.update({
            'refs': [],
            'sources': [],
            'depends_on': {
                'nodes': [],
                'macros': [],
            },
            'unique_id': node_path,
            'empty': empty,
            'fqn': fqn,
            'tags': tags,
            'config': config_dict,
            # Set these temporarily so get_rendered() has access to a schema,
            # database, and alias.
            'schema': self.default_schema,
            'database': self.default_database,
            'alias': node_dict.get('name'),
        })

        # if there's a column, it should end up part of the ParsedNode
        if column_name is not None:
            node_dict['column_name'] = column_name

        return node_dict

    def _render_with_context(self, parsed_node, config):
        """Given the parsed node and a SourceConfig to use during parsing,
        render the node's sql wtih macro capture enabled.

        Note: this mutates the config object when config() calls are rendered.
        """
        context = dbt.context.parser.generate(
            parsed_node,
            self.root_project_config,
            self.macro_manifest,
            config)

        dbt.clients.jinja.get_rendered(
            parsed_node.raw_sql, context, parsed_node.to_shallow_dict(),
            capture_macros=True)

    def _update_parsed_node_info(self, parsed_node, config):
        """Given the SourceConfig used for parsing and the parsed node,
        generate and set the true values to use, overriding the temporary parse
        values set in _build_intermediate_parsed_node.
        """
        # Set tags on node provided in config blocks
        model_tags = config.config.get('tags', [])
        parsed_node.tags.extend(model_tags)

        # Overwrite node config
        config_dict = parsed_node.get('config', {})
        config_dict.update(config.config)
        parsed_node.config = config_dict

        # Special macro defined in the global project. Use the root project's
        # definition, not the current package
        schema_override = config.config.get('schema')
        get_schema = self.get_schema_func()
        try:
            schema = get_schema(schema_override, parsed_node)
        except dbt.exceptions.CompilationException as exc:
            too_many_args = (
                "macro 'dbt_macro__generate_schema_name' takes not more than "
                "1 argument(s)"
            )
            if too_many_args not in str(exc):
                raise
            deprecations.warn('generate-schema-name-single-arg')
            schema = get_schema(schema_override)
        parsed_node.schema = schema.strip()

        alias_override = config.config.get('alias')
        get_alias = self.get_alias_func()
        parsed_node.alias = get_alias(alias_override, parsed_node).strip()

        parsed_node.database = config.config.get(
            'database', self.default_database
        ).strip()

        for hook_type in dbt.hooks.ModelHookType.Both:
            parsed_node.config[hook_type] = dbt.hooks.get_hooks(parsed_node,
                                                                hook_type)

    def parse_node(self, node, node_path, package_project_config, tags=None,
                   fqn_extra=None, fqn=None, agate_table=None,
                   snapshot_config=None, column_name=None):
        """Parse a node, given an UnparsedNode and any other required information.

        agate_table should be set if the node came from a seed file.
        snapshot_config should be set if the node is an Snapshot node.
        column_name should be set if the node is a Test node associated with a
        particular column.
        """
        logger.debug("Parsing {}".format(node_path))

        tags = coalesce(tags, [])
        fqn_extra = coalesce(fqn_extra, [])

        if fqn is None:
            fqn = self.get_fqn(node, package_project_config, fqn_extra)

        config = SourceConfig(
            self.root_project_config,
            package_project_config,
            fqn,
            node.resource_type)

        parsed_dict = self._build_intermediate_node_dict(
            config, node.serialize(), node_path, config, tags, fqn,
            agate_table, snapshot_config, column_name
        )
        parsed_node = ParsedNode(**parsed_dict)

        self._render_with_context(parsed_node, config)
        self._update_parsed_node_info(parsed_node, config)

        parsed_node.validate()

        return parsed_node

    def check_block_parsing(self, name, path, contents):
        """Check if we were able to extract toplevel blocks from the given
        contents. Return True if extraction was successful (no exceptions),
        False if it fails.
        """
        if not dbt.flags.TEST_NEW_PARSER:
            return True
        try:
            dbt.clients.jinja.extract_toplevel_blocks(contents)
        except Exception:
            return False
        return True
