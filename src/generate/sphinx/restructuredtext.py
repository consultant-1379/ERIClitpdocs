
import os
import logging
import inspect

from litp.core.model_type import PropertyType
from litp.core.model_type import Property
from litp.core.model_type import View
from litp.core.model_type import Child
from litp.core.model_type import Collection
from litp.core.model_type import Reference
from litp.core.model_type import RefCollection
from litp.core.plugin import Plugin
from litp.core.litp_logging import LitpLogger
from litp.core.validators import PropertyValidator
from litp.core.validators import ItemValidator
from litp.migration.operations.base_operation import BaseOperation
from sphinx.classdiagram import ClassDiagram

log = LitpLogger()

# LIST OF CONTRIBUTED PLUGINS AND EXTENSIONS
CONTRIBUTED_PLUGINS = \
    ['san',
     'userplugin',
     'groupplugin',
     'hyperics',
     'postgresql',
     'versantmanagement',
     'epsjse',
     'zookeeper',
     'modeldeployment',
     'configmanager',
     'mysql',
     'opendj',
     'elasticsearch',
     'dps',
]
CONTRIBUTED_EXTENSIONS = \
    ['san_extension',
     'userapi_extension',
     'groupapi_extension',
     'hyperics_extension',
     'postgresql_extension',
     'versantmanagement_extension',
     'epsjseapi_extension',
     'zookeeperapi_extension',
     'modeldeployment_extension',
     'configmanagerapi_extension',
     'mysql_extension',
     'opendj_extension',
     'elasticsearch_extension',
]

PROPERTY_TYPES_ROOT = "property_types"
ITEM_TYPES_ROOT = "item_types"
PLUGINS_ROOT = "plugins"
EXTENSIONS_ROOT = "extensions"

HEADING_PREFIX = "LITP "
PROP_TYPES = "Property Types"
ITEM_TYPES = "Item Types"
PLUGINS = "Plugins"
EXTENSIONS = "Model Extensions"
VALIDATORS_HEADING = HEADING_PREFIX + "Core Validators"
OPERATIONS_HEADING = HEADING_PREFIX + "Migration Operations"
ISO_RST_DIR = "/../rstFilesISO"

TOCTREE_HIDDEN_HEADING = """\n\n
.. toctree::
   :hidden:

"""

PLUGIN_TEMPLATE = """\
.. |external| raw:: html

   <img alt="external" src="../../_static/external_link_icon.svg">

LITP Plugin **'{plugin_name}'** ({plugin_version})
=======================================================

.. litp-plugin:: {plugin_name}

Overview
--------
{plugin_description}

{plugin_requires}

Validation
----------
{plugin_item_validation}

Configuration / Usage
---------------------
{plugin_item_config}

{snapshot_docs}
"""

PLUGIN_SNAPSHOT_TEMPLATE = """
Snapshot Validation
-------------------
{plugin_snapshot_validation}

Snapshot Configuration
----------------------
{plugin_snapshot_plan}
"""

EXTENSION_TEMPLATE = """\
LITP Model Extension **'{extension_name}'** ({extension_version})
===========================================================================

.. model-extension:: {extension_name}

Overview
--------
{extension_description}

{extension_required_by}

Defined Property Types
----------------------
{extension_property_types}

Defined Item Types
------------------
{extension_item_types}

Item Type Graph
---------------
.. graphviz:: {ext_model_dot}

"""

PROP_TABLE_HEADER_TEMPLATE = """\n
Properties
++++++++++

.. csv-table::
   :header: "Name", "Description", "Type",\
       "Always Present?",\
       "User-Specified?",\
       "Updatable by Plugin?",\
       "Updatable by REST?",\
       "Site-Specific?",\
       "Configuration?",\
       "Default Value"
   :widths: 8, 32, 10, 6, 6, 6, 6, 6, 6, 13

"""

STRUCT_TABLE_HEADER_TEMPLATE = """\n
Child Items
+++++++++++

.. csv-table::
   :header: "Child Item ID", "Description", "Option 1", "Option 2"
"""

DOC_HEADER_TEMPLATE = """{header}
==============================================

Overview
--------
.. include:: ../{section}_overview.rst

List of {list_type}
------------------------------------------------------------
"""

DOC_LINK_TEMPLATE = """
- :doc:`{link_target}`
"""

PROPERTY_TYPE_TEMPLATE = """
'{property_type_id}' {deprecated} Property Type
=====================================================================

.. property-type:: {property_type_id}

This property type is defined by \
:doc:`../extensions/{plugin_id}_extension/index`

Validators:
+++++++++++

    The value of the property is validated \
using the property validators listed below:

{property_type_validation}

"""

VALIDATOR_TEMPLATE = """
{validator_heading}

{validator_docstring}
{validator_options}
"""

ITEM_TYPE_TEMPLATE = """
'{type_name}' {deprecated} Item Type
=====================================================================

.. item-type:: {type_name}

Description
+++++++++++

{item_description}


Information
+++++++++++

- **{type_name}** is defined by:
  :doc:`../extensions/{plugin_id}_extension/index`

{extends_type}

{extended_by}

The following graphic illustrates this item type:

.. graphviz::  ./{type_name}.dot

{type_attributes}

Validators
++++++++++
{item_type_validation}

"""

PROPERTY_NOTES_TEMPLATE = """
Notes on Properties
-------------------
- **Always Present?** specifies whether this property is
  mandatory for the item type in question. If **Yes**, this property is
  automatically included if you add a '{type_name}' item to the the model;
  if the user then fails to specify a value for the property, the default
  value is used.
- **User-Specified?**  specifies whether the value of
  this property must be input by the user during item creation. If **Yes**,
  there is no default value for this property; the user must specify its value.
- **Updatable by Plugin?** specifies whether the value of this property
  can be set by a plug-in.
- **Updatable by REST?** specifies whether the value of this property can be
  updated by the REST interface after the item to which the property belongs
  has been applied.
- **Site-Specific?**  specifies whether this property allows site-specific
  values to pass offline XSD validation when they conform to the regular
  expression "%%[a-zA-Z0-9\-\._]+%%".
- **Configuration?** specifies whether the property can configure the system
  and generate plans.

"""

VALIDATORS_HEADER = VALIDATORS_HEADING + """
========================================

Overview
--------
Core provides a set of common validators which are listed below.
It is recommended that plugin developers use these where possible
to prevent duplicating common validation logic. This set of validators
will likely expand over time.

"""

OPERATION_TEMPLATE = """
{operation_name}
^^^^^^^^^^^^^^^^^^^^^^^^^^^
{operation_docstring}
{operation_options}
"""

OPERATIONS_HEADER = OPERATIONS_HEADING + """
========================================

Overview
--------
In order to facilitate migration tasks, Core provides a set of
common operations which allow an engineer to modify the state of
item types and properties in the LITP model. The operations are
listed below. Whenever an operation is performed it will be logged
as an INFO message in *"/var/log/messages"*.

"""

ITEM_TYPE_VALIDATORS = ("\nThe item type is validated"
                        " using the item validators listed below:\n")

ITEM_TYPE_NO_VALIDATORS = """
This item type has no additional validation.
"""

PROPERTY_ATTRIBUTE_TEMPLATE = \
'''   **{attrib_name}** {deprecated}, "{prop_description}",''' + \
" :ptype:`{attrib_type}`, " + \
"{attrib_required}, {user_must_input}, {updatable_plugin}, " + \
"{updatable_rest}, {site_specific}, {configuration}, {attrib_default}"

CHILD_ATTRIBUTE_TEMPLATE = \
'''   **{attrib_name}** {deprecated},  "Child of ''' + \
''' :itype:`{attrib_type}`",''' + \
"'required={attrib_required}', *N/A*"

REFERENCE_ATTRIBUTE_TEMPLATE = \
'''   **{attrib_name}** {deprecated}, "Inherited Child of ''' + \
''':itype:`{attrib_type}`",''' + \
"'required={attrib_required}', *N/A*"

COLLECTION_ATTRIBUTE_TEMPLATE = "   **{attrib_name}** {deprecated}, " + \
"\"{collection_type} of :itype:`{attrib_type}`\", " + \
" 'min count={min_count}', 'max count={max_count}'"

protected_item_types = ['root', 'litp-service-base', 'import-iso',
                                'logging', 'maintenance', 'restore_model',
                                'prepare-restore', 'restore']

itemtype_not_updatable = ['prepare_actions', 'prepare_path']


class SphinxGenerator(object):
    def __init__(self, root_path):
        self.plugins = []
        self.contrib_plugins = []
        self.extensions = []
        self.contrib_extensions = []
        self.property_types = []
        self.contrib_property_types = []
        self.item_types = []
        self.contrib_item_types = []
        self.attrib_formatters = {
            Property: self._format_property,
            View: self._format_view,
            Child: self._format_child,
            Collection: self._format_collection,
            Reference: self._format_reference,
            RefCollection: self._format_collection,
        }
        self.root_path = root_path
        self.iso_root_path = root_path + ISO_RST_DIR
        self.items = {}
        self.diagram = ClassDiagram()
        self.requires = {}
        self.required_by = {}
        self._log_properties_header()

    def _get_formatter(self, class_type):
        for formatter_type, method in self.attrib_formatters.items():
            if issubclass(class_type, formatter_type):
                return method
        raise Exception("Cannot find formatter for type %s" % (class_type,))

    def _get_property_types(self, plugin):
        try:
            return plugin.register_property_types()
        except:
            return plugin.define_property_types()

    def _get_item_types(self, plugin):
        try:
            types = plugin.register_item_types()
        except:
            types = plugin.define_item_types()
        return [t for t in types]

    @staticmethod
    def is_contributed_ext(extension_id):
        contrib = False
        if extension_id in CONTRIBUTED_EXTENSIONS:
            contrib = True
        return contrib

    @staticmethod
    def is_contributed_plugin(plugin_id):
        contrib = False
        if plugin_id in CONTRIBUTED_PLUGINS:
            contrib = True
        return contrib

    def generate_ext(self, ext_id, ext_ver, extension):
        property_types = self._get_property_types(extension)
        self.generate_property_types_doc(ext_id, property_types,
                contrib=self.is_contributed_ext(ext_id))
        item_types = self._get_item_types(extension)
        self.generate_item_types_doc(ext_id, item_types,
                contrib=self.is_contributed_ext(ext_id))
        self.generate_ext_doc(ext_id, ext_ver, extension)

    def generate_plugin(self, plugin_id, plugin_ver, plugin):
        property_types = self._get_property_types(plugin)
        self.generate_property_types_doc(plugin_id, property_types,
                contrib=self.is_contributed_plugin(plugin_id))
        item_types = self._get_item_types(plugin)
        self.generate_item_types_doc(plugin_id, item_types,
                contrib=self.is_contributed_plugin(plugin_id))
        self.generate_plugin_doc(plugin_id, plugin_ver, plugin)

    def generate_plugin_doc(self, plugin_id, plugin_ver, plugin):
        if self.is_contributed_plugin(plugin_id):
            self.contrib_plugins.append(plugin_id)
        else:
            self.plugins.append(plugin_id)
        plugin_path = os.path.join(self.root_path, PLUGINS_ROOT,
                                   plugin_id.lower() + "_plugin", "index.rst")
        self._write_file(plugin_path, self._create_plugin_rst(plugin_id,
                                                              plugin_ver,
                                                              plugin))
        if not self.is_contributed_plugin(plugin_id):
            iso_plugin_path = os.path.join(self.iso_root_path, PLUGINS_ROOT,
                                   plugin_id.lower() + "_plugin", "index.rst")
            self._write_file(iso_plugin_path,
                              self._create_plugin_rst(plugin_id,
                                                      plugin_ver,
                                                      plugin,
                                                      iso_docs=True))

    def generate_ext_doc(self, ext_id, ext_ver, extension):
        if self.is_contributed_ext(ext_id):
            self.contrib_extensions.append(ext_id)
        else:
            self.extensions.append(ext_id)
        plugin_path = os.path.join(self.root_path, EXTENSIONS_ROOT,
                                   ext_id.lower() + "_extension", "index.rst")
        self._write_file(plugin_path, self._create_extension_rst(ext_id,
                                                                 ext_ver,
                                                                 extension))
        if not self.is_contributed_ext(ext_id):
            iso_plugin_path = os.path.join(self.iso_root_path, EXTENSIONS_ROOT,
                                   ext_id.lower() + "_extension", "index.rst")
            self._write_file(iso_plugin_path,
                             self._create_extension_rst(ext_id,
                                                        ext_ver,
                                                        extension,
                                                        iso_docs=True))

    def generate_property_types_doc(self, plugin_id,
                                    prop_types, contrib=False):
        for prop_type in sorted(prop_types):
            if contrib:
                self.contrib_property_types.append(prop_type.property_type_id)
            else:
                self.property_types.append(prop_type.property_type_id)
            prop_path = os.path.join(self.root_path, PROPERTY_TYPES_ROOT,
                                     prop_type.property_type_id + ".rst")
            prop_path = self._clean_path(prop_path)
            content = self._create_property_type_rst(plugin_id, prop_type)
            self._write_file(prop_path, content)
            if not contrib:
                iso_prop_path = os.path.join(
                    self.iso_root_path,
                    PROPERTY_TYPES_ROOT,
                    self._clean_path(prop_type.property_type_id + ".rst")
                )
                self._write_file(iso_prop_path, content)

    def generate_item_types_doc(self, plugin_id, item_types, contrib=False):
        for item_type in sorted(item_types):
            if contrib:
                self.contrib_item_types.append(item_type.item_type_id)
            else:
                self.item_types.append(item_type.item_type_id)
            item_path = os.path.join(self.root_path, ITEM_TYPES_ROOT,
                                     item_type.item_type_id + ".rst")
            item_path = self._clean_path(item_path)
            iso_item_path = os.path.join(self.iso_root_path, ITEM_TYPES_ROOT,
                self._clean_path(item_type.item_type_id + ".rst"))
            content = self._create_item_type_rst(plugin_id, item_type)
            self._write_file(item_path, content)
            if not contrib:
                content = self._create_item_type_rst(plugin_id,
                                                     item_type,
                                                     iso_docs=True)
                self._write_file(iso_item_path, content)

            if plugin_id not in self.items:
                self.items[plugin_id] = [item_type]
            else:
                self.items[plugin_id].append(item_type)

            # generate dot graph for this item type
            dot_path = os.path.join(self.root_path, ITEM_TYPES_ROOT,
                                    item_type.item_type_id + ".dot"
            )
            content = self.diagram.generate_data_model_graph(
                        self.items,
                        item_type=item_type.item_type_id
            )
            self._write_file(dot_path, content)
            if not contrib:
                iso_dot_path = os.path.join(
                    self.iso_root_path, ITEM_TYPES_ROOT,
                    item_type.item_type_id + ".dot"
                )
                self._write_file(iso_dot_path, content)

    def create_item_type_hierarchy(self, extensions):
        item_types = []      # excludes contrib
        all_item_types = []  # includes contrib
        for ext_name, _, ext in extensions:
            if ext_name not in CONTRIBUTED_EXTENSIONS:
                item_types.extend(self._get_item_types(ext))
            all_item_types.extend(self._get_item_types(ext))
        ancestors, descendants = self._gen_item_type_hierarchy(all_item_types)
        self.ancestors = ancestors
        self.descendants = descendants
        ancestors, descendants = self._gen_item_type_hierarchy(item_types)
        self.non_contrib_ancestors = ancestors
        self.non_contrib_descendants = descendants

    def _gen_item_type_hierarchy(self, item_types):
        ancestors = dict()
        descendants = dict()
        for item_type in item_types:
            if 'baseitem' == item_type:
                ancestors[item_type.item_type_id] = None
            else:
                if item_type.extend_item:
                    ancestors[item_type.item_type_id] = item_type.extend_item
                    if not item_type.extend_item in descendants:
                        descendants[item_type.extend_item] = \
                            set([item_type.item_type_id])
                    else:
                        descendants[item_type.extend_item].add(
                            item_type.item_type_id
                        )
        return ancestors, descendants

    def generate_index_doc(self):
        self.generate_plugin_index_doc()
        self.generate_contrib_plugin_index_doc()
        self.generate_extension_index_doc()
        self.generate_contrib_extension_index_doc()
        self.generate_property_types_index_doc()
        self.generate_contrib_property_types_index_doc()
        self.generate_item_types_index_doc()
        self.generate_contrib_item_types_index_doc()

        # write complete items type graph for all item types
        #dot_path = os.path.join(
        #    self.root_path, ITEM_TYPES_ROOT, "all_items.dot")
        #self._write_file(dot_path,
        #                 self.diagram.generate_data_model_graph(self.items)
        #)

    def generate_validators_doc(self, validators_module):
        members = dir(validators_module)
        classes = [getattr(validators_module, m) for m in members]

        prop_validator_classes = []
        item_validator_classes = []
        for validator_class in classes:
            if inspect.isclass(validator_class):
                if issubclass(validator_class, PropertyValidator):
                    is_base_validator = False
                    if validator_class == PropertyValidator:
                        is_base_validator = True
                    prop_validator_classes.append(
                        (validator_class, is_base_validator)
                    )
                if issubclass(validator_class, ItemValidator):
                    is_base_validator = False
                    if validator_class == ItemValidator:
                        is_base_validator = True
                    item_validator_classes.append(
                        (validator_class, is_base_validator)
                    )

        prop_validators = self._format_validator_classes(
            prop_validator_classes,
            ".. _prop-validators:\n\nProperty Validators")
        item_validators = self._format_validator_classes(
            item_validator_classes,
            ".. _item-validators:\n\nItem Validators")

        index_path = os.path.join(self.root_path,
                                  "plugin_api",
                                  "validators.rst")
        validators_content = VALIDATORS_HEADER + \
            prop_validators + item_validators

        self._write_file(index_path, validators_content)

    def generate_operations_doc(self, operations_module):
        members = dir(operations_module)
        classes = [getattr(operations_module, m) for m in members]

        operation_classes = []
        for operation_class in classes:
            if inspect.isclass(operation_class):
                if issubclass(operation_class, BaseOperation):
                    is_base_operation = False
                    if operation_class == BaseOperation:
                        is_base_operation = True
                    operation_classes.append(
                        (operation_class, is_base_operation)
                    )

        operations = self._format_operation_classes(
            operation_classes,
            ".. _migration-operations:\n\nMigration operations")
        index_path = os.path.join(self.root_path,
                                  "plugin_api",
                                  "operations.rst")
        operations_content = OPERATIONS_HEADER + operations

        self._write_file(index_path, operations_content)

    @staticmethod
    def _fullclassname(klass):
        return klass.__module__ + "." + klass.__name__

    def _format_validator_classes(self, classes, heading):
        lines = []
        lines.append("\n" + heading + "\n++++++++++++++++++++++\n\n")
        for (c, is_base) in classes:
            skip_index = ''
            if is_base:
                skip_index = '    :noindex:\n'
            lines.append(".. autoclass:: " + \
                    self._fullclassname(c) + "\n" +\
                    skip_index
#                    "    :members: __init__, validate" + "\n"
            )
        return "\n".join(lines)

    def _format_operation_classes(self, classes, heading):
        lines = []
        lines.append("\n" + heading + "\n++++++++++++++++++++++\n\n")
        for (c, is_base) in classes:
            skip_index = ''
            if is_base:
                skip_index = '    :noindex:\n'
            lines.append(".. autoclass:: " +
                         self._fullclassname(c) + "\n" +
                         skip_index)
        return "\n".join(lines)

    def generate_plugin_index_doc(self):
        index_path = os.path.join(
                self.root_path, PLUGINS_ROOT, "index.rst")
        content = self._create_index_rst(PLUGINS,
                                         "plugins",
                                          self.plugins,
                                          is_plugin=True)
        self._write_file(index_path, content)
        iso_index_path = os.path.join(
                self.iso_root_path, PLUGINS_ROOT, "index.rst")
        self._write_file(iso_index_path, content)

    def generate_contrib_plugin_index_doc(self):
        index_path = os.path.join(
                self.root_path, PLUGINS_ROOT, "contrib_index.rst")
        self._write_file(index_path,
                         self._create_index_rst("Contributed " + PLUGINS,
                                                "plugins",
                                                self.contrib_plugins,
                                                is_plugin=True))

    def generate_extension_index_doc(self):
        index_path = os.path.join(
            self.root_path, EXTENSIONS_ROOT, "index.rst")
        content = self._create_index_rst(EXTENSIONS,
                                          "extensions",
                                          self.extensions,
                                          is_ext=True)
        self._write_file(index_path, content)
        iso_index_path = os.path.join(
            self.iso_root_path, EXTENSIONS_ROOT, "index.rst")
        self._write_file(iso_index_path, content)

    def generate_contrib_extension_index_doc(self):
        index_path = os.path.join(
                self.root_path, EXTENSIONS_ROOT, "contrib_index.rst")
        self._write_file(index_path,
                         self._create_index_rst("Contributed " + EXTENSIONS,
                                                "extensions",
                                                self.contrib_extensions,
                                                is_ext=True))

    def generate_property_types_index_doc(self):
        index_path = os.path.join(
                self.root_path, PROPERTY_TYPES_ROOT, "index.rst")
        iso_index_path = os.path.join(
                self.iso_root_path, PROPERTY_TYPES_ROOT, "index.rst")
        content = self._create_index_rst(PROP_TYPES,
                                         "property_types",
                                         self.property_types)
        self._write_file(index_path, content)
        self._write_file(iso_index_path, content)

    def generate_contrib_property_types_index_doc(self):
        index_path = os.path.join(
                self.root_path, PROPERTY_TYPES_ROOT, "contrib_index.rst")
        iso_index_path = os.path.join(
                self.iso_root_path, PROPERTY_TYPES_ROOT, "contrib_index.rst")
        content = self._create_index_rst("Contributed " + PROP_TYPES,
                                         "property_types",
                                          self.contrib_property_types)
        self._write_file(index_path, content)

    def generate_item_types_index_doc(self):
        index_path = os.path.join(self.root_path, ITEM_TYPES_ROOT, "index.rst")
        iso_index_path = os.path.join(
            self.iso_root_path, ITEM_TYPES_ROOT, "index.rst")
        content = self._create_index_rst(ITEM_TYPES,
                                         "item_types",
                                         self.item_types)
        self._write_file(index_path, content)
        self._write_file(iso_index_path, content)

    def generate_contrib_item_types_index_doc(self):
        index_path = os.path.join(
                self.root_path, ITEM_TYPES_ROOT, "contrib_index.rst")
        iso_index_path = os.path.join(
                self.iso_root_path, ITEM_TYPES_ROOT, "contrib_index.rst")
        content = self._create_index_rst(
            "Contributed " + ITEM_TYPES,
            "item_types", self.contrib_item_types)
        self._write_file(index_path, content)

    def _clean_path(self, filepath):
        if self.root_path in filepath and ISO_RST_DIR not in filepath:
            relpath = filepath.split(self.root_path)[1].lower().replace('-',
                                                                        '_')
            if relpath.startswith('/'):
                relpath = relpath[1:]
            return os.path.join(self.root_path, relpath)
        else:
            return filepath.lower().replace('-', '_')

    def _clean_doc(self, docstring):
        return (docstring or "")

    def _write_file(self, filepath, contents):
        try:
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))
            newfile = open(filepath, "w")
            newfile.write(contents)
        except:
            log.trace.exception("Exception writing Sphinx file: %s", filepath)
            raise

    def _extends_string(self, item_type, iso_docs):
        if iso_docs:
            ancestors = self.non_contrib_ancestors
        else:
            ancestors = self.ancestors

        if not item_type.item_type_id in ancestors:
            return ""
        else:
            return "- **{0}** extends :doc:`{1}`".format(
                    item_type.item_type_id,
                    self._clean_path(ancestors[item_type.item_type_id]))

    def _structure_string(self, item_type):
        if not item_type.item_type_id in self.ancestors:
            return ("This item type can be created with the following "
                   "*structure* / properties:")
        else:
            return ("This item type inherits its structure from the "
                    ":doc:`{0}` which it extends. "
                    "You can create an item of "
                    "this type using a combination "
                    "of the inherited properties and the properties "
                   "listed below:").format(self._clean_path(
                       self.ancestors[item_type.item_type_id]))

    def _extended_by_string(self, item_type, iso_docs):
        if iso_docs:
            descendants = self.non_contrib_descendants
        else:
            descendants = self.descendants
        if not item_type.item_type_id in descendants:
            return ""
        else:
            # There may be several descendants
            descendant_types = ["  - :doc:`%s`\n" %\
                    (self._clean_path(descendant)) for descendant in \
                    sorted(descendants[item_type.item_type_id])]
            return '- **{0}** is extended by:\n\n'.format(
                        item_type.item_type_id
                    ) + '\n'.join(descendant_types)

    def _create_index_rst(self, heading, section, items,
                          is_plugin=False, is_ext=False):
        index_items = []
        index_items.append(
                DOC_HEADER_TEMPLATE.format(header=HEADING_PREFIX + heading,
                                           list_type=heading,
                                           section=section
                )
        )
        for item in sorted(items):
            print("Generating index for item %s %s, %s"
                   % (item, is_plugin, is_ext))
            if is_plugin:
                target = item + "_plugin/index"
            elif is_ext:
                target = item + "_extension/index"
            else:
                target = item
            index_items.append(self._format_doc_link(
                                    self._clean_path(target)))
        index_items.append(TOCTREE_HIDDEN_HEADING)
        for item in sorted(items):
            print("Generating toctree for item %s %s, %s"
                   % (item, is_plugin, is_ext))
            if is_plugin:
                target = "   " + item + "_plugin/index.rst\n"
            elif is_ext:
                target = "   " + item + "_extension/index.rst\n"
            else:
                target = "   " + item + ".rst\n"
            index_items.append(self._clean_path(target))

        return "".join(index_items)

    def _create_plugin_rst(self, plugin_name, plugin_ver, plugin,
                           iso_docs=False):

        dot_path = os.path.join(self.root_path, PLUGINS_ROOT,
                plugin_name.lower() + "_plugin",
                plugin_name.lower() + ".dot"
        )
        self._write_file(dot_path,
                self.diagram.generate_data_model_graph(self.items, plugin_name)
        )
        iso_dot_path = os.path.join(self.iso_root_path, PLUGINS_ROOT,
                plugin_name.lower() + "_plugin",
                plugin_name.lower() + ".dot"
        )
        self._write_file(iso_dot_path,
                self.diagram.generate_data_model_graph(self.items, plugin_name)
        )
        if iso_docs:
            plugin_description = self._clean_doc(plugin.__doc__)
        else:
            plugin_description = self._autoclass_doc(plugin)
        plugin_data = dict(
            plugin_name=plugin_name,
            plugin_version=plugin_ver,
            plugin_description=plugin_description,
            plugin_requires=self._requires_string(plugin_name),
            plugin_item_validation=plugin.validate_model.__doc__,
            plugin_item_config=plugin.create_configuration.__doc__,
            snapshot_docs=self._get_plugin_snapshot_doc(plugin)
        )
        return PLUGIN_TEMPLATE.format(**plugin_data)

    def _get_plugin_snapshot_doc(self, plugin):
        doc = ''
        snapshot_data = dict()
        snapshot_data['plugin_snapshot_validation'] = None
        snapshot_data['plugin_snapshot_plan'] = None
        if self._get_class_that_defined_method(
                                plugin.validate_model_snapshot):
            snapshot_data['plugin_snapshot_validation'] \
                 = plugin.validate_model_snapshot.__doc__
        if self._get_class_that_defined_method(
                                plugin.create_snapshot_plan):
            snapshot_data['plugin_snapshot_plan'] \
                 = plugin.create_snapshot_plan.__doc__

        if snapshot_data['plugin_snapshot_validation'] == None and \
        snapshot_data['plugin_snapshot_plan'] == None:
            return doc

        if snapshot_data['plugin_snapshot_validation'] == None:
            snapshot_data['plugin_snapshot_validation'] = \
               "No Snapshot Validation required"
        if snapshot_data['plugin_snapshot_plan'] == None:
            snapshot_data['plugin_snapshot_plan'] = \
               "No Snapshot Configuration needed"
        doc = PLUGIN_SNAPSHOT_TEMPLATE.format(**snapshot_data)
        return doc

    def _get_class_that_defined_method(self, method):
        for cls in inspect.getmro(method.im_class):
            if method.__name__ in cls.__dict__:
                class_type = inspect.getmro(cls)
                #If value is 2, its a base class that we don't want
                if len(class_type) > 2:
                    return True
        return False

    def _requires_string(self, plugin_name):
        if plugin_name in ("core_plugin", "puppet_manager"):
            return ""
        required_exts = ["  - :doc:`%s`\n" % \
                    (self._doc_ref_path(*require)) \
                    for require in \
                    sorted(self.requires[(plugin_name, 'plugin')])]
        return 'This plugin requires:\n' + '\n'.join(required_exts)

    def _doc_ref_path(self, name, type):
        doc_ref_path = '../../%ss/%s_%s/index' % (type, name, type)
        return self._clean_path(doc_ref_path)

    def _autoclass_doc(self, klass):
        return ".. autoclass:: {0}".format(
                                self._fullclassname(klass.__class__))

    def _create_extension_rst(self, extension_name, extension_ver, extension,
                              iso_docs=False):

        dot_path = os.path.join(self.root_path, EXTENSIONS_ROOT,
                extension_name.lower() + "_extension",
                extension_name.lower() + ".dot"
        )
        iso_dot_path = os.path.join(self.iso_root_path, EXTENSIONS_ROOT,
                extension_name.lower() + "_extension",
                extension_name.lower() + ".dot"
        )
        # dont't generate graph for the core extension as it is too complex
        if extension_name != 'core_extension':
            content = self.diagram.generate_data_model_graph(self.items,
                                                             extension_name)

            self._write_file(dot_path, content)
            self._write_file(iso_dot_path, content)
            dot_file = extension_name.lower() + ".dot"
        else:
            dot_file = extension_name.lower() + ".dot\n\nNone available."

        if iso_docs:
            extension_description = self._clean_doc(extension.__doc__)
        else:
            extension_description = self._autoclass_doc(extension)

        ext_data = dict(
           extension_name=extension_name,
           extension_version=extension_ver,
           extension_description=extension_description,
           extension_required_by=self._required_by_string(extension_name),
           extension_property_types=self._format_defined_prop_types(extension),
           extension_item_types=self._format_defined_item_types(extension),
           ext_model_dot=dot_file,
        )
        return EXTENSION_TEMPLATE.format(**ext_data)

    def _required_by_string(self, extension_name):
        if extension_name == "core_extension":
            return ""
        required_by = ["  - :doc:`%s`\n" % \
                    (self._doc_ref_path(*require)) \
                    for require in \
                    sorted(self.required_by[(extension_name, 'extension')])]
        return 'This extension is required by:\n' + '\n'.join(required_by)

    def _format_validator(self, validator):
        options = ''
        for property, value in vars(validator).iteritems():
            options += "    - **%s:**  ``%s``\n" % (property, value)

        validator_name = validator.__class__.__name__
        underlined_validator_name = validator_name + '\n' + \
               ('-' * len(validator_name))
        validator_data = dict(
                         validator_heading=underlined_validator_name,
                         validator_docstring=validator.__doc__,
                         validator_options=options,
                         )
        return VALIDATOR_TEMPLATE.format(**validator_data)

    def _create_property_type_rst(self, plugin_id, prop_type):
        property_type_validation = ''
        for validator in  prop_type.validators:
            property_type_validation += self._format_validator(validator)

        property_type_data = dict(
            plugin_id=plugin_id.lower(),
            property_type_id=prop_type.property_type_id,
            deprecated=self._get_deprecated_string(prop_type),
            property_type_validation=property_type_validation
        )
        return PROPERTY_TYPE_TEMPLATE.format(**property_type_data)

    def _create_item_type_rst(self, plugin_id, item_type, iso_docs=False):
        item_type_validation = ''
        if item_type.validators:
            item_type_validation = ITEM_TYPE_VALIDATORS
            for validator in  item_type.validators:
                item_type_validation += self._format_validator(validator)
        else:
            item_type_validation = ITEM_TYPE_NO_VALIDATORS

        if not item_type.item_description:
            print "Warning: No description for item type '%s'" % \
                    (item_type.item_type_id)
        item_type_data = dict(
            plugin_id=plugin_id.lower(),
            type_name=item_type.item_type_id,
            deprecated=self._get_deprecated_string(item_type),
            equals="".join(['=' for i in range(len(item_type.item_type_id))]),
            item_description=(item_type.item_description or 'N/A').\
                    replace('{', '{{').replace('}', '}}'),
            extends_type=self._extends_string(item_type, iso_docs),
            extended_by=self._extended_by_string(item_type, iso_docs),
            type_attributes=self.format_attributes(item_type),
            item_type_validation=item_type_validation,
        )
        return ITEM_TYPE_TEMPLATE.format(**item_type_data)

    def _format_doc_link(self, link_target):
        link_data = dict(link_target=link_target)
        return DOC_LINK_TEMPLATE.format(**link_data)

    def _prop_type_target(self, prop_type):
        return "../../%s/%s" % (PROPERTY_TYPES_ROOT,
                                self._clean_path(prop_type.property_type_id))

    def _format_registered_prop_types(self, plugin):

        def compare_prop(el1, el2):
            if (el1.property_type_id) < (el2.property_type_id):
                return -1
            if (el1.property_type_id) > (el2.property_type_id):
                return 1
            return 0

        property_type_links = []
        for prop_type in sorted(self._get_property_types(plugin),
                                compare_prop):
            property_type_links.append(self._format_doc_link(
                self._prop_type_target(prop_type))
            )
        return "\n".join(property_type_links)

    def _item_type_target(self, item_type):
        return "../../%s/%s" % (ITEM_TYPES_ROOT,
                                self._clean_path(item_type.item_type_id))

    def _format_registered_item_types(self, plugin):
        item_type_links = []

        def compare_item(el1, el2):
            if (el1.item_type_id) < (el2.item_type_id):
                return -1
            if (el1.item_type_id) > (el2.item_type_id):
                return 1
            return 0

        for item_type in sorted(self._get_item_types(plugin),
                                compare_item):
            item_type_links.append(self._format_doc_link(
                self._item_type_target(item_type))
            )
        return "\n".join(item_type_links)

    def _format_defined_item_types(self, extension):
        return self._format_registered_item_types(extension)

    def _format_defined_prop_types(self, extension):
        return self._format_registered_prop_types(extension)

    def _log_properties_header(self):
        self._log_property("%s,%s,%s,%s,%s,%s,%s" % \
          ("item_type_id",
           "property_name",
           "is_required",
           "has_default",
           "default_value",
           "is_rest_updatable",
           "is_plugin_updatable"))

    def _log_property(self, line):
        with open("target/item_properties.csv", "a+") as f:
            f.write(line + "\n")

    def format_attributes(self, item_type):
        templates = []
        template = PROP_TABLE_HEADER_TEMPLATE

        # Generate documentation for Properties and Views
        header = True
        for att_id, attribute in sorted(item_type.structure.items()):
            if (isinstance(attribute, Property) or isinstance(attribute,
                    View)):
                if header:
                    templates.append(template)
                    header = False
                formatter = self._get_formatter(type(attribute))
                templates.append(formatter(att_id, attribute))
                if isinstance(attribute, Property):
                    self._log_property("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % \
                      (item_type.item_type_id,
                       att_id,
                       attribute.required,
                       str(attribute.default is not None),
                       '"' + str(attribute.default) + '"',
                       attribute.updatable_rest,
                       attribute.updatable_plugin,
                       attribute.configuration,
                       attribute.deprecated,
                       attribute.site_specific))

        if header == False:
            templates.append(PROPERTY_NOTES_TEMPLATE.format(
                                type_name=item_type.item_type_id)
                            )

        # Generate documentation for structural elements other than Properties
        # and Views
        header = True
        for att_id, attribute in sorted(item_type.structure.items()):
            if not (isinstance(attribute, Property) or \
                    isinstance(attribute, View)):
                if header:
                    templates.append(STRUCT_TABLE_HEADER_TEMPLATE)
                    header = False
                templates.append(self._get_formatter(type(attribute))(att_id,
                attribute))

        # if we have props / structure then add structure header string
        if templates:
            templates.insert(0, self._structure_string(item_type))

        # Format the attributes
        format_param = dict(
                type_name=item_type.item_type_id
                )
        item_type_rst = "\n".join(templates).format(**format_param)
        item_type_rst = item_type_rst.replace('{{', '{').replace('}}', '}')
        return item_type_rst

    def _format_xml_snippet(self, item_type):
        template = []
        if item_type.item_type_id in protected_item_types:
            template.append("Item Type '%s' is created by default "
                                "in the model" % (item_type.item_type_id))
            return " ".join(template)

        if item_type.extend_item:
            template.append("<!-- The '%s' item type extends the '%s' item "
                             "type. Check the '%s' item_type for base "
                             "property types  -->" %
                            (item_type.item_type_id, item_type.extend_item,
                             item_type.extend_item))
        template.append("<litp:%s id=\"{%s_ID}\">" %
                        (item_type.item_type_id,
                         item_type.item_type_id.upper()))
        for att_id, attribute in sorted(item_type.structure.items()):
            att_type = attribute.item_type_id
            if isinstance(attribute, Property):
                self._get_property_information(template, attribute, att_id,
                                         True)
            elif isinstance(attribute, Child):
                self._get_type_template(template, att_type, attribute, att_id)
            elif isinstance(attribute, Reference):
                att_type += "-inherit"
                template.append(
                    '  <litp:%s source_path="/../../" id=\"%s\"/>' % \
                    (att_type, att_id)
                )
            elif isinstance(attribute, RefCollection):
                desc = item_type.item_type_id + "-" + att_id + "-collection"
                self._get_type_template(template, desc, attribute, att_id)
            elif  isinstance(attribute, Collection):
                desc = item_type.item_type_id + "-" + att_id + "-collection"
                self._get_type_template(template, desc, attribute, att_id)
        template.append('</litp:%s>' % item_type.item_type_id)
        return "\n    ".join(template)

    def _get_property_information(self, template, attribute,
                                  att_id, xml_format=False):
        if not attribute.updatable_plugin:
            if getattr(attribute, 'default') != None:
                if xml_format:
                    template.append("  <%s>%s</%s>" %
                         (att_id, attribute.default, att_id))
                else:
                    template.append("%s='%s'" % (att_id, attribute.default))
            else:
                if xml_format:
                    template.append("  <%s>{%s_VALUE}</%s>" % \
                        (att_id, att_id.upper(), att_id))
                else:
                    template.append("%s='{%s_VALUE}'" % \
                                    (att_id, att_id.upper()))

    def _get_type_template(self, template, desc, attribute, att_id):
        template.append('  <litp:%s id="%s">' % (desc, att_id))
        if isinstance(attribute, RefCollection):
            template.append('     <!-- Inherit additional %s\'s here -->'
                            % att_id)
        elif isinstance(attribute, Collection):
            template.append('     <!-- Add additional %s\'s here -->'
                          % att_id)
        template.append('  </litp:%s>' % (desc))

    def _format_cli_snippet(self, item_type):
        cli_template = []
        first_element = True
        if item_type.item_type_id in protected_item_types:
            cli_template.append("Item Type '%s' is created by default "
                                "in the model" % (item_type.item_type_id))
            return " ".join(cli_template)
        if item_type.extend_item:
            cli_template.append("# The '%s' item type extends the '%s' "
                            "item type. Check the '%s' item_type for "
                            "base property types\n   " %
                            (item_type.item_type_id, item_type.extend_item,
                            item_type.extend_item))
        cli_template.append("litp create -t %s -p ../%s1" %
                               (item_type.item_type_id,
                                item_type.item_type_id))
        for att_id, attribute in sorted(item_type.structure.items()):
            if isinstance(attribute, Property):
                if first_element:
                    cli_template.append("-o")
                    first_element = False
                self._get_property_information(cli_template, attribute,
                                                att_id)
        return " ".join(cli_template)

    def _format_property(self, property_id, property):
        on_item, user_input, default_caption = self._property_semantics(
                property)
        prop_template = PROPERTY_ATTRIBUTE_TEMPLATE

        if not property.prop_description:
            print "Warning: No description for property '%s'" % (property_id)
        prop_data = dict(
            attrib_name=property_id,
            deprecated=self._get_deprecated_string(property),
            attrib_type=property.prop_type_id,
            prop_description=self._format_desc(property.prop_description),
            attrib_required=on_item,
            user_must_input=user_input,
            attrib_default=default_caption,
            updatable_plugin=self._format_boolean_value(
                property.updatable_plugin),
            updatable_rest=self._format_boolean_value(
                property.updatable_rest),
            site_specific=self._format_boolean_value(
                property.site_specific),
            configuration=self._format_boolean_value(
                property.configuration)
        )
        for (template_key, template_value) in prop_data.iteritems():

            prop_data[template_key] = template_value.replace('{', '{{').\
                    replace('}', '}}')
        return prop_template.format(**prop_data)

    def _format_boolean_value(self, val):
        if val == True:
            return "Yes"
        if val == False:
            return "No"
        return "N/A"

    def _format_desc(self, desc):
        # sphinx csv tables require "" to display a "
        desc = desc.replace('"', '""')
        desc = desc.replace('""""', '""')
        return desc

    def _format_view(self, view_id, view_instance):
        on_item, user_input, default_caption = self._property_semantics(
                    view_instance)

        if not view_instance.item_description:
            print "Warning: No description for view '%s'" % (view_id)
        view_data = dict(
            attrib_name=view_id,
            deprecated=self._get_deprecated_string(view_instance),
            attrib_type="N/A",
            prop_description="(**View**) " + \
                    (view_instance.item_description),
            attrib_required=on_item,
            user_must_input=user_input,
            attrib_default=default_caption,
            updatable_plugin=self._format_boolean_value(None),
            updatable_rest=self._format_boolean_value(None),
            site_specific=self._format_boolean_value(None),
            configuration=self._format_boolean_value(None)
        )
        for (template_key, template_value) in view_data.iteritems():
            view_data[template_key] = template_value.replace('{', '{{').\
                    replace('}', '}}')
        return PROPERTY_ATTRIBUTE_TEMPLATE.format(**view_data)

    def _default_or_not(self, val):
        if val:
            return val
        else:
            return ''

    def _property_semantics(self, instance):
        if isinstance(instance, View):
            return ("Yes", "*N/A*", "*N/A* - Views are dynamic")
        if not instance.required:
            if instance.item_type_id in itemtype_not_updatable:
                return ("Yes", "No", "\"``{0}`` "\
                        "\"".format(instance.default))
            elif instance.default:
                return ("Yes", "No", "\"``{0}`` - is used if no value is "\
                        "given\"".format(instance.default))
            else:
                return ("No", "No", "\"*No default value* - property absent"
                        " from item unless it is populated\"")
        else:
            if instance.default:
                if instance.prop_type_id == "hostname":
                    # 8884 - Overwrite sockect.gethostname() for ms
                    default_val = "\"The hostname of the current machine " \
                            "is used if no value is given\""
                else:
                    default_val = "\"``{0}`` - is used if no value is " \
                            "given\"".format(instance.default)
                return ("Yes", "No", default_val)
            else:
                return ("Yes", "Yes", "\"*No default value* - value **must** "
                        "be input by user\"")

    def _yes_or_no(self, req, default):
        if req and default is None:
            return "Yes"
        else:
            return "No"

    @staticmethod
    def _get_deprecated_string(item):
        deprecation_string = ''
        if item.deprecated:
            deprecation_string = ' **(deprecated)**'
        return deprecation_string

    def _format_child(self, child_id, child_type):
        item_data = dict(
            attrib_name=child_id,
            deprecated=self._get_deprecated_string(child_type),
            attrib_type=child_type.item_type_id,
            attrib_required=self._yes_or_no(child_type.required,
                                            None),
        )
        return CHILD_ATTRIBUTE_TEMPLATE.format(**item_data)

    def _format_reference(self, reference_id, reference_type):
        item_data = dict(
            attrib_name=reference_id,
            deprecated=self._get_deprecated_string(reference_type),
            attrib_type=reference_type.item_type_id,
            attrib_required=self._yes_or_no(reference_type.required,
                                            None),
        )
        return REFERENCE_ATTRIBUTE_TEMPLATE.format(**item_data)

    @staticmethod
    def _collection_string(collection_type):
        if collection_type.__class__.__name__ == "RefCollection":
            return "Inherited collection"
        else:
            return collection_type.__class__.__name__

    def _format_collection(self, collection_id, collection_type):
        item_data = dict(
            collection_type=self._collection_string(collection_type),
            attrib_name=collection_id,
            deprecated=self._get_deprecated_string(collection_type),
            attrib_type=collection_type.item_type_id,
            min_count=collection_type.min_count or 0,
            max_count=collection_type.max_count or "unlimited",
        )
        return COLLECTION_ATTRIBUTE_TEMPLATE.format(**item_data)
