.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. currentmodule:: litp.core.plugin

.. _methods_to_implement_in_a_plugin:

Methods to Implement in a Plugin
================================

The role of a plugin is to create tasks to perform configuration. To do this, it can inspect the deployment model. 
Based on the state of relevant model items, it can then generate tasks to perform the appropriate 
configuration activities. For example,  if the state of an item is set
to ``ForRemoval``, the plugin will create a task that will instruct Puppet
to remove that item.

To provide a list of tasks to the Execution Manager, you must
(at a minimum) implement the :func:`Plugin.create_configuration` method in the
plugin. 

.. note::
    A single task can affect the state of more than one model item.  (See: :ref:`task-multiple-model-items`)

This process is described in the following sections.

If the role of a plugin is to create lock and unlock tasks for a given node, it
has to implement the :func:`Plugin.create_lock_tasks` method.

.. _sample-plugin:

Sample Plugin
-------------

A ``tar`` archive containing an sample plugin may be downloaded
from :download:`here <../attachments/ERIClitpexample.tar.gz>`.

This plugin installs example-conf files in the /tmp directory of the node. To install an example-conf file, complete
the following steps: 

* Download and unpack the sample plugin and extension
* Build the sample plugin and extension
    - mvn clean install
* Install the newly built RPMs
* Create an example-conf item
    - litp create -t example-conf -p /software/items/test -o name=test.conf
    - litp inherit -p /deployments/site1/clusters/cluster1/nodes/node1/items/test -s /software/items/test
    - litp inherit -p /deployments/site1/clusters/cluster1/nodes/node2/items/test -s /software/items/test
* Create and run a plan
    - litp create_plan
    - litp run_plan
* The example-conf file is installed following successful completion of the plan.

.. note::
  The sample Plugin is dependent on the sample Model Extension so that must be downloaded and built first using 'mvn clean install' . 
  The sample Model Extension is available :download:`here <../attachments/ERIClitpexampleapi.tar.gz>`

Also, the source for LITP plugins are available at :doc:`../plugins/index`.
Select a plugin and then follow the **[source]** link. These plugins can
be helpful to use as a reference.

Access Data From within the Plugin
----------------------------------

Use the :func:`litp.core.plugin_context_api.PluginApiContext.query` method to
return a list of :class:`litp.core.model_manager.QueryItem` objects that match
specified criteria for use in the plugin's task generation logic.

When the Deployment Manager calls the :func:`Plugin.create_configuration`
method on a plugin, it passes parameter ``plugin_api_context`` to the plugin,
which can be used to query the Deployment Model:

.. code-block:: python
  :emphasize-lines: 7

    def create_configuration(self, plugin_api_context):
        """
        Provides support for the addition, update and
        removal of 'package'.
        """
        tasks = []
        nodes = plugin_api_context.query(item_type="node")
        ms_nodes = plugin_api_context.query(item_type="ms")

        all_nodes = nodes + ms_nodes

        ...

The plugin's :func:`Plugin.create_configuration` method can access structural
elements of the :class:`QueryItem` objects returned by
:func:`litp.core.plugin_context_api.PluginApiContext.query` using the dot
notation:

.. code-block:: python
  :emphasize-lines: 3

  matches = plugin_api_context.query(item_type="package")
  for item in matches:
      if "foo" == item.description:
          break


These objects also have a common set of utility methods that the plugin's
:py:meth:`Plugin.create_configuration` implementation can use to check the state
of the model item:

.. currentmodule:: litp.core.model_manager

.. py:method:: QueryItem.is_initial()
   :noindex:

.. py:method:: QueryItem.is_updated()
   :noindex:

.. py:method:: QueryItem.is_applied()
   :noindex:

.. py:method:: QueryItem.is_for_removal()
   :noindex:

.. py:method:: QueryItem.get_state()
   :noindex:

.. py:method:: QueryItem.get_source()
   :noindex:

.. note::
  These methods are public methods provided by the core to allow plugins to
  query the status of an item in the model. They are used by plugins, not
  implemented by them.


.. currentmodule:: litp.core.model_manager

These methods should be used to inspect relevant items and create tasks depending 
on the state of the item. For the state lifecycle of model items, please refer to
:ref:`state-diagram`. If a Plugin wants to react to a model item being added to
the model (:py:meth:`QueryItem.is_initial`) or an item's properties being updated 
(:py:meth:`QueryItem.is_updated`), it is the responsibility of the plugin to create 
one or more appropriate tasks to be added to the next plan. :py:meth:`QueryItem.is_applied`
signals that the item in that state has had its configuration applied by the configuration
manager (ie. Puppet) in one of the previous plan runs.

If an item is removed from the model, it will be in the ``ForRemoval`` state
(:py:meth:`QueryItem.is_for_removal`) until the next plan is run. If a Plugin wants to remove 
that item's configuration (eg. by removing a config file from a node), then the plugin 
needs to create a task (eg. :py:class:`litp.core.task.ConfigTask` using Puppet resource 
`file <http://docs.puppetlabs.com/references/3.stable/type.html#file>`__ |external|) that
will enforce the file's absence on the target node.

There isn't a comprehensive or extensive "history" of changes retained. Only
the current property values along with the previously applied values are
available to a Plugin as data dictionaries :py:attr:`QueryItem.properties` and
:py:attr:`QueryItem.applied_properties`, respectively. 

It is important to note that some properties may be non-configuration properties.
A property should be marked as non-configuration if it does not directly affect system
configuration and, therefore, a deployment Plan will not use it. 
In these cases, the behaviour of the item will be as follows:

* An item in ``Applied`` state will stay in ``Applied`` state only if a change
  to a non-configuration property is made. Both the item attribute and
  `item.applied_properties[property_name]` are updated at the same time, so there is no 
  item delta discernible in :py:meth:`Plugin.create_configuration` or 
  :py:meth:`Plugin.validate_model` methods.
* An item in ``Applied`` state will transition to ``Updated`` if a change
  to a non-configuration property is made along with a change to a configuration property.
* An inherited item in ``ForRemoval`` state will transition to ``Applied`` if a
  non-configuration property is changed in the source item.
* An inherited item in ``ForRemoval`` state will transition to ``Updated`` if a change to a
  non-configuration property is made along with a change to a configuration property.

As an example, let's consider a Plugin which uses a ``UserProfile`` ItemType
that has a ``username`` Property. An item instance is created with a Property
value of ``bob`` and that item is successfully applied by the configuration
manager during a plan run. If the ``username`` Property on that item is later
changed to ``Robert``, the Plugin can detect the change by checking for items
of type ``UserProfile`` that are in the ``Updated`` state and react by creating
one or more task that will effect the configuration changes needed to reflect
the property value change.

The precise delta between previous and current values of the item can be
determined by comparing the :py:attr:`QueryItem.properties` and
:py:attr:`QueryItem.applied_properties` attributes on that ``UserProfile``
:py:class:`QueryItem`.

The configuration of a peer server (which is driven by a model item) 
cannot be determined by LITP if :py:attr:`QueryItem.applied_properties_determinable` 
is set to ``False``. In this case, plugins must generate tasks using 
all properties of that model item.
You cannot update an item which is in ForRemoval state if 
its QueryItem.applied_properties_determinable flag is set to False.

The :py:meth:`QueryItem.query` method allows a query to be performed on child
items of a :class:`QueryItem` in the Deployment Model:
 
.. code-block:: python

    plugin_api_context.query(item_type="infrastructure")[0].query("storage-profile")

.. note::
   Just like :py:meth:`litp.core.plugin_context_api.PluginApiContext.query`, :py:meth:`QueryItem.query` queries the model for items which match specified criteria, but only for child items of the QueryItem and a list of :py:class:`QueryItem` objects is returned.

.. seealso::

    :ref:`accessing-the-deployment-model` in the :doc:`../plugin_api/index`
     For more information on the Plugin Context API and Query Items

.. _types-of-tasks:

Types of Tasks
--------------

A plugin can return 3 different types of tasks:

1. **Configuration Task** - Config Tasks are the most common and preferred mechanism
   within LITP for a plugin to affect system changes. Used to construct configuration
   for the Puppet master running on the MS, which is pushed to Puppet agents on the
   nodes, these agents both configure the nodes and subsequently enforce that they
   maintain that configuration. For more information see :ref:`config-tasks`.

   Config Tasks may use (i) a 3PP Puppet module, (ii) a bespoke Puppet module written
   for and included with a plugin, or (iii) use pre-defined puppet resource types
   such package or service (for a list of built-in puppet resource
   types see: https://docs.puppetlabs.com/references/latest/type.html |external| )

   An example of a Config Task is in the :ref:`sample-plugin`.

   Example Config Task:

.. code-block:: python
  :emphasize-lines: 8

    def create_configuration(self, plugin_api_context):
        tasks = []

        for node in plugin_api_context.query(item_type="node"):
            packages = node.query(item_type="package")
            for package in packages:
                if package.is_initial():
                    tasks.append(ConfigTask(node, package,
                        'Install package "%s" on node "%s"' % \
                            (package.name, node.hostname),
                         "package", package.name, # call_type, call_id
                         ensure="installed",
                         name=package.name,
                         version=package.version))

        return tasks

2. **Callback Task** - A Callback task is an action that is executed on the plugin, which
   is called by the execution manager during plan execution. Callback tasks are used
   typically where there is no Puppet or MCO agent available on the target system,
   For example: ssh commands / network calls  or calls to a remote SAN to create block
   storage. A Callback task reports failure or success to the execution manager by
   raising exceptions. For more information see :ref:`callback-tasks`.

   The :doc:`../plugins/ipmi_plugin_plugin/index` is a good example plugin which uses
   callback tasks to PXE boot nodes.

   An example of a Callback Task is in the :ref:`sample-plugin`.

   Example Callback Task:

.. code-block:: python
  :emphasize-lines: 5

    def create_configuration(self, plugin_api_context):
        san = plugin_api_context.query("san")[0]
        return [ # Constructed in a similar fashion to a ConfigTask. 
                 # But execution calls the specified method on the plugin with specified properties
                 CallbackTask(
                        san, "Configure SAN '{0}'".format(san.name),
                        self.cb_configure_san,
                        san.name,
                        san.ipaddress)
               ]

    def cb_configure_san(self, callback_api, name, ip):
         san_name = name
         san_ip = ip
         ...  # Configure SAN with provided properties


3. **Remote Execution Task** - Remote Execution Tasks  are used when you want to trigger
   non-configuration actions on a set of nodes in parallel e.g. for systems administration
   tasks across clusters of servers, such as snapshotting, checking the state of nodes, or VCS config.
   Remote Execution Tasks request actions from MCollective (MCO) agents on each node. A plugin
   developer can use one of the existing MCollective agents, or define their own agent (and
   include in their plugin) to do its particular orchestration. Existing agents allow actions
   such as ping, package install, execute commands on a node. As with Puppet modules, there are
   other open source MCO agents available. For more information see :ref:`remote-execution-tasks`.

   Example Remote Execution Task:

.. code-block:: python
  :emphasize-lines: 6

    def create_configuration(self, api):
        for node in api.query('node'):
            service = api.query("service")[0]
        return [ # Constructed in a similar fashion to all Tasks.
                 # But execution of the task calls the mco resource agent with the provided arguments
                 RemoteExecutionTask(
                    [node], service,
                    "Check status of a service {0}".format(service.name),
                    "service", "status", service="service.name")
               ]

.. currentmodule:: litp.core.plugin

Creating Tasks
--------------

To begin creating tasks, implement the :meth:`Plugin.create_configuration`
method in the plugin.

The :func:`Plugin.create_configuration` method is the only method needed for
a plugin to generate LITP tasks and is run on every plan creation. However
if a Model Extension defines new data types, validation may be required in a
:func:`Plugin.validate_model` method.

The :func:`Plugin.create_configuration` method will return a list of tasks for
execution by the LITP Execution Manager. The order of tasks in this list is not
significant, although the plugin can enforce the order of tasks by either
adding another :class:`~litp.core.task.Task` to the
:attr:`~litp.core.task.Task.requires` attribute of a given task or inserting
them in :class:`~litp.core.task.OrderedTaskList` objects in the order in which
you want them executed.  

:class:`~litp.core.task.OrderedTaskList` will be internally
transformed into a chain of tasks with :attr:`Task.requires` set to contain
the next task. (See :ref:`task-dependencies` and :ref:`setting-dependencies-tasks`).

To manage resources, you must create :class:`~litp.core.task.ConfigTask`
objects on a per-node basis for each Puppet resource that needs to be managed
(created, updated, removed) by the plugin.

Certain items may not lend themselves to having their own task. You can set up
a task to update items other than the primary one upon the task's success.
(see :ref:`task-multiple-model-items`)

To perform operations that are transient by nature, you can
create :class:`~litp.core.task.RemoteExecutionTask` objects that make use of
accompanying MCollective agents that are copied onto nodes. (See
:ref:`remote-execution-tasks`). Alternatively, you can use
:class:`~litp.core.task.CallbackTask` objects to allow your own Python code to
be run when the task is executed.

The Puppet Manager will manage and execute the
:class:`~litp.core.task.ConfigTask` objects given by a Plugin.  Only the most
recent Puppet resource, will be persisted in the generated puppet
manifests.

If a :class:`~litp.core.task.ConfigTask` refers to a previously applied resource (by
specifying the same ``call_type`` and ``call_id``) in an update, then the old manifest
entry is overwritten.

You can also optionally configure a :class:`~litp.core.task.ConfigTask` to replace
arbitrary resources previously applied on the same node by adding one or more
``(call_type, call_id)`` to the task's ``replaces`` set attribute. (See :ref:`config-tasks`)


.. code-block:: python
  :emphasize-lines: 6,9,11,14,16

    def create_configuration(self, plugin_api_context):
        """
        Provides support for the addition, update and
        removal of 'package'.
        """
        tasks = []
        nodes = plugin_api_context.query(item_type="node") + \
                plugin_api_context.query(item_type="ms")

        for node in nodes:
            packages = node.query(item_type="package")
            for package in packages:
                if package.is_initial() or package.is_updated():
                    self._add_package_task(node, package, tasks)
                elif package.is_for_removal():
                    self._add_removal_package_task(node, package, tasks)

        return tasks

    def _add_package_task(self, node, package, tasks):
        tasks.append(ConfigTask(node, package,
                     'Install package "%s" on node "%s"' % \
                                     (package.name, node.hostname),
                     "package", package.name,  # call_type, call_id
                     ensure="installed",
                     name=package.name,
                     version=package.version))

    def _add_removal_package_task(self, node, package, tasks):
        tasks.append(ConfigTask(node, package,
                     'Removing package "%s" from node "%s"' % \
                                     (package.name, node.hostname),
                     "package", package.name,
                     ensure="absent",
                     name=package.name))


.. note::
   In the example above, task generation is delegated to private methods such
   as `_add_package_task()`. This is at the Developer's discretion.

.. note::
   The name of the parameter ``plugin_api_context`` is not fixed and can be changed.

.. seealso::

   An example of a Config/Callback Tasks is in the :ref:`sample-plugin`.
   :ref:`base-plugin-class` in the :doc:`../plugin_api/index`
   For more information on the Plugin API

Defining a Custom Puppet Resource
---------------------------------

A Puppet resource is called by a Config Task within the plugin.

Below is an example of a simple puppet manifest from the sample plugin:

.. code-block:: bash

    # Puppet Manifest file for example plugin
    define test_example::test_example(
         $filename,
         $file_ensure
    )
    {

        file {"/tmp/${filename}":
          ensure => $file_ensure,
          owner => nobody,
          group => nobody,
        }
    }

Below is an example of a Config Task from the :ref:`sample-plugin` 
calling the Puppet resource defined above:

.. code-block:: python
     :emphasize-lines: 1,6,8,9

      ConfigTask(
            node,
            package,
            'Install %s on node %s' \
             % (package.name, node.hostname),
            "test_example::test_example",
            call_id=str(package.item_id),
            filename=str(package.name),
            file_ensure="present"
            )


Creating MCO Callback Tasks
---------------------------
 
The MCollective Simple RPC framework provides a straightforward means for 
extending MCollective functionality for custom tasks. It separates the 
description of the API (in .ddl files) and the implementation (in .rb files). 
MCollective is written in Ruby.

An example of a MCO Callback Task is in the :ref:`sample-plugin`.

Below is an example of a simple ddl file for an MCollective agent:

.. code-block:: ruby

    metadata    :name        => "example",
            :description => "API for an example cli commands",
            :author      => "User < User@ericsson.com>",
            :license     => "Ericsson",
            :version     => "1.0",
            :url         => "http://ericsson.com",
            :timeout     => 10

    action "check_dir_exists", :description => "Checks if a directory has been created" do
      display :always

    input  :path,
           :prompt      => "Path",
           :description => "The path to be checked",
           :type        => :string,
           :validation  => '^((?:[a-zA-Z]\:){0,1}(?:[\\/][\w.-]+){1,})$',
           :optional    => false,
           :maxlength   => 100

    output :retcode,
           :description => "The exit code from running the command",
           :display_as => "Result code"
    output :out,
           :description => "The stdout from running the command",
           :display_as => "out"
    output :err,
           :description => "The stderr from running the command",
           :display_as => "err"
    end

Below is an example MCollective .rb file for the ddl above:

.. code-block:: ruby

    require 'open3'
    def get_system_path
      res = %x[source /etc/profile;  facter | grep path]
      path =  res.split("=>").last
      return path
    end

    module MCollective
      module Agent
        class Example<RPC::Agent

          action "check_dir_exists" do
            path = request[:path]

            cmd = %{if [ -d } + path + %{ ]; then echo yes; else echo no; fi}
            reply[:retcode] = run("#{cmd}",
                             :stdout => :out,
                             :stderr => :err,
                             :chomp => true,
                             :environment => {"PATH" => get_system_path})
         end
       end
     end
    end

**Invoking MCO actions on the command line**

If you want to test an MCollective command on the command line, you can do the following:
 - Copy the .ddl and .rb files to /opt/ericsson/nms/litp/etc/mcollective/mcollective/agent/
   on the MS and to /opt/mcollective/mcollective/agent on the nodes.
 - Restart mcollective daemon by running the following command as root user on the MS and relevant nodes:
              - service mcollective restart
 - Or reload the agents by running the following command as root user on the MS and relevant nodes:
              - service mcollective reload-agents

Calling mco action from the command line with json formatted response:

.. code-block:: bash

    $ mco rpc example check_dir_exists path="/tmp" -I node1 --json

The output from the mco action is:

.. code-block:: bash

     [
      {
        "statusmsg": "OK",
        "action": "check_dir_exists",
        "data": {
          "out": "yes",
          "retcode": 0,
          "err": ""
        },
        "statuscode": 0,
        "sender": "node1",
        "agent": "example"
      }
    ]

Example Callback Task using the MCO agent from above:

.. code-block:: python

    def create_callback_task(self, model_item, dir_name, node_hostnames):
       return CallbackTask(model_item,
                           "Checking file exists",
                           self.check_dir_exist,
                           dir_name,
                           node_hostnames)
                

    def check_dir_exists(self, callback_api, dir_name, node_hostnames):
        args = dict()
        args["dir_name"] = dir_name
        results = callback_api.rpc_command(node_hostnames, "example", 'check_dir_exists', args) 

**MCO Unit Tests**

If you want to write unit tests for your MCO agent, checkout the :ref:`sample-plugin`.

.. note::
    To deliver the agent files with your plugin, store the files in the following directory within the plugin: puppet/mcollective_agents/files

Creating Snapshot Callback Tasks
--------------------------------

A plugin can provide Callback tasks to create, remove or restore snapshots. For more detail on how to do this, see :ref:`plugin_snapshot_api`


.. _setting-dependencies-tasks:

Setting Dependencies between Tasks
----------------------------------

Each task has a ``requires`` attribute which is a set storing multiple dependencies.

A task can require all tasks with a particular model_item by adding an instance
of :class:`QueryItem` corresponding to that model_item

Secondly, a task can require a :class:`~litp.core.task.ConfigTask` by
specifying a tuple with call_type and call_id. If there is any matching task
created by the same plugin it will be set as a dependency.

Thirdly, a task can require another task created within same plugin by
adding a reference to that task to its ``requires`` set.

.. code-block:: python
  :emphasize-lines: 13, 16, 19

    def create_configuration(self, plugin_api_context):
        ms = plugin_api_context.query("ms")[0]
        infr = plugin_api_context.query("infrastructure")[0]

        task1 = ConfigTask(ms, ms.items, 'Example task 1',
                           'example_call_type1', 'example_call_id1')
        task2 = ConfigTask(ms, ms.items, 'Example task 2',
                           'example_call_type2', 'example_call_id2')
        task3 = ConfigTask(ms, infr, 'Example task 3',
                           'example_call_type3', 'example_call_id3')

        # Task1 requires all Tasks associated with the ms.services model item (QueryItem dependency)
        task1.requires.add(ms.services)

        # Task 2 requires another ConfigTask (Task) by providing the call_type and type_id (ConfigTask dependency)
        task2.requires.add (('example_call_type1', 'example_call_id1'))

        # Task 3 requires Task 2 (direct 'task-to-task' dependency)
        task3.requires.add(task2)

        return [task1, task2, task3]

.. note::
    In the example above task1 will have a dependency on tasks
    created by any plugin which are associated with the 'ms.services' model item.
    Also, task2 will have a dependency on task1 while task3 will have a dependency on task2.

.. warning::
    If the plugin provides a set of tasks with a set of dependencies between
    them, and if you want to update those dependencies in a way which conflicts
    with the previous set, you must provide the full set of tasks with an
    updated set of dependencies.

.. warning::
    You must not set dependencies between configuration and deconfiguration 
    tasks (ConfigTasks and/or CallbackTasks). LITP treats
    these dependencies as deprecated and removes them from the plan.

.. _task-multiple-model-items:

Updating Multiple Model Items Using a Single Task
-------------------------------------------------

Each task has a property (:py:attr:`Task.model_items`) which is a set of model
items, the states of which the plugin developer intends to be updated upon the task's
successful completion.

A task can have multiple model items specified this way and a single model item
can be updatable by more than one task.

Only successful completion of all tasks attached to a model item will result in
a change of state of that model item.

Model items referenced in `Task.model_items` property do not affect the order of
the task in topological sort.

.. code-block:: python

    def create_configuration(self, plugin_api_context):
        ms = plugin_api_context.query("ms")[0]
        infr = plugin_api_context.query("infrastructure")[0]

        task1 = ConfigTask(ms, ms, 'Example task 1', 'example_call_type1',
                        'example_call_id1')

        task1.model_items.add(infr)
        return [task1]

.. note::
    In the example above task1 is set to update both ``ms`` and
    ``infrastructure`` model items upon successful execution as long as all
    the tasks these model items are attached to are successful.

Modifying Model Items before Plan Creation
------------------------------------------

Plugins should not directly modify items in the model, but should examine
the model and generate appropriate tasks. Extending the model with properties
that are updated by a plugin indicates that the internal logic is exposed to
an external interface. This can have repercussions for the maintainability
and extensibility of the model.

However, there are situations when it becomes necessary for a plugin to directly
modify the model. For example, when the timestamp of a file or a checksum
of its contents must be calculated and stored in an item property. In these
circumstances, the plugin author can implement the :func:`Plugin.update_model`
method in the plugin.

This method is called before the :func:`Plugin.validate_model` method and is passed
a ``plugin_api_context`` parameter which can be used to query the Deployment Model.
The :func:`litp.core.plugin_context_api.PluginApiContext.query` method will
return a list of :class:`litp.core.model_manager.QueryItem` objects, and the
properties of those objects may be modified.  This will only work for properties
which are defined with ``updatable_plugin=True`` when the ItemType is defined.

The ``create_plan`` command should never fail at this stage. If there is a
dependency on a resource external to the management server, any exception
should be handled gracefully and allow a plan to be created, even if that means
that a property can't be updated.  Any raised exceptions not handled by
the plugin terminate the ``create_plan`` command and return an
``InternalServerError`` to the client.

.. code-block:: python

    def update_model(self, plugin_api_context):
        node = plugin_api_context.query('node')[0]
        for test_item in node.query("test_item"):
            test_item.version = "X.Y.Z"

.. note::
    It is recommended that a plugin only update its own model extension items.

Logging
-------
LITP provides a logging subsystem which can be used for logging in a plugin,
more information on this is available in the :ref:`logging` section of
the *LITP Plugin API Documentation*.

Lock and Unlock Tasks
---------------------

The :func:`Plugin.create_lock_tasks` method will be called with a node argument for
all the nodes that need to be locked during plan. The method has to return a 2
item tuple of (lock_task, unlock_task). During running of the plan these tasks
will make sure that the node will be locked when it's necessary.

.. code-block:: python

    def create_lock_tasks(self, api, node):
        ms = api.query("ms")[0]
        return (
            RemoteExecutionTask([node], ms, "Lock %s" % node.item_id, "lock_unlock", "lock"),
            RemoteExecutionTask([node], ms, "Unlock %s" % node.item_id, "lock_unlock", "unlock"),
        )

.. _future-property-value-plugin:

Evaluating Property Values which are Updated During a Running Plan
------------------------------------------------------------------

The :class:`FuturePropertyValue` class allows for property values set during 
a running plan to be evaluated and used by tasks running in the same plan.

.. code-block:: python

    from litp.core.future_property_value import FuturePropertyValue

    class DummyPlugin(Plugin):

        def create_configuration(self, plugin_api_context):
            node_q = plugin_api_context.query("node")[0]
            future_property_value = \
                    FuturePropertyValue(node_q, "some_property")
            # Set value of 'some_property' property to 'future_value_property'
            return [ ConfigTask(node_q, node_q, "Future Property Task",
                            "call_type", "call_id",
                            some_property=future_property_value)]


The :class:`View` class can be used in conjunction with
:class:`FuturePropertyValue`. To demonstrate this, firstly define a
:class:`View` in an extension (along with its callable method), as shown below:

.. code-block:: python

    from litp.core.model_type import ItemType, View, Property

    def define_item_types(self):
        return [
            ItemType("some_item",
                some_property=Property("basic_string", updatable_plugin=True),
                future_view=View("basic_string",
                    callable_method=self.view_method))]

    @staticmethod
    def view_method(plugin_api_context, query_item):
        return "<prefix>" + query_item.some_property + "<suffix>"


Then make use of the View-backed FuturePropertyValue in a plugin:

.. code-block:: python

    from litp.core.future_property_value import FuturePropertyValue

    class DummyPlugin(Plugin):

        def create_configuration(self, plugin_api_context):
            node_q = plugin_api_context.query("node")[0]
            # Create a future property value which contains a View
            future_property_view = FuturePropertyValue(node_q, "future_view")
            future_property_value = \
                    FuturePropertyValue(node_q, "some_property")
            # Set value of 'future_view' property to 'future_value_view'
            return [ ConfigTask(node_q, node_q, "Future Property Task",
                            "call_type", "call_id",
                            some_property=future_property_value,
                            future_view=future_property_view)]

.. note::
  Property names used above are for example purposes only.

Unsetting a Property
--------------------

.. currentmodule:: litp.core.model_manager

To unset a property of a :class:`litp.core.model_manager.QueryItem` from
within a plugin, call its :py:meth:`QueryItem.clear_property` function passing
the property name as an argument:

.. code-block:: python

    query_item.clear_property(property_name)

This function is designed to behave the same as the ``litp update`` command using
the ``-d`` option:

.. code-block:: python

    litp update -p /path/to/item -d property_name

Further information on the :py:meth:`QueryItem.clear_property` function is
available here: :py:meth:`QueryItem.clear_property`

.. note::
  When :py:meth:`QueryItem.clear_property` is called on an inherited item and the required validation has been passed, the property value is reverted to that of its source. If the property does not exist on the source, it is deleted. This is consistent with the ``litp update`` command using the ``-d`` option.
