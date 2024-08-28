.. _rest-get-operations:

=======================================
GET operation - LITP |release| REST API
=======================================

##############
GET Operations
##############

The REST API ``GET`` operation maps to the READ operation to request details of a specific ``item`` URI.

Request Structure
-----------------

.. csv-table::
   :header: "Component", "Example", "Description"

   "Request Location/URI", "``{base_uri}/deployments/d1``", "URI to be operated upon"
   "Accept Header", "``application/json``", "Acceptable content type (optional, and currently unused)"
   "Request Type", "``GET``", "HTTP method"

Response Header
---------------

The Header includes the HTTP status code for after the operation and the ``Content-Type`` of the response data.

.. code-block:: rest

   HTTP/1.1 200 OK
   Date: Mon, 21 Oct 2013 10:16:43 GMT
   Content-Length: 622
   Content-Type: application/json

Example: Read the content of an ``item``
----------------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/deployments/d1

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
    "item-type-name": "deployment",
    "_embedded": {
        "item": [
            {
                "item-type-name": "collection-of-cluster",
                "applied_properties_determinable": true,
                "state": "Initial",
                "_links": {
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters"
                    },
                    "collection-of": {
                        "href": "{base_uri}/item-types/cluster"
                    }
                },
                "id": "clusters"
            }
        ]
    },
    "state": "Initial",
    "applied_properties_determinable": true,
    "_links": {
        "self": {
            "href": "{base_uri}/deployments/d1"
        },
        "item-type": {
            "href": "{base_uri}/item-types/deployment"
        }
    },
    "id": "d1"
   }
  
   

Example: Read the content of a ``collection``
---------------------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/deployments/d1/clusters/cluster1/nodes

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
    "item-type-name": "collection-of-node",
    "_embedded": {
        "item": [
            {
                "item-type-name": "node",
                "applied_properties_determinable": true,
                "state": "Initial",
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
                "applied_properties_determinable": true,
                "state": "Initial",
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
    "state": "Initial",
    "applied_properties_determinable": true,
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


Example: Read the ``item`` content that was inherited from another ``item``
---------------------------------------------------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/deployments/d1/clusters/cluster1/nodes/node1/os

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/os"
           },
           "inherited-from": {
               "href": "{base_uri}/software/profiles/rhel_6_6"
           }
       },
       "properties": {
           "name": "sample-profile"
       },
       "id": "os",
        "applied_properties_determinable": true,
       "item-type-name": "reference-to-os-profile",
       "state": "Initial",
       "required": "system"
   }

Example: Read the content of a ``plan``
---------------------------------------

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
       "state": "valid",
       "snapshot": "Snapshot with timestamp 12345.67 exists"
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
