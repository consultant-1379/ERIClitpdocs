.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">



Testing Your Plugin
===================

It is recommended that you use both of the following test types to test your plugin:
            -  Unit tests
            -  Accelerated tests (ATs)

Unit Testing Your Plugin
===========================
As part of creating a plugin from the Maven archetype, a
test directory is created which contains some basic unit tests.
All unit tests are executed as part of the maven build process and
you can run them using the  ``mvn test`` command.

Below is an example unit test file for a plugin (ERIClitpexample/test/test_example_plugin/test_example.py):

.. code-block:: python
    :emphasize-lines: 43, 53, 68, 72, 77, 81, 86, 97, 103, 111, 122, 129

    # import model extension and plugin
    from example_extension.exampleextension import ExampleExtension
    from example_plugin.exampleplugin import ExamplePlugin

    # import other core components
    from litp.extensions.core_extension import CoreExtension
    from litp.core.model_manager import ModelManager
    from litp.core.plugin_manager import PluginManager
    from litp.core.model_type import ItemType, Child
    from litp.core.model_item import ModelItem
    from litp.core.plugin_context_api import PluginApiContext

    import unittest


    class TestExamplePlugin(unittest.TestCase):

        def setUp(self):
            # Instantiate a model manager adding model extension item types
            self.model = ModelManager()
            self.plugin_manager = PluginManager(self.model)
            # Instantiate a plugin API context to pass to the plugin
            self.context = PluginApiContext(self.model)

            # Add the Core Property Types
            self.plugin_manager.add_property_types(
                CoreExtension().define_property_types())
            # Add the Core Item Types
            self.plugin_manager.add_item_types(
                CoreExtension().define_item_types())

            # Add your model extension Property Types
            self.plugin_manager.add_property_types(
                ExampleExtension().define_property_types())
            # Add your model extension Item Types
            self.plugin_manager.add_item_types(
                ExampleExtension().define_item_types())

            # Add default minimal model (which creates '/' root item)
            self.plugin_manager.add_default_model()

            # Instantiate your plugin
            self.plugin = ExamplePlugin()

        def setup_base_model(self):
            # Use create_item to build up the required model
            self.model.create_item('deployment', '/deployments/d1')
            self.model.create_item('cluster', '/deployments/d1/clusters/c1')
            self.node1 = self.model.create_item("node",
                '/deployments/d1/clusters/c1/nodes/n1',
                hostname="node1")
            self.assertEqual(ModelItem, type(self.node1))

        def setup_model_with_example_item(self):
            self.setup_base_model()
            # Create the required model items to test the plugin
            self.item1 = self.model.create_item("example",
                                                '/software/items/example1',
                                                name="abc",
                                                directory="/def/")
            self.assertEqual(ModelItem, type(self.item1))
            self.model.create_inherit("/software/items/example1",
                "/deployments/d1/clusters/c1/nodes/n1/items/item1")

        def test_validate_model_no_errors_with_no_model(self):
            errors = self.plugin.validate_model(self.context)
            self.assertEqual(0, len(errors))

        def test_validate_model_no_errors_with_valid_model(self):
            self.setup_model_with_example_item()
            errors = self.plugin.validate_model(self.context)
            self.assertEqual(0, len(errors))

        def test_create_configuration_no_model_no_tasks(self):
            tasks = self.plugin.create_configuration(self.context)
            self.assertEqual(0, len(tasks))

        def test_create_configuration_valid_model_1_tasks(self):
            self.setup_model_with_example_item()
            tasks = self.plugin.create_configuration(self.context)
            self.assertEqual(1, len(tasks))
            task = tasks[0]
            # Assert the task is as expectedCc
            self.assertEqual("/deployments/d1/clusters/c1/nodes/n1/items/item1",
                             task.model_item.get_vpath())
            self.assertEqual('Configure abc on node "node1"',
                             task.description)
            self.assertEqual("example::config", task.call_type)
            self.assertEqual("item1", task.call_id)
            self.assertEqual({"name": "abc",
                              "directory": "/def/",
                              "ensure": "present"}, task.kwargs)

        def test_create_configuration_all_applied_no_tasks(self):
            self.setup_model_with_example_item()
            self.model.set_all_applied()
            tasks = self.plugin.create_configuration(self.context)
            self.assertEqual(0, len(tasks))

        def test_create_configuration_valid_model_update_tasks(self):
            self.setup_model_with_example_item()
            self.model.set_all_applied()
            self.model.update_item("/deployments/d1/clusters/c1/nodes/n1/items/item1", 
                directory="/ghi/")
            tasks = self.plugin.create_configuration(self.context)
            self.assertEqual(1, len(tasks))
            task = tasks[0]
            # Assert the task is as expected
            self.assertEqual("/deployments/d1/clusters/c1/nodes/n1/items/item1",
                             task.model_item.get_vpath())
            self.assertEqual('Configure abc on node "node1"',
                             task.description)
            self.assertEqual("example::config", task.call_type)
            self.assertEqual("item1", task.call_id)
            self.assertEqual({"name": "abc",
                              "directory": "/ghi/",
                              "ensure": "present"}, task.kwargs)

        def test_create_configuration_valid_model_removal_tasks(self):
            self.setup_model_with_example_item()
            self.model.set_all_applied()
            self.model.remove_item("/deployments/d1/clusters/c1/nodes/n1/items/item1")
            tasks = self.plugin.create_configuration(self.context)
            self.assertEqual(1, len(tasks))
            task = tasks[0]
            # Assert the task is as expected
            self.assertEqual("/deployments/d1/clusters/c1/nodes/n1/items/item1",
                             task.model_item.get_vpath())
            self.assertEqual('Remove abc on node "node1"',
                             task.description)
            self.assertEqual("example::config", task.call_type)
            self.assertEqual("item1", task.call_id)
            self.assertEqual({"name": "abc",
                              "directory": "/def/",
                              "ensure": "absent"}, task.kwargs)


.. note::
    Code coverage statistics are output as part of running the tests
    and it is strongly recommended that code coverage is above 85%.

LITP ATs (Accelerated Tests)
===========================

The LITP ATs  (`Accelerated Tests <https://arm1s11-eiffel004.eiffel.gic.ericsson.se:8443/nexus/content/sites/litp2/ERIClitpatrunner/latest/>`_ |external| ) provide a layer of testing in a level between
unit testing and integration testing. 

