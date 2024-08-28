.. _rest-item-discovery:

=========================================
Item discovery  - LITP |release| REST API
=========================================

#######################
REST API Item Discovery
#######################

The REST API discovery service returns a list of ``item-types`` and ``property-types`` registered with this instance that can be used to build a LITP model.

The ``item-types`` and ``property-types`` endpoints are located at:

.. code-block:: rest

   {base_uri}/item-types

   {base_uri}/property-types

where an ``item`` has a valid ``item-type`` definition a link to it is included in the ``_links``

.. code-block:: rest

           "item-type": {
               "href": "{base_uri}/item-types/{item-type-name}"
           }

where an ``item`` has a collection of ``item-type`` objects definition a link to it is included in the ``_links``

.. code-block:: rest

           "collection-of": {
               "href": "{base_uri}/item-types/{item-type-name}"
           }

and a corresponding ``item-type-name`` ``key:value`` property

.. code-block:: rest

           "item-type-name": "",

.. _item-type-operations:

**********
Item Types
**********

Item Type Schema
----------------
An ``item-type`` entry can have any of  the following properties:
 - ``default`` - A default value for the ``item``, which will be set if none is provided. If the ``item`` has no default, "null" will be present.
 - ``description`` - description of the item type
 - ``regex`` - the regular expression which the value supplied must satisfy (e.g.: ^(true)|(false)$ can only be satisfied by "true" or "false")
 - ``required`` - a boolean expression which denotes whether the field is required to create the item type
 - ``base-type`` - the item type which the current type extends (e.g. a "libvirt-system", is an extension of the general "system" type)

For collection types, in addition to the ``rel`` link in ``_links``, the following is returned:
 - ``max`` - the maximum number of items this collection field can contain (validated upon ``plan`` creation)
 - ``min`` - the minimum number of items this collection field can contain (validated upon ``plan`` creation)

Request Structure
-----------------

.. csv-table::
   :header: "Component", "Example", "Description"

   "Request Location/URI", "``{base_uri}/item-types``", "URI to be operated upon"
   "Request Type", "``GET``", "HTTP method"

Response Header
---------------

The Header includes the HTTP status code for after the operation and the ``Content-Type`` of the response data.

.. code-block:: rest

   HTTP/1.1 200 OK
   Date: Fri, 18 Oct 2013 14:51:38 GMT
   Content-Length: 857
   Content-Type: application/json

Example: list all ``item-types``
--------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/item-types

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/item-types"
           }
       },
       "id": "item-types",
       "_embedded": {
           "item-type": [
               :
               :
               {
                   "_links": {
                       "self": {
                           "href": "{base_uri}/item-types/node"
                       }
                   },
                   "id": "node",
                   "properties": {
                       "hostname": {
                           "_links": {
                               "self": {
                                   "href": "{base_uri}/property-types/hostname"
                               }
                           },
                           "id": "hostname",
                           "regex": "^(\\.[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])$",
                           "required": true,
                           "description": "hostname for this node."
                       },
                       "node_id": {
                           "_links": {
                               "self": {
                                   "href": "{base_uri}/property-types/node_id"
                               }
                           },
                           "id": "node_id"
                           "regex": "^.*$",
                           "required": false,
                           "description": ""
                       }
                   },
                   "description": "A single Compute Node."
               },
               {
                   "_links": {
                       "self": {
                           "href": "{base_uri}/item-types/libvirt-system"
                       },
                       "base-type": {
                           "href": "{base_uri}/item-types/system"
                       }
                   },
                   "id": "libvirt-system",
                   "properties": {
                       "system_name": {
                           "_links": {
                               "self": {
                                   "href": "{base_uri}/property-types/basic_string"
                               }
                           },
                           "regex": "^[a-zA-Z0-9\\-\\._]+$",
                           "id": "basic_string",
                           "required": true,
                           "description": "Name of system."
                       },
                       "disk_size": {
                           "_links": {
                               "self": {
                                   "href": "{base_uri}/property-types/libvirt_disk_size"
                               }
                           },
                           "id": "libvirt_disk_size",
                           "regex": "^[1-9][0-9]{0,}G$",
                           "default": "40G",
                           "required": false,
                           "description": "Size of Virtual Disk in Gigabytes."
                       },
                       "ram": {
                           "_links": {
                               "self": {
                                   "href": "{base_uri}/property-types/libvirt_ram_size"
                               }
                           },
                           "id": "libvirt_ram_size",
                           "regex": "^[1-9][0-9]{2,}M$",
                           "default": "2048M",
                           "required": false,
                           "description": "Size of RAM for Virtual Device in Megabytes."
                       },
                       "cpus": {
                           "_links": {
                               "self": {
                                   "href": "{base_uri}/property-types/libvirt_cpu_number"
                               }
                           },
                           "id": "libvirt_cpu_number",
                           "regex": "^[0-9]+$",
                           "default": "2",
                           "required": false,
                           "description": "Number of CPUs to be given to VM."
                       },
                       "path": {
                           "_links": {
                               "self": {
                                   "href": "{base_uri}/property-types/path_string"
                               }
                           },
                           "id": "path_string",
                           "regex": "^/[A-Za-z0-9\\-\\._/#:\\s*]+$",
                           "default": "/var/lib/libvirt/images",
                           "required": false,
                           "description": "Path for VM image (Please ensure this path has appropriate space for the specified VMs)."
                       },
                       "serial": {
                           "_links": {
                               "self": {
                                   "href": "{base_uri}/property-types/basic_string"
                               }
                           },
                           "id": "basic_string",
                           "regex": "^[a-zA-Z0-9\\-\\._]+$",
                           "required": false,
                           "description": "Serial number of system."
                       }
                   },
                   "description": "libvirt Virtual Machine."
               }
               :
               :
           ]
       }
   }

Example: list an ``item-type`` - node
-------------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/item-types/node

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/item-types/node"
           }
       },
       "id": "node",
       "properties": {
           "hostname": {
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/hostname"
                   }
               },
               "regex": "^(\\.[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])$",
               "id": "hostname",
               "required": true,
               "description": "hostname for this node."
           },
           "node_id": {
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/node_id"
                   }
               },
               "id": "node_id",
               "regex": "^.*$",
               "required": false,
               "description": "id for this node."
           }
       },
       "_embedded": {
           "item": [
               {
                   "_links": {
                       "reference-to": {
                           "href": "{base_uri}/item-types/network-profile-base"
                       }
                   },
                   "id": "network_profile",
                   "default": false,
                   "required": true,
                   "description": "Reference to network-profile-base"
               },
               {
                   "_links": {
                       "reference-to": {
                           "href": "{base_uri}/item-types/os-profile"
                       }
                   },
                   "id": "os",
                   "default": false,
                   "required": true,
                   "description": "Reference to os-profile"
               },
               {
                   "_links": {
                       "reference-to": {
                           "href": "{base_uri}/item-types/system"
                       }
                   },
                   "id": "system",
                   "default": false,
                   "required": true,
                   "description": "Reference to system"
               },
               {
                   "_links": {
                       "ref-collection-of": {
                           "href": "{base_uri}/item-types/ip-range"
                       }
                   },
                   "id": "ipaddresses",
                   "max": 50,
                   "min": 1,
                   "description": "Ref-collection of ip-range"
               },
               {
                   "_links": {
                       "ref-collection-of": {
                           "href": "{base_uri}/item-types/software-item"
                       }
                   },
                   "id": "items",
                   "max": 9999,
                   "min": 0,
                   "description": "Ref-collection of software-item"
               },
               {
                   "_links": {
                       "reference-to": {
                           "href": "{base_uri}/item-types/storage-profile-base"
                       }
                   },
                   "id": "storage_profile",
                   "default": false,
                   "required": true,
                   "description": "Reference to storage-profile-base"
               }
           ]
       },
       "description": "A single Compute Node."
   }

Example: list an ``item-type`` - ip-range
-----------------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/item-types/ip-range

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "base-type": {
               "href": "{base_uri}/item-types/network-range"
           },
           "self": {
               "href": "{base_uri}/item-types/ip-range"
           }
       },
       "id": "ip-range",
       "properties": {
           "subnet": {
               "regex": "^.*$",
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/network"
                   }
               },
               "required": true,
               "description": "Subnet for ip-range.",
               "id": "network"
           },
           "end": {
               "regex": "^[0-9\\.]+$",
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/ipv4_address"
                   }
               },
               "required": true,
               "description": "End address of ip-range.",
               "id": "ipv4_address"
           },
           "start": {
               "regex": "^[0-9\\.]+$",
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/ipv4_address"
                   }
               },
               "required": true,
               "description": "Start address of ip-range.",
               "id": "ipv4_address"
           },
           "address": {
               "regex": "^[0-9\\.]+$",
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/ipv4_address"
                   }
               },
               "required": false,
               "description": "Allocated address from ip-range.",
               "id": "ipv4_address"
           },
           "network_name": {
               "regex": "^[a-zA-Z0-9\\-\\._]+$",
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/basic_string"
                   }
               },
               "required": true,
               "description": "Network name for ip-range. This must be unique to each ip-range.",
               "id": "basic_string"
           },
           "gateway": {
               "regex": "^[0-9\\.]+$",
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/ipv4_address"
                   }
               },
               "required": false,
               "description": "Gateway for ip-range.",
               "id": "ipv4_address"
           }
       },
       "description": "IP address range item."
   }

Example: list an ``item-type`` - libvirt-system
-----------------------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/item-types/libvirt-system

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/item-types/libvirt-system"
           },
           "base-type": {
               "href": "{base_uri}/item-types/system"
           }
       },
       "id": "libvirt-system",
       "properties": {
           "system_name": {
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/basic_string"
                   }
               },
               "regex": "^[a-zA-Z0-9\\-\\._]+$",
               "id": "basic_string",
               "required": true,
               "description": "Name of system."
           },
           "disk_size": {
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/libvirt_disk_size"
                   }
               },
               "regex": "^[1-9][0-9]{0,}G$",
               "id": "libvirt_disk_size",
               "required": false,
               "description": "Size of Virtual Disk in Gigabytes.",
               "default": "40G"
           },
           "ram": {
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/libvirt_ram_size"
                   }
               },
               "regex": "^[1-9][0-9]{2,}M$",
               "id": "libvirt_ram_size",
               "required": false,
               "description": "Size of RAM for Virtual Device in Megabytes.",
               "default": "2048M"
           },
           "cpus": {
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/libvirt_cpu_number"
                   }
               },
               "regex": "^[0-9]+$",
               "id": "libvirt_cpu_number",
               "required": false,
               "description": "Number of CPUs to be given to VM.",
               "default": "2"
           },
           "path": {
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/path_string"
                   }
               },
               "regex": "^/[A-Za-z0-9\\-\\._/#:\\s*]+$",
               "id": "path_string",
               "required": false,
               "description": "Path for VM image (Please ensure this path has appropriate space for the specified VMs).",
               "default": "/var/lib/libvirt/images"
           },
           "serial": {
               "_links": {
                   "self": {
                       "href": "{base_uri}/property-types/basic_string"
                   }
               },
               "regex": "^[a-zA-Z0-9\\-\\._]+$",
               "id": "basic_string",
               "required": false,
               "description": "Serial number of system."
           }
       },
       "_embedded": {
           "item": [
               {
                   "_links": {
                       "collection-of": {
                           "href": "{base_uri}/item-types/disk"
                       }
                   },
                   "id": "disks",
                   "max": 9999,
                   "min": 0,
                   "description": "Collection of disk"
               },
               {
                   "_links": {
                       "collection-of": {
                           "href": "{base_uri}/item-types/nic"
                       }
                   },
                   "id": "network_interfaces",
                   "max": 9999,
                   "min": 0,
                   "description": "Collection of nic"
               }
           ]
       },
       "description": "libvirt Virtual Machine."
   }

.. _property-type-operations:

**************
Property Types
**************

Property Type Schema
--------------------
A ``property-type`` entry can have any of  the following properties:
 - ``description`` - description of the item type
 - ``regex`` - the regular expression which the value supplied must satisfy (e.g.: ^(true)|(false)$ can only be satisfied by "true" or "false")

Example: list all ``property-types``
------------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/property-types

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/property-types"
           }
       },
       "id": "property-types",
       "_embedded": {
           "property-type": [
               :
               :
               {
                   "_links": {
                       "self": {
                           "href": "{base_uri}/property-types/basic_date_format"
                       }
                   },
                   "id": "basic_date_format",
                   "regex": "^([-]?[%]+[Y|m|d|s])*$"
               },
               {
                   "_links": {
                       "self": {
                           "href": "{base_uri}/property-types/digit"
                       }
                   },
                   "id": "digit",
                   "regex": "^[0-9]$"
               },
               {
                   "_links": {
                       "self": {
                           "href": "{base_uri}/property-types/disk_size"
                       }
                   },
                   "id": "disk_size",
                   "regex": "^[1-9][0-9]{0,}[MGT]$"
               },
               {
                   "_links": {
                       "self": {
                           "href": "{base_uri}/property-types/file_mode"
                       }
                   },
                   "id": "file_mode",
                   "regex": "^[0-7]?[0-7][0-7][0-7]$"
               }
               :
               :
           ]
       }
   }

Example: list a ``property-type``
---------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/property-types/hostname

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/property-types/hostname"
           }
       },
       "id": "hostname",
       "regex": "^(\\.[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\\-]{0,61}[a-zA-Z0-9])$",
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
