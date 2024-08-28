.. _rest-snapshot-operations:

=============================================
Snapshot operations - LITP |release| REST API
=============================================

###################
Snapshot Operations
###################

********
Overview
********

The REST interface supports a limited set of operations for interacting
with ``snapshot-base`` items.
The CLI commands ``create_snapshot``, ``remove_snapshot`` and
``restore_snapshot`` issue the following requests to complete user operations.


List ``snapshots``
------------------
The collection of ``snapshot-base`` items is located at

.. code-block:: rest

   {base_uri}/snapshots

Request Method
^^^^^^^^^^^^^^

.. code-block:: rest

   GET

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {

    "_links": {
        "self": {
            "href": "{base_uri}/snapshots"
        },
        "collection-of": {
            "href": "{base_uri}/item-types/snapshot-base"
        }
    },
    "id": "snapshots",
    "item-type-name": "collection-of-snapshot-base",
    "state": "Applied",
    "_embedded": {
        "item": [
            {
                "_links": {
                    "self": {
                        "href": "{base_uri}/snapshots/named"
                    },
                    "item-type": {
                        "href": "{base_uri}/item-types/snapshot-base"
                    }
                },
                "id": "named",
                "item-type-name": "snapshot-base",
                "properties": {
                    "active": "true",
                    "timestamp": "1428129881.7"
                },
                "state": "Applied"

            },
            {
                "_links": {
                    "self": {
                        "href": "{base_uri}/snapshots/snapshot"
                    },
                    "item-type": {
                        "href": "{base_uri}/item-types/snapshot-base"
                    }
                },
                "id": "snapshot",
                "item-type-name": "snapshot-base",
                "properties": {
                    "timestamp": "1428129842.15"
                },
                "state": "Applied"
            }
        ]
    }

List ``snapshot``
-----------------
Individual ``snapshot-base`` items are located by

.. code-block:: rest

   {base_uri}/snapshots/{snapshot name}

Request Method
^^^^^^^^^^^^^^

.. code-block:: rest

   GET

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
        "_links": {
            "self": {
                "href": "{base_uri}/snapshots/{snapshot name}"
            },
            "item-type": {
                "href": "{base_uri}/item-types/snapshot-base"
            }
        },
        "id": "{snapshot name}",
        "item-type-name": "snapshot-base",
        "properties": {
            "active": "true",
            "timestamp": "1428129881.7"
        },
        "state": "Applied"
    }

*******************
Snapshot Operations
*******************

.. _create_a_snapshot:

Create a ``snapshot``
---------------------
A ``POST`` request to a valid URI will create a ``snapshot-base``
model item (identified by the unique snapshot identifier ``{snapshot name}``).
A ``create`` snapshot ``plan`` is created and triggered to run.
The ``create`` snapshot ``plan`` is returned.
A ``{snapshot name}`` of ``snapshot`` must be used to create a deployment snapshot.
All other values for ``{snapshot name}`` will create named backup snapshots.

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/snapshots/{snapshot name}

Optional Request Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: rest

   {base_uri}/snapshots/{snapshot name}?exclude_nodes={excluded nodes}
The optional request parameter ``exclude_nodes`` can be appended to the Request URI. The value of ``{excluded nodes}`` is a comma separated list of node hostnames.

Request Method
^^^^^^^^^^^^^^

.. code-block:: rest

   POST

Request Body
^^^^^^^^^^^^

The only property in the request body is

.. code-block:: rest

   {
       "type": "snapshot-base"
   }



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
       "state": "initial"
   }

Remove a ``snapshot`` ( Deprecated, this_ )
-------------------------------------------

A ``DELETE`` request to a valid URI will remove a ``snapshot-base``
model item (identified by the unique snapshot identifier ``{snapshot name}``).
A ``remove`` snapshot ``plan`` is created and triggered to run.
The ``remove`` snapshot ``plan`` is returned.

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/snapshots/{snapshot name}

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
       "state": "initial"
   }

.. _this:
.. _remove_a_snapshot:

Remove a ``snapshot``
----------------------
A ``PUT`` request to a valid URI will remove a ``snapshot-base``
model item (identified by the unique snapshot identifier ``{snapshot name}``).
A ``remove`` snapshot ``plan`` is created and triggered to run.
The ``remove`` snapshot ``plan`` is returned.


.. code-block:: rest

   {base_uri}/snapshots/{snapshot name}

Optional Request Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: rest

   {base_uri}/snapshots/{snapshot name}?exclude_nodes={excluded nodes}
The optional request parameter ``exclude_nodes`` can be appended to the Request URI. The value of ``{excluded nodes}`` is a comma separated list of node hostnames.

Request Body
^^^^^^^^^^^^
You must set the value of the ``action`` property to ``remove`` to trigger the remove snapshot plan.

.. code-block:: rest

   {
       "properties":{"action" : "remove"}
   }

The ``force`` property is optional and defaults to ``False`` if not specified.

If this value is ``False``, the ``remove`` snapshot plan will fail if any nodes are unreachable. If the property is set to ``True``, the plan will ignore unreachable nodes. 


.. code-block:: rest

   {
       "properties":{"action" : "remove", "force" : "True"}
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
       "state": "initial"
   }


Restore a ``snapshot``
----------------------
A ``PUT`` request to a valid URI will update a ``snapshot-base``
model item (identified by the unique snapshot identifier ``{snapshot name}``).
A ``restore`` snapshot ``plan`` is created and triggered to run.
The ``restore`` snapshot ``plan`` is returned.
Only deployment ``snapshot-base`` items (``{snapshot name}`` of ``snapshot``) may be restored.


.. code-block:: rest

   {base_uri}/snapshots/snapshot

Request Body
^^^^^^^^^^^^
The required property ``force`` can be set to ``True`` or ``False``. 
If this value is ``True``, the ``restore`` snapshot plan will run even if there are nodes that are unreachable or if there are missing snapshots on reachable nodes. If the value is ``False``, the ``restore`` snapshot plan  will fail if any nodes are unreachable or if there are no appropriate snapshots found.

.. code-block:: rest

   {
       "properties":{"force" : "False"}
   }

The property ``action`` is optional and if used, it must be set to ``restore``.
If not specified, is treated as ``restore``.

.. code-block:: rest

   {
       "properties":{"action" :"restore", force" : "False"}
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
       "state": "initial"
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
