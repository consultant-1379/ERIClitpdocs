.. _rest-plan-operations:

=========================================
Plan operations - LITP |release| REST API
=========================================

###############
Plan Operations
###############

********
Overview
********

A ``plan`` is a sorted list of tasks used to deploy the deployment model on a system. The ``tasks`` are arranged according to a topological sort algorithm based on queries to plugins and dependencies in the model for items used by the plugins. Only one ``plan`` exists at any time and you must create a new ``plan`` following any changes to the model. ``Plan`` operations via the REST interface are shown below.

**************
Plan Structure
**************

When a ``plan`` is created, a ``POST`` request to the ``plans`` URI will cause the model to be validated. The response will either be a ``plan`` structure or a list of error messages. Once created, a ``plan`` is a conceptual node that maintains the current state of the ``plan`` (``running``, ``stopped``, ``valid`` etc.) and the ``phases`` and ``tasks`` that are to be run within that ``plan``. The ``plan`` structure is shown as follows:

.. code-block:: rest

    plan
    |
    |
    +---phases
    |    |
    |    +----phase_1
    |    |    |
    |    |    +----task_1
    |    |    +----task_2
    :    :    :
    |    |    +----task_n
    |    |
    |    +----phase_2
    |    |    |
    |    |    +----task_1
    |    |    +----task_2
    :    :    :
    |    |    +----task_n
    |    |
    |    +----phase_n
    |    |    |
    |    |    +----task_1
    |    |    +----task_2
    :    :    :
    |    |    +----task_n


Example sample ``plan``
-----------------------

.. code-block:: rest

    Phase 1
        Task status
        -----------
        Success         .../ms/services/cobbler
                        Generate UDEV Kickstart snippet for host "node2"
        Success         .../ms/services/cobbler
                        Generate UDEV Kickstart snippet for host "node1"
        Success         .../ms/services/cobbler
                        Generate LVM Kickstart snippet for host "node2"
        Success         .../ms/services/cobbler
                        Generate LVM Kickstart snippet for host "node1"
        Success         .../ms/services/cobbler
                        Generate Cobbler Kickstart file for host "node2"
        Success         .../ms/services/cobbler
                        Generate Cobbler Kickstart file for host "node1"
    Phase 2
        Task status
        -----------
        Success         .../ms/services
                        Set up Cobbler distros, profiles and systems for node
                        s: ['node2', 'node1']
    Phase 3
        Task status
        -----------
        Running         .../ms/libvirt
                        Create VM "VM2"
        Running         .../ms/libvirt
                        Create VM "VM1"
    Phase 4
        Task status
        -----------
        Initial         .../d1/nodes/node1/network_profile/netgraph
                        Generate task for loopback.
        Initial         .../d1/nodes/node1/network_profile/netgraph
                        Generate tasks for ifaces
        Initial         .../deployments/d1/nodes/node1/system
                        Wait for VM "VM1" to initialise
        Initial         .../d1/nodes/node2/network_profile/netgraph
                        Generate task for loopback.
        Initial         .../d1/nodes/node2/network_profile/netgraph
                        Generate tasks for ifaces
        Initial         .../deployments/d1/nodes/node2/system
                        Wait for VM "VM2" to initialise
    Phase 5
        Task status
        -----------
        Initial         .../deployments/d1/nodes/node1/os
                        Wait for node "node1" to install
        Initial         .../deployments/d1/nodes/node2/os
                        Wait for node "node2" to install

***************
Plan Operations
***************

Create a ``plan``
-----------------
Any changes to the model will require a new ``plan`` to be created (which results in model validation). This is done via a ``POST`` request.

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/plans/

Request Method
^^^^^^^^^^^^^^

.. code-block:: rest

   POST

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       "id": "plan",
       "type": "plan"
       "no-lock-tasks": "true|false"
       "no-lock-tasks-list": c1 c2
   }

Note: ``no-lock-tasks`` is an optional parameter. If specified as ``true``, plugin generation of Lock/Unlock tasks is skipped. As a result, tasks in plan phases may be different.

Note: ``no-lock-tasks-list`` is an optional parameter.  If clusters are specified then it will skip the plugin generation of Lock/Unlock tasks for the nodes in those clusters.

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/plans/plan"
           },
           "item-type": {
               "href": "{base_uri}/item-types/plan"
           }
       },
       "id": "plan",
       "item-type-name": "plan",
       "_embedded": {
           "item": [
               {
                   "_links": {
                       "self": {
                           "href": "{base_uri}/plans/plan/phases"
                       },
                       "collection-of": {
                           "href": "{base_uri}/item-types/phase"
                       }
                   },
                   "id": "phases",
                   "item-type-name": "collection-of-phase"
               }
           ]
       },
       "state": "valid"
   }

Run a ``plan``
--------------
A ``plan`` may be executed by issuing a ``PUT`` request to a created ``plan``, specifying the ``state`` change in the request body. Valid states are: ``running`` and ``stopped``.

.. code-block:: rest

   {base_uri}/plans/plan

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       state:"running"
   }

Request Method
^^^^^^^^^^^^^^

.. code-block:: rest

   PUT

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/plans/plan"
           },
           "item-type": {
               "href": "{base_uri}/item-types/plan"
           }
       },
       "id": "plan",
       "item-type-name": "plan",
       "_embedded": {
           "item": [
               {
                   "_links": {
                       "self": {
                           "href": "{base_uri}/plans/plan/phases"
                       },
                       "collection-of": {
                           "href": "{base_uri}/item-types/phase"
                       }
                   },
                   "id": "phases",
                   "item-type-name": "collection-of-phase"
               }
           ]
       },
       "state": "running"
   }

Stop a running ``plan``
-----------------------
Updates to the ``plan`` while it is executing may be possible depending on the errors returned from running ``tasks`` and ``phases``.

.. code-block:: rest

   {base_uri}/plans/plan

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       state:"stopped"
   }

Request Method
^^^^^^^^^^^^^^

.. code-block:: rest

   PUT

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/plans/plan"
           },
           "item-type": {
               "href": "{base_uri}/item-types/plan"
           }
       },
       "id": "plan",
       "item-type-name": "plan",
       "_embedded": {
           "item": [
               {
                   "_links": {
                       "self": {
                           "href": "{base_uri}/plans/plan/phases"
                       },
                       "collection-of": {
                           "href": "{base_uri}/item-types/phase"
                       }
                   },
                   "id": "phases",
                   "item-type-name": "collection-of-phase"
               }
           ]
       },
       "state": "stopping"
   }



Resume a ``plan``
-----------------
A ``plan`` that has entered the ``failed`` state may be resumed by issuing a ``PUT`` request to the ``plan``, specifying a ``state`` change back to ``running`` in the request body if the ``resume`` option is also passed with a value of ``true``. Valid ``resume`` values are: ``true`` and ``false``.

.. code-block:: rest

   {base_uri}/plans/plan

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       state:"running",
       resume:"true"
   }

Request Method
^^^^^^^^^^^^^^

.. code-block:: rest

   PUT

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/plans/plan"
           },
           "item-type": {
               "href": "{base_uri}/item-types/plan"
           }
       },
       "id": "plan",
       "item-type-name": "plan",
       "_embedded": {
           "item": [
               {
                   "_links": {
                       "self": {
                           "href": "{base_uri}/plans/plan/phases"
                       },
                       "collection-of": {
                           "href": "{base_uri}/item-types/phase"
                       }
                   },
                   "id": "phases",
                   "item-type-name": "collection-of-phase"
               }
           ]
       },
       "state": "running"
   }


Delete a ``plan``
-----------------
A ``DELETE`` operation can be issued to the ``plan`` if it is to be removed.
A successful completion returns the containing object ``{base_uri}/plans``

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/plans/plan

Request Method
^^^^^^^^^^^^^^

.. code-block:: rest

   DELETE

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/plans"
           },
           "collection-of": {
               "href": "{base_uri}/item-types/plan"
           }
       },
       "id": "plans",
       "item-type-name": "collection-of-plan"
   }

----------
REST Pages
----------
* :ref:`rest-api-crud`
   - :ref:`rest-api-request_format`
   - :ref:`rest-api-response_format`
   - :ref:`rest-post-operations`
   - :ref:`rest-get-operations`
   - :ref:`rest-put-operations`
   - :ref:`rest-delete-operations`
* :ref:`rest-plan-operations`
* :ref:`rest-snapshot-operations`
* :ref:`rest-item-discovery`
* :ref:`rest-message-handling`
* :ref:`rest-litp-operations`
