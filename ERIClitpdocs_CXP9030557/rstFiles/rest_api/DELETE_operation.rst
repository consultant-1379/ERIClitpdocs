.. _rest-delete-operations:

==========================================
DELETE operation - LITP |release| REST API
==========================================

################
DELETE Operation
################

The REST API ``DELETE`` operation will attempt to remove an existing ``item`` and remove everything below that ``item`` in the model. The ``item`` returned in the response is the parent of the deleted resource.


Request Structure
-----------------

.. csv-table::
   :header: "Component", "Example", "Description"

   "Request Location/URI", "``{base_uri}/deployments/d1``", "URI to be operated upon"
   "Request Type", "``DELETE``", "HTTP method"

Response Header
---------------

The Header includes the HTTP status code for after the operation and the ``Content-Type`` of the response data.

.. code-block:: rest

   HTTP/1.1 200 OK
   Date: Fri, 18 Oct 2013 14:40:57 GMT
   Content-Length: 359
   Content-Type: application/json

Example: Delete a ``node``
--------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/deployments/d1/clusters/cluster1/nodes/node1

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
    "item-type-name": "collection-of-node",
    "_embedded": {
        "item": [
            {
                "item-type-name": "node",
                "state": "ForRemoval",
                "_links": {
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1"
                    },
                    "item-type": {
                        "href": "{base_uri}/item-types/node"
                    }
                },
                "id": "node1",
                "properties": {
                    "hostname": "node1"
                }
            },
            {
                "item-type-name": "node",
                "state": "Applied",
                "_links": {
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node2"
                    },
                    "item-type": {
                        "href": "{base_uri}/item-types/node"
                    }
                },
                "id": "node2",
                "properties": {
                    "hostname": "node2"
                }
            }
        ]
    },
    "state": "Applied",
    "_links": {
        "self": {
            "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes"
        },
        "collection-of": {
            "href": "{base_uri}/item-types/node"
        }
    },
    "id": "nodes"
   }

Example: Delete a ``plan``
--------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/plans/plan

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
