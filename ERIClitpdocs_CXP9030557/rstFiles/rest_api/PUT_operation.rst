.. _rest-put-operations:

=======================================
PUT operation - LITP |release| REST API
=======================================

#############
PUT Operation
#############

The REST API PUT Operation maps to the ``UPDATE`` operation to update an existing ``item`` with given parameters.
Properties should be supplied in correct key value pairs with no duplicates as per ``RFC 4627`` for ``application/json`` media type (http://tools.ietf.org/html/rfc4627#section-2.2).
If any key:value pair in the current implementation has the same key as an existing pair, the value of the new pair replaces that of the existing pair.

If a property is to be removed, an empty (``null``) value can be specified - subject to validation.

The operation returns the ``item`` state after completion.

Request Structure
-----------------

.. csv-table::
   :header: "Component", "Example", "Description"

   "Request Location/URI", "``{base_uri}/deployments/d1/clusters/c1``", "URI to be operated upon"
   "Content Type", "``Content-Type:application/json``", "content type of data in payload"
   "Request Data", "``{'properties':{'HA_manager':'haManager1'}}``", "``PUT`` JSON data"
   "Request Type", "``PUT``", "HTTP method"

Request PUT Data
^^^^^^^^^^^^^^^^^
Request PUT data has the following form

.. code-block:: rest

   {
       "properties": {}
   }

``properties`` are key value pairs that will be validated against the ``item-type`` properties

When updating a ``plan`` object, the key ``state`` replaces ``properties``

.. code-block:: rest

   {
       "state": ""
   }

valid values

Response Header
---------------

The Header includes the HTTP status code for after the operation and the ``Content-Type`` of the response data.

.. code-block:: rest

   HTTP/1.1 200 OK
   Date: Fri, 18 Oct 2013 14:51:38 GMT
   Content-Length: 857
   Content-Type: application/json

Example: Update one or more properties - ``mac address``
--------------------------------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/infrastructure/systems/ms_system/network_interfaces/if0

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       "properties": {
           "macaddress": "08:00:27:65:C8:B3"
       }
   }

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
    "item-type-name": "eth",
    "state": "Updated",
    "applied_properties_determinable": true,
    "_links": {
        "self": {
            "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/network_interfaces/if0"
        },
        "item-type": {
            "href": "{base_uri}/item-types/eth"
        }
    },
    "id": "if0",
    "properties": {
        "macaddress": "08:00:27:65:C8:B3",
        "ipaddress": "10.10.10.101",
        "network_name": "mgmt",
        "device_name": "eth0"
    }
   }

Example: Remove non required property - ``mac address``
-------------------------------------------------------
If the property is not ``required`` then the property will be removed.

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/infrastructure/systems/ms_system/network_interfaces/if0

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       "properties": {
           "macaddress": null
       }
   }

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/infrastructure/systems/ms_system/network_interfaces/if0"
           },
           "item-type": {
               "href": "{base_uri}/item-types/nic"
           }
       },
       "applied_properties_determinable": true,
       "properties": {
           "interface_name": "eth0"
       },
       "id": "if0",
       "item-type-name": "nic",
       "state": "Initial"
   }

Example: Remove required property - ``hostname``
------------------------------------------------
If the property is ``required``, then any ``regex`` and validation are applied.
If the property is ``required``, a ``default`` value is defined for it and ``null`` is passed as a value in the request data. The ``default`` value is then applied.


Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/deployments/d1/clusters/cluster1/nodes/node1

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       "properties": {
           "hostname": null
       }
   }

Response Header
^^^^^^^^^^^^^^^

.. code-block:: rest

   HTTP/1.1 400 Bad Request
   Date: Fri, 18 Oct 2013 14:51:38 GMT
   Content-Length: 857
   Content-Type: application/json

Response Body
^^^^^^^^^^^^^

.. code-block:: rest
 
   {
    "_embedded": {
        "item": [
            {
                "required": "os",
                "id": "storage_profile",
                "applied_properties_determinable": true,
                "item-type-name": "reference-to-storage-profile",
                "state": "Initial",
                "_links": {
                    "inherited-from": {
                        "href": "{base_uri}/infrastructure/storage/storage_profiles/profile_1"
                    },
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/storage_profile"
                    },
                    "item-type": {
                        "href": "{base_uri}/item-types/storage-profile"
                    }
                },
                "properties": {
                    "volume_driver": "lvm"
                }
            },
            {
                "item-type-name": "ref-collection-of-software-item",
                "state": "Initial",
                "applied_properties_determinable": true,
                "required": "os,storage_profile",
                "_links": {
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/items"
                    },
                    "ref-collection-of": {
                        "href": "{base_uri}/item-types/software-item"
                    }
                },
                "id": "items"
            },
            {
                "item-type-name": "collection-of-network-interface",
                "applied_properties_determinable": true,
                "state": "Initial",
                "required": "os",
                "_links": {
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/network_interfaces"
                    },
                    "collection-of": {
                        "href": "{base_uri}/item-types/network-interface"
                    }
                },
                "id": "network_interfaces"
            },
            {
                "required": "controllers",
                "id": "system",
                "applied_properties_determinable": true,
                "item-type-name": "reference-to-system",
                "state": "Initial",
                "_links": {
                    "inherited-from": {
                        "href": "{base_uri}/infrastructure/systems/system1"
                    },
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/system"
                    },
                    "item-type": {
                        "href": "{base_uri}/item-types/system"
                    }
                },
                "properties": {
                    "system_name": "MN1VM"
                }
            },
            {
                "applied_properties_determinable": true,
                "item-type-name": "collection-of-controller-base",
                "state": "Initial",
                "_links": {
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/controllers"
                    },
                    "collection-of": {
                        "href": "{base_uri}/item-types/controller-base"
                    }
                },
                "id": "controllers"
            },
            {
                "applied_properties_determinable": true,
                "item-type-name": "ref-collection-of-service-base",
                "state": "Initial",
                "required": "os",
                "_links": {
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/services"
                    },
                    "ref-collection-of": {
                        "href": "{base_uri}/item-types/service-base"
                    }
                },
                "id": "services"
            },
            {
                "applied_properties_determinable": true,
                "item-type-name": "ref-collection-of-route-base",
                "state": "Initial",
                "_links": {
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/routes"
                    },
                    "ref-collection-of": {
                        "href": "{base_uri}/item-types/route-base"
                    }
                },
                "id": "routes"
            },
            {
                "item-type-name": "collection-of-node-config",
                "applied_properties_determinable": true,
                "state": "Initial",
                "required": "network_interfaces",
                "_links": {
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/configs"
                    },
                    "collection-of": {
                        "href": "{base_uri}/item-types/node-config"
                    }
                },
                "id": "configs"
            },
            {
                "required": "system",
                "id": "os",
                "applied_properties_determinable": true,
                "item-type-name": "reference-to-os-profile",
                "state": "Initial",
                "_links": {
                    "inherited-from": {
                        "href": "{base_uri}/software/profiles/rhel_6_6"
                    },
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/os"
                    },
                    "item-type": {
                        "href": "{base_uri}/item-types/os-profile"
                    }
                },
                "properties": {
                    "name": "sample-profile",
                    "kopts_post": "console=ttyS0,115200",
                    "breed": "redhat",
                    "version": "rhel6",
                    "path": "/var/www/html/6/os/x86_64/",
                    "arch": "x86_64"
                }
            },
            {
                "item-type-name": "ref-collection-of-file-system-base",
                "state": "Initial",
                "applied_properties_determinable": true,
                "required": "storage_profile",
                "_links": {
                    "self": {
                        "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1/file_systems"
                    },
                    "ref-collection-of": {
                        "href": "{base_uri}/item-types/file-system-base"
                    }
                },
                "id": "file_systems"
            }
        ]
    },
    "messages": [
        {
            "message": "ItemType \"node\" is required to have a \"property\" with name \"hostname\"",
            "type": "MissingRequiredPropertyError",
            "property_name": "hostname"
        }
    ],
    "id": "node1",
    "item-type-name": "node",
    "state": "Applied",
    "_links": {
        "self": {
            "href": "{base_uri}/deployments/d1/clusters/cluster1/nodes/node1"
        },
        "item-type": {
            "href": "{base_uri}/item-types/node"
        }
    },
    "properties": {
        "hostname": "node1"
    }
   }

Example: Run a ``plan``
-----------------------

.. code-block:: rest

   {base_uri}/plans/plan

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       state:"running"
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
       "state": "running"
   }

Example: Stop a running ``plan``
--------------------------------

.. code-block:: rest

   {base_uri}/plans/plan

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       state:"stopped"
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
       "state": "stopping"
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
