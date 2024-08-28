.. currentmodule:: litp.core.extension

Methods to Implement in a Model Extension
=========================================

A Model Extension defines extra data required to perform a task. Not every
plugin needs a Model Extension. Some plugins harness the data already
available in the model and request LITP Core to perform new tasks based on
this existing data. An example of this is ERIClitphosts which adds host
entries for the node model items which are defined in the core extension.

.. _sample-extension:

Sample Model Extension
----------------------

A ``tar`` archive containing a sample Model Extension may be
downloaded :download:`here <../attachments/ERIClitpexampleapi.tar.gz>`

To build the sample Model Extension run the command 'mvn clean install'

Also, the source for LITP model extensions are available at :doc:`../extensions/index`.
Select a model extension and then follow the **[source]** link. These model extensions can
be helpful to use as a reference.

Defining Types
--------------

In addition to the core set of LITP Data model types, a Model Extension can define new item types by implementing method :func:`ModelExtension.define_item_types`.

1. Define the item types

  For example:

  .. code-block:: python
    :emphasize-lines: 3,4,10,11

      def define_item_types(self):
          return  [
              ItemType("package-list",
                  extend_item="software-item",
                  packages=Collection("package"),
                  name=Property("basic_string",
                      prop_description="Name of package collection.",
                      required=True
                ),
              ),
              ItemType("package",
                  extend_item="software-item",
                  item_description="A software package.",
                  name=Property("basic_string",
                      prop_description="Package name to install/remove",
                      required=True
                  ),
                  version=Property("package_version",
                      prop_description="Package version to install/remove",
                  ),
                  release=Property("any_string",
                      prop_description="Package release to install/remove",
                  ),
                  arch=Property("any_string",
                      prop_description="Package arch to install/remove",
                  ),
                  ensure=Property("package_ensure",
                      prop_description="Constraint for package enforcement",
                      default="installed",
                  ),
                  config=Property("package_config",
                      prop_description="Constraint for configuration retention",
                  ),
                  repository=Property("any_string",
                      prop_description="Name of repository to get Package",
                  )
              )
          ]


  .. note::
     The 'extend_item' value as highlighted above, is a pre-defined item type,
     by extending an item type we inherit any of its properties and structure.
     Also, the extension of 'software-item' allows our new item type to be added
     to the model at any point which allows an item of extended type. For example,
     the a 'package' item can now be created at the path '/software/items/package1'.

  .. note::
     An appropriate description should be provided for all defined item types and
     properties, as these descriptions are used to generate documentation.

  The model extension above would allow the following items to be created in the model:

  .. code-block:: bash

     # Create a vim 'package-list' containing multiple packages
     litp create -t package-list -p /software/items/vim_pkgs -o name='vim_pkgs'
     litp create -t package      -p /software/items/vim_pkgs/packages/pkg1 -o name='vim-minimal' version='7.2'
     litp create -t package      -p /software/items/vim_pkgs/packages/pkg2 -o name='vim-enhanced' version='7.2'

     # Create a standalone emacs 'package' model item
     litp create -t package      -p /software/items/emacs_pkg -o name='emacs' version='23.1'


2. Define additional property types if required.

  In addition to the core set of LITP property types, a Model Extension can
  define new property types by implementing method
  :func:`ModelExtension.define_property_types`.

  For example:

  .. code-block:: python

      def define_property_types(self):
          return[
              PropertyType(
                  "package_version",
                  regex="^[a-zA-Z0-9\.\-_s]+$"),
              PropertyType(
                  "package_ensure",
                  regex=("^(installed)|(present)|(absent)|"
                         "(latest)|(purged)|(held)$")),
              PropertyType(
                  "package_config",
                  regex="'^(keep)|(replace)$"),
          ]

.. seealso::

   :ref:`base-extension-class` in the :doc:`../plugin_api/index`
     For more information on the Model Extension API

   :doc:`../item_types/index`
     For the complete set of defined item types

   :doc:`../property_types/index`
     For the complete set of property types

Logging
-------
LITP provides a logging subsystem which can be used for logging in a
model extension, more information on this is available in the
:ref:`logging` section of the *LITP Plugin API Documentation*.

Testing your Model Extension
-----------------------------
As part of creating a Model Extension from the maven archetype, a
test directory is created which contains some basic unit tests.
All unit-tests are executed as part of the maven build process and
can be run using the *mvn test* command.

Below is an example unit-test file for a Model Extension (ERIClitpexampleapi/test/test_example_extension.py):

.. code-block:: python
    :emphasize-lines: 13,19

    import unittest
    from example_extension.exampleextension import ExampleExtension

    class TestExampleExtension(unittest.TestCase):

        def setUp(self):
            self.ext = ExampleExtension()

        def test_property_types_registered(self):
            prop_types_expected = ['property_type1',]
            prop_types = [pt.property_type_id for pt in
                          self.ext.define_property_types()]
            self.assertEquals(prop_types_expected, prop_types)

        def test_item_types_registered(self):
            item_types_expected = ['example-item-type1',]
            item_types = [it.item_type_id for it in
                          self.ext.define_item_types()]
            self.assertEquals(item_types_expected, item_types)

    if __name__ == '__main__':
        unittest.main()

.. note::
    Code coverage statistics are output as part of running the tests
    and it is strongly recommended a that code coverage is above a 85% threshold.

In addition to unit-testing, there is a LITP Accelerated Test utility available. For
more information see: :doc:`plugin_testing`.


Changing a Model Extension
--------------------------

Making changes to model extensions, requires the migration of existing model
items to be inline with the new item types.

How to include model migrations scripts and the procedures in how the data
will be migrated are outlined in :doc:`model_migration`
