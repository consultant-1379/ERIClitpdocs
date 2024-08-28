##############################################################################
# COPYRIGHT Ericsson AB 2016
#
# The copyright to the computer program(s) herein is the property of
# Ericsson AB. The programs may be used and/or copied only with written
# permission from Ericsson AB. or in accordance with the terms and
# conditions stipulated in the agreement/contract under which the
# program(s) have been supplied.
##############################################################################

import unittest

from litp.extensions.core_extension import CoreExtension
from litp.core.model_manager import ModelManager, QueryItem
from litp.core.plugin_manager import PluginManager
from litp.core.model_type import ItemType, Child
from litp.core.validators import ValidationError
from litp.core.model_item import ModelItem
from litp.core.plugin_context_api import PluginApiContext

from example_plugin.example_plugin import ExamplePlugin
from example_extension.example_extension import ExampleExtension


class TestExamplePlugin(unittest.TestCase):

    def setUp(self):
        """
        Construct a model, sufficient for test cases
        that you wish to implement in this suite.
        """
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

        # Instantiate your plugin and register with PluginManager
        self.plugin = ExamplePlugin()

    def setup_base_model(self):
        # Use create_item to build up the required model
        self.model.create_item('deployment', '/deployments/d1')
        self.model.create_item('cluster', '/deployments/d1/clusters/c1')

        self.node1 = self.model.create_item("node",
            '/deployments/d1/clusters/c1/nodes/node1',
            hostname="node1")
        self.assertEqual(ModelItem, type(self.node1))
        self.node2 = self.model.create_item("node",
            '/deployments/d1/clusters/c1/nodes/node2',
            hostname="node2")
        self.assertEqual(ModelItem, type(self.node2))

    def setup_model_with_example_item(self):
        self.setup_base_model()
        # Create the required model items to test the plugin
        self.item1 = self.model.create_item("example-conf",
                                            '/software/items/example1',
                                            name="test.conf")
        self.assertEqual(ModelItem, type(self.item1))
        self.model.create_inherited("/software/items/example1",
            "/deployments/d1/clusters/c1/nodes/node1/items/item1")
        self.model.create_inherited("/software/items/example1",
            "/deployments/d1/clusters/c1/nodes/node2/items/item1")

    def test_validate_model_no_errors_with_no_model(self):
        errors = self.plugin.validate_model(self.context)
        self.assertEqual(0, len(errors))

    def test_validate_model_no_errors_with_valid_model(self):
        self.setup_model_with_example_item()
        errors = self.plugin.validate_model(self.context)
        self.assertEqual(0, len(errors))

    def test_create_configuration_valid_model_tasks(self):
        self.setup_model_with_example_item()
        tasks = self.plugin.create_configuration(self.context)
        self.assertEqual(4, len(tasks))
        task = tasks[0]
        # Assert the task is as expected
        self.assertEqual("/deployments/d1/clusters/c1/nodes/node1/items/item1",
                         task.model_item.get_vpath())
        self.assertEqual('Install test.conf on node node1',
                         task.description)
        self.assertEqual("test_example::test_example", task.call_type)
        self.assertEqual("item1", task.call_id)
        self.assertEqual({'file_ensure': 'present',
                          "filename": 'test.conf'}, task.kwargs)

    def test_create_configuration_all_applied_no_tasks(self):
        self.setup_model_with_example_item()
        self.model.set_all_applied()
        tasks = self.plugin.create_configuration(self.context)
        self.assertEqual(0, len(tasks))

    def test_create_configuration_valid_model_update_tasks(self):
        self.setup_model_with_example_item()
        self.model.set_all_applied()
        self.model.update_item("/deployments/d1/clusters/c1/nodes/node1/items/"
                               "item1",
            name="test1.conf")
        tasks = self.plugin.create_configuration(self.context)
        self.assertEqual(2, len(tasks))
        task = tasks[0]
        # Assert the task is as expected
        self.assertEqual("/deployments/d1/clusters/c1/nodes/node1/items/item1",
                         task.model_item.get_vpath())
        self.assertEqual('Install test1.conf on node node1',
                         task.description)
        self.assertEqual("test_example::test_example", task.call_type)
        self.assertEqual("item1", task.call_id)
        self.assertEqual({'file_ensure': 'present',
                          "filename": 'test1.conf'}, task.kwargs)

    def test_create_configuration_valid_model_removal_tasks(self):
        self.setup_model_with_example_item()
        self.model.set_all_applied()
        self.model.remove_item("/deployments/d1/clusters/c1/nodes/node1/"
                               "items/item1")
        tasks = self.plugin.create_configuration(self.context)
        self.assertEqual(1, len(tasks))
        task = tasks[0]
        # Assert the task is as expected
        self.assertEqual("/deployments/d1/clusters/c1/nodes/node1/items/item1",
                         task.model_item.get_vpath())
        self.assertEqual('Remove test.conf on node node1',
                         task.description)
        self.assertEqual("test_example::test_example", task.call_type)
        self.assertEqual("item1", task.call_id)
        self.assertEqual({"filename": 'test.conf',
                          "file_ensure": "absent"}, task.kwargs)
