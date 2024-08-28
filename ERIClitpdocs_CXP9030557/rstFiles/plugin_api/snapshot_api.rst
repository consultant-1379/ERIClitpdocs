.. _plugin_snapshot_api:

==================================
LITP |release| Plugin Snapshot API
==================================

This document details the APIs that are available to plugins to create, remove
or restore snapshots.  A plugin can provide Callback tasks to create, remove or
restore snapshots.  Tasks that are not Callback tasks are unsupported and will
be ignored during plan generation.

Using Tags to Order Snapshot Tasks
----------------------------------

Callback Tasks in a snapshot plan can provide a 'tag_name' which is used as an
identifier to assign the task to a given phase in the plan.
The task is then assigned to the appropriate phase based on a predefined
set of rules in the snapshot plan creation logic.

All valid tags are listed below in the order that tasks using them would
appear in a plan. The position of the default phase is also shown.

A task will be assigned to the default phase if:

- it does not have a tag.
- it has a tag that is not listed in the Valid Tags section below.

Valid Tags
**********

The tags for **create_snapshot** tasks are available for import
from ``litp.plan_types.create_snapshot.create_snapshot_tags``.
The following tags are valid for **create_snapshot** tasks in both a deployment 
snapshot plan and a named backup snapshot plan:

.. csv-table::
   :header: "Valid tags and default phase position", "Description"

   "VALIDATION_TAG", "All tasks generated to perform validation checks before
   the plan proceeds."
   "PRE_OPERATION_TAG" , "All tasks generated that need to execute before the
   snapshots are created."
   "LMS_LVM_VOLUME_TAG", "All tasks associated with MS LVM file-systems."
   "PEER_NODE_LVM_VOLUME_TAG", "All tasks associated with LVM file-systems on
   the peer nodes."
   "PEER_NODE_VXVM_VOLUME_TAG", "All tasks associated with VxVM
   file-systems on the peer nodes."
   "NAS_FILESYSTEM_TAG", "All tasks associated with NAS shared file-systems."
   "SAN_LUN_TAG", "All tasks associated with SAN LUNs."
   "``Default Phase``", "``Position of the default phase.``"
   "POST_OPERATION_TAG", "All tasks generated at the end of the snapshot
   sequence."

The tags for **remove_snapshot** tasks are available for import
from ``litp.plan_types.remove_snapshot.remove_snapshot_tags``.
The following tags are valid for **remove_snapshot** tasks in both a deployment
snapshot plan and a named backup snapshot plan.

.. csv-table::
   :header: "Valid tags and default phase position", "Description"

   "VALIDATION_TAG", "All tasks generated to perform validation checks before
   the plan proceeds."
   "PRE_OPERATION_TAG" , "All tasks generated that need to execute before the
   snapshots are removed."
   "LMS_LVM_VOLUME_TAG", "All tasks associated with MS LVM file-systems."
   "PEER_NODE_LVM_VOLUME_TAG", "All tasks associated with LVM
   file-systems on the peer nodes."
   "PEER_NODE_VXVM_VOLUME_TAG", "All tasks associated with VxVM
   file-systems on the peer nodes."
   "NAS_FILESYSTEM_TAG", "All tasks associated with NAS shared file-systems."
   "SAN_LUN_TAG", "All tasks associated with SAN LUNs."
   "``Default Phase``", "``Position of the default phase.``"
   "POST_OPERATION_TAG", "All tasks generated at the end of the snapshot
   sequence."

The tags for **restore_snapshot** tasks are available for import
from ``litp.plan_types.restore_snapshot.restore_snapshot_tags``.
The following tags are valid for **restore_snapshot** tasks in a
deployment snapshot plan only:

.. csv-table::
   :header: "Valid tags and default phase position", "Description"

   "VALIDATION_TAG", "All tasks generated to perform validation checks before
   the plan proceeds."
   "PREPARE_PUPPET_TAG", "All tasks associated with pre-restore Puppet
   operations."
   "PREPARE_VCS_TAG", "All tasks associated with pre-restore VCS operations."
   "PRE_OPERATION_TAG", "All tasks associated with pre-restore operations
   excluding Puppet and VCS."
   "NAS_FILESYSTEM_TAG","All tasks associated with NAS shared file-systems."
   "PEER_NODE_LVM_VOLUME_TAG","All tasks associated with LVM file-systems on
   the peer nodes."
   "PEER_NODE_VXVM_VOLUME_TAG","All tasks associated with VxVM file-systems on
   the peer nodes."
   "PEER_NODE_REBOOT_TAG","All tasks associated with the reboot of peer nodes."
   "PEER_NODE_POWER_OFF_TAG","All tasks associated with power off procedure."
   "SAN_LUN_TAG","All tasks associated with SAN LUNs."
   "SANITISATION_TAG","All tasks associated with a post-rollback cleanup."
   "PEER_NODE_POWER_ON_TAG","All tasks associated with power on procedure of
   peer nodes."
   "PEER_NODE_POST_POWER_ON_TAG","All tasks associated with procedures
   following power on of peer nodes."
   "LMS_LVM_VOLUME_TAG","All tasks associated with MS LVM file-systems."
   "``Default Phase``", "``Position of the default phase.``"
   "LMS_REBOOT_TAG","All tasks associated with MS reboot."

Generating Tasks for Snapshot Plans
-----------------------------------

The :func:`litp.core.plugin.Plugin.create_snapshot_plan()` method is called by
the Execution Manager for all plugins when a snapshot plan is being created. It
is called after successful snapshot model validation has been performed by all
plugins (see :func:`litp.core.plugin.Plugin.validate_model_snapshot`).

The :func:`litp.core.plugin_context_api.PluginApiContext.snapshot_action`
method will return a ``create``, ``remove`` or ``restore`` action or will raise
an exception if no matching action is found.

The :func:`litp.core.plugin_context_api.PluginApiContext.snapshot_model` method
will return a :class:`~litp.core.snapshot_model_api.SnapshotModelApi` object
for the current snapshot or None if no snapshot present.  The
:func:`~litp.core.plugin_context_api.PluginApiContext.snapshot_model` method
only pertains to ``restore`` and ``remove`` actions, and not ``create``.

.. code-block:: python

    from litp.plan_types.create_snapshot import create_snapshot_tags
    from litp.plan_types.create_snapshot import remove_snapshot_tags
    from litp.plan_types.create_snapshot import restore_snapshot_tags

    def create_snapshot_plan(self, plugin_api_context):
        tasks = []
        # Returns action to execute in the snapshot plan
        action = plugin_api_context.snapshot_action()

        if action == 'create':
            for node in plugin_api_context.query("node"):
                if node.is_initial():
                    for fs in node.query("filesystems"):
                        tasks.append(CallbackTask(
                            fs,
                            "Create a snapshot of '{0}'".format(fs.name),
                            self._create_snapshot_task,
                            node.hostname, fs.name,
                            tag_name=create_snapshot_tags.NAS_FILESYSTEM_TAG
                        ))
        elif action =='remove':
            # Returns the SnapshotModelApi for the current snapshot
            snapshot_model = plugin_api_context.snapshot_model()
            if snapshot_model != None:
                for node in snapshot_model.query("node"):
                    for fs in node.query("filesystems"):
                        tasks.append(CallbackTask(
                            fs,
                            "Remove a snapshot of '{0}'".format(fs.name),
                            self._remove_snapshot_task,
                            node.hostname, fs.name,
                            tag_name=remove_snapshot_tags.NAS_FILESYSTEM_TAG
                        ))
        elif action =='restore':
            # Returns the SnapshotModelApi for the current snapshot
            snapshot_model = plugin_api_context.snapshot_model()
            if snapshot_model != None:
                for node in snapshot_model.query("node"):
                    for fs in node.query("filesystems"):
                        tasks.append(CallbackTask(
                            fs,
                            "Restore a snapshot of '{0}'".format(fs.name),
                            self._restore_snapshot_task,
                            node.hostname, fs.name,
                            tag_name=restore_snapshot_tags.NAS_FILESYSTEM_TAG
                        ))
        return tasks

    def _create_snapshot_task(self, callback_api, node_hostname, fs_name):
        # callback task method to create a snapshot
        pass

    def _remove_snapshot_task(self, callback_api, node_hostname, fs_name):
        # callback task method to remove a snapshot
        pass

    def _remove_snapshot_task(self, callback_api, node_hostname, fs_name):
        # callback task method to remove a snapshot
        pass

.. _accessing-snapshot-data:

Accessing Snapshot Data from within the Plugin
----------------------------------------------

.. currentmodule:: litp.core.snapshot_model_api

The :class:`SnapshotModelApi` should only be used when generating snapshot
tasks or validating the model in a plugin's
:func:`~litp.core.plugin.Plugin.create_snapshot_plan()` or
:func:`~litp.core.plugin.Plugin.validate_model_snapshot` methods.

The :func:`litp.core.plugin_context_api.PluginApiContext.snapshot_model`
method returns a :class:`SnapshotModelApi` object that provides a read-only,
queryable model as it was at the time of the snapshot creation.  The
:class:`SnapshotModelApi` is only available through
:class:`~litp.core.plugin_context_api.PluginApiContext` instances and not
through :class:`~litp.core.callback_api.CallbackApi` instances.

Use :func:`SnapshotModelApi.query` or :func:`SnapshotModelApi.query_by_vpath`
to retrieve :class:`~litp.core.model_manager.QueryItem` objects matching
items of the deployment model:

.. code-block:: python

    snapshot_model = plugin_api_context.snapshot_model()
    if snapshot_model:
        nodes = snapshot_model.query('node')
        for node in nodes:
            # file systems for node from the creation time of the snapshot
            fs_for_node = node.query('file-system-base')

.. warning::

    The :class:`SnapshotModelApi` is not a replacement for the
    :class:`~litp.core.plugin_context_api.PluginApiContext`. If
    querying for live model data, the :class:`SnapshotModelApi`
    should not be used.

The snapshot model data source is deleted when the snapshot is removed.

For more information on working with your plugin, see
:ref:`methods_to_implement_in_a_plugin`. 
