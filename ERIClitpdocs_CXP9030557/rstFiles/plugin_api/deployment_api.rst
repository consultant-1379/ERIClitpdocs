.. |external| raw:: html

   <img alt="external" src="_static/external_link_icon.svg">

.. |br| raw:: html

   <br />

.. _plugin_deployment_api:

.. currentmodule:: litp.core.task

====================================
LITP |release| Plugin Deployment API
====================================

This document details the API available to plugins for deploying a model.

Instances of :class:`ConfigTask`, :class:`CallbackTask` or
:class:`RemoteExecutionTask` generated by plugins during the creation of a
deployment plan can be given a ``tag_name`` attribute which is used as an
identifier to assign the Task to a given group.

For more information on task ordering, see :ref:`task-ordering-derived`.


Using tags to order deployment tasks
====================================

To specify the order of a task in a deployment plan, the plugin author can provide
a tag to the task.

The task is then assigned to the appropriate group based on a predefined
set of rules in the deployment plan creation logic. For a task to be assigned
to a given group, it must meet at least one of the criteria defined for that group.

.. note::
  If a task tag is not provided, then the task's group is determined by
  the model item to which the task is associated (this is true of all task types)

.. warning::
  You must ensure that only suitable tags are given to tasks. Unsuitable tags may
  result in tasks being filtered out of the plan (for example, by assigning the
  ``NODE_TAG`` tag to a task whose associated primary item is ``/ms``).

Group criteria
*******************

Given the ``NODE_GROUP`` criteria below, for a task to meet these criteria it has
to satisfy *one* of the following:

#. The task is tagged with the ``NODE_TAG``.
#. The task is an instance of :class:`RemoteExecutionTask` that is not given a tag but satifies the ruleset criteria below.
#. The task is an instance of :class:`ConfigTask` that is not given a tag but satifies the ruleset criteria below.
#. The task is an instance of :class:`CallbackTask` that is not given a tag but satifies the ruleset criteria below.

.. code-block:: python
   :emphasize-lines: 5, 8-10, 13-15, 18-20

    {
        "group_name": deployment_plan_groups.NODE_GROUP,
        "criteria": [
            {
                "tag_name": deployment_plan_tags.NODE_TAG,
            },
            {
                "task_type": "RemoteExecutionTask",
                "model_item.get_node.is_node": True,
                "tag_name": None,
            },
            {
                "task_type": "ConfigTask",
                "node.is_ms": False,
                "tag_name": None,
            },
            {
                "task_type": "CallbackTask",
                "model_item.get_node.is_node": True,
                "tag_name": None,
            }],
        "requires": [deployment_plan_groups.BOOT_GROUP]
    },

If a task is provided with an invalid tag, a warning is logged and the task
is treated as if no tag was provided and sorted into the ``MS_GROUP``. A
ruleset has a default group that is populated with tasks that do not match
any group criteria. An invalid tag is a tag that has not been defined in
a ruleset.

Example Config tasks using a tag:
*********************************

.. code-block:: python
   :emphasize-lines: 11, 16, 21, 26

    from litp.plan_types.deployment_plan import deployment_plan_tags

    def create_configuration(self, api):
        tasks = []
        for node in api.query('node'):
            for item in node.query('story10531_tc1', is_initial=True):
                tasks.append(ConfigTask(
                    node, item,
                    'tagged as MS',
                    'res_ms', 'apache-package',
                    tag_name=deployment_plan_tags.MS_TAG))
                tasks.append(ConfigTask(
                    node, item,
                    'tagged as BOOT',
                    'res_boot', 'apache.conf',
                    tag_name=deployment_plan_tags.BOOT_TAG))
                tasks.append(ConfigTask(
                    node, item,
                    'tagged as CLUSTER',
                    'res_cluster', 'httpd_2',
                    tag_name=deployment_plan_tags.CLUSTER_TAG))
                tasks.append(ConfigTask(
                    node, item,
                    'tagged as NODE',
                    'res_node', 'httpd_1',
                    tag_name=deployment_plan_tags.NODE_TAG))
        return tasks


.. py:module:: litp.plan_types.deployment_plan.deployment_plan_ruleset

.. py:module:: litp.plan_types.deployment_plan.deployment_plan_tags

The tags for **deployment plan** tasks are available for import
from :py:mod:`litp.plan_types.deployment_plan.deployment_plan_tags`.
The following tags are valid for **deployment plan** tasks:

.. csv-table::
   :header: "Tag", "Description"

   ``MS_TAG``, "All tasks associated with a model item which is a child of the LITP
   Management Server."
   ``BOOT_TAG``, "All tasks used to install the operating system on new nodes."
   ``PRE_NODE_CLUSTER_TAG``, "All tasks whose model item is a cluster item
   that must be executed *before* node tasks for that cluster"
   ``NODE_TAG``, "All tasks associated with a model item under a node."
   ``CLUSTER_TAG``, "All tasks whose model item is a cluster item."
   ``POST_CLUSTER_TAG``, "All tasks that must be executed *after*
   tasks in the cluster group."
