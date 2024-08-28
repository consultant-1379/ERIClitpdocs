.. _model-migration-guide:

LITP |release| Model Migration
==============================

LITP maintains a version for each defined item type and is aware of the
last migration executed on a given installation. It can execute all
forward migrations in sequence so that all item types are brought to
the correct version of the given release. The migration process looks in
each plugin's configuration to find where its migration scripts are stored
and collects them. It will sequence the overall list of migrations to be
executed and execute them on the restart of the deployment manager after
the new versions of the plugins are installed.

The following basic operations are supported:

#. RemoveProperty
#. AddProperty
#. RenameProperty
#. AddCollection
#. AddRefCollection

More information on operations provided by core can be found
at :doc:`../plugin_api/operations`


Deprecation
===========

It is recommended that properties and item types are marked as deprecated for
one release cycle before being removed.
Property and item types have deprecated flags that allow them be flagged for
deprecation (by setting *deprecated=True*) before they are removed.
When an deprecated item is created or updated, a warning message is logged
(in /var/log/messages) and item types & properties for deprecation are
highlighted in the auto-generated Sphinx documentation.
The deprecated flags can be seen in item type and property documentation
at :ref:`plugin-api-item-types`.


Basic Operation
===============

When you shut down the LITP daemon (litpd), update the LITP software and
restart litpd, any version changes to LITP and the model extensions are
detected, and migration scripts update the existing model to be inline with
the new software.

Migration scripts are python files that are stored in a given set location
(for example, /opt/ericsson/nms/litp/etc/migrations/<model_extension_name>/001_add_property_foo.py).
If any migration files are present in etc/migrations/<model_extension_name>
they will be detected by the integration pom and included in the built rpm.

*The following shows a sample layout of a projects 'etc/migrations/' directory:*

.. code-block:: bash

    [ERIClitppackageapi]# find etc/migrations/
     etc/migrations/
     etc/migrations/package_extension
     etc/migrations/package_extension/__init__.py
     etc/migrations/package_extension/001_add_property_foo.py

Each migration file contains a list of operations to be performed on the model
and the version at which this migration will be applied.
When you shut down litpd, update to older LITP software and restart litpd,
it will detect the older version and apply any required migration.


When a Migration Script Is Required 
-----------------------------------
  
- If you add a collection to an item type, the migration script must add that collection to any model item instances of that item type in the model.

- If you add a required property (with a default value) to an existing item type, the migration script must set the property on existing item types with the default value.

- If you add an optional property (with a default value) to an existing item type, the migration script must set the property on existing item types with the default value.

- If you add a required property with no default value to an existing item type, the migration script must set the value for that property type on existing item types.


When a Migration Script Is Not Required 
---------------------------------------

- If you add new property types. 

- If you add an optional property (with no default value) to an existing item type.


Sample Migration Scripts
------------------------

The following example shows a sample migration script that is used to add
'new_prop1' with a default value of 'value1' to all package items:

.. code-block:: python

    from litp.migration import BaseMigration
    from litp.migration.operations import AddProperty

    class Migration(BaseMigration):
        version = '1.0.22'
        operations = [
            AddProperty('package', 'new_prop1', 'value1')
        ]

.. note::
   There should be only one Migration defined per migration file and the class
   MUST be called Migration, or the operation will not be carried out.

If all migrations are successful the model is saved and the *litpd* service is started.

If a migration fails, the migration file is logged but the service will
not be started. The saved model data is not updated.

The following example shows a migration script that contains multiple operations:

.. code-block:: python

    from litp.migration import BaseMigration
    from litp.migration.operations import AddProperty, RemoveProperty, RenameProperty

    class Migration(BaseMigration):
        version = '1.0.24'
        operations = [
            AddProperty('package', 'new_prop1', 'new _value'),
            RenameProperty('package', 'old_prop_name', 'new_prop_name'),
            RemoveProperty('package', 'old_prop1', 'default_value')
        ]


The "version" assigned above should be set to match the version of model extension in which
the change is required.

For example, in the package api model extension:

.. code-block:: bash

   [ERIClitppackageapi]# git pull
   [ERIClitppackageapi]# head pom.xml 
     <groupId>com.ericsson.nms.litp</groupId>
     <artifactId>ERIClitppackageapi</artifactId>
     <version>1.12.1-SNAPSHOT</version>

If you wanted to make a change to the current package model extension as shown
above, then the next released version would be '1.12.1'. This should be the
value set in the version variable in the Migration class in a migration script
which you should commit along with the change in the model extension.

The version variable in the Migration class in the migration script should be
synchronized with the model extension revision number delivering the new functionality.

Custom Operations
=================

If the changes required for a model migration are more complex than the
operations provided by core, it is possible to write custom model
migrations to achieve whatever changes are required to the model.

Custom operations extend the base Operation class and must implement
*mutate_forwards* and *mutate_backwards* methods. These mutate methods
are provided with a instance of the model manager with which they can find
and update items in the model.

Sample Custom Operations
------------------------

Below is an sample custom operation to merge two properties into one:

.. code-block:: python

   from litp.migration.operations import BaseOperation

   class MergePropertyOperation(BaseOperation):

       def __init__(self, item_type_id, old_property1, old_property2, new_property):
           self.item_type_id = item_type_id
           self.old_property1 = old_property1
           self.old_property2 = old_property2
           self.new_property = new_property

       def mutate_forward(self, model_manager):
           matched_items = model_manager.find_modelitems(self.item_type_id)
           for item in matched_items:
               if getattr(item, self.new_property) is None:
                   prop_value1 = getattr(item, self.old_property1, '')
                   prop_value2 = getattr(item, self.old_property2, '')
                   merged_value = "%s-%s" % (prop_value1, prop_value2)
                   item.delete_property(self.old_property1)
                   item.delete_property(self.old_property2)
                   model_manager.update_item(item.vpath, **{self.new_property: merged_value})

       def mutate_backward(self, model_manager):
           matched_items = model_manager.find_modelitems(self.item_type_id)
           for item in matched_items:
               if getattr(item, self.new_property) is not None:
                   merged_value = getattr(item, self.new_property)
                   prop_value1, prop_value2 = merged_value.split('-')
                   item.delete_property(self.new_property)
                   model_manager.update_item(item.vpath, **{self.old_property1: prop_value1})
                   model_manager.update_item(item.vpath, **{self.old_property2: prop_value2})

Below is an sample custom operation to split one property into two:

.. code-block:: python

   class SplitPropertyOperation(BaseOperation):

       def __init__(self, item_type_id, old_property, new_property1, new_property2):
           self.item_type_id = item_type_id
           self.old_property = old_property
           self.new_property1 = new_property1
           self.new_property2 = new_property2

       def mutate_forward(self, model_manager):
           matched_items = model_manager.find_modelitems(self.item_type_id)
           for item in matched_items:
               if getattr(item, self.old_property) is not None:
                   merged_value = getattr(item, self.old_property)
                   prop_value1, prop_value2 = merged_value.split('-')
                   item.delete_property(self.old_property)
                   model_manager.update_item(item.vpath, **{self.new_property1: prop_value1})
                   model_manager.update_item(item.vpath, **{self.new_property2: prop_value2})

       def mutate_backward(self, model_manager):
           matched_items = model_manager.find_modelitems(self.item_type_id)
           for item in matched_items:
               if (getattr(item, self.new_property1) is not None and
                   getattr(item, self.new_property2) is not None):
                   prop_value1 = getattr(item, self.new_property1, '')
                   prop_value2 = getattr(item, self.new_property2, '')
                   merged_value = "%s-%s" % (prop_value1, prop_value2)
                   item.delete_property(self.new_property1)
                   item.delete_property(self.new_property2)
                   model_manager.update_item(item.vpath, **{self.old_property: merged_value})

Below is a sample custom operation to move a property from an item to another:

.. code-block:: python

   class MovePropertyOperation(BaseOperation):

       def __init__(self, old_item_type_id, new_item_type_id, property_name):
           self.old_item_type_id = old_item_type_id
           self.new_item_type_id = new_item_type_id
           self.property_name = property_name

       def mutate_forward(self, model_manager):
           old_matched_items = model_manager.find_modelitems(self.old_item_type_id)
           new_matched_items = model_manager.find_modelitems(self.new_item_type_id)
           for old_item in old_matched_items:
               for new_item in new_matched_items:
                   if getattr(old_item, "name") is not None and \
                      getattr(old_item, "name") == getattr(new_item, "name"):
                       if getattr(old_item, self.property_name) is not None:
                           prop_value = getattr(old_item, self.property_name)
                           old_item.delete_property(self.property_name)
                           model_manager.update_item(new_item.vpath, **{self.property_name: prop_value})

       def mutate_backward(self, model_manager):
           old_matched_items = model_manager.find_modelitems(self.old_item_type_id)
           new_matched_items = model_manager.find_modelitems(self.new_item_type_id)
           for old_item in old_matched_items:
               for new_item in new_matched_items:
                   if getattr(old_item, "name") is not None and \
                      getattr(old_item, "name") == getattr(new_item, "name"):
                       if getattr(new_item, self.property_name) is not None:
                           prop_value = getattr(new_item, self.property_name)
                           new_item.delete_property(self.property_name)
                           model_manager.update_item(old_item.vpath, **{self.property_name: prop_value})
