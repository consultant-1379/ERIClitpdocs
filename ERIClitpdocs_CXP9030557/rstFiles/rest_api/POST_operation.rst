.. _rest-post-operations:

========================================
POST Operation - LITP |release| REST API
========================================

##############
POST Operation
##############

********
Overview
********

The REST API POST operation maps to the ``CREATE`` operation to create a new ``item`` instance in the model.
Properties should be supplied in correct key/value pairs with no duplicates as described in ``RFC 4627`` for the ``application/json`` media type (http://tools.ietf.org/html/rfc4627#section-2.2).
If any key/value pair in the current implementation has the same key as an existing pair, the value of the new pair replaces that of the existing pair.

The operation returns the newly created ``item`` after completion.

Request Structure
-----------------

.. csv-table::
   :header: "Component", "Example", "Description"

   "Request Location/URI", "``{base_uri}/deployments/d1/clusters/c1``", "URI to be operated upon"
   "Content Type", "``Content-Type:application/json``", "content type of data in payload"
   "Request Data", "``{'id': 'c1', 'type': 'cluster', 'properties':{'ha_manager':'vcs'}}``", "``POST`` JSON data"
   "Request Type", "``POST``", "HTTP method"

Request POST Data
^^^^^^^^^^^^^^^^^
Request POST data has the following form

.. code-block:: rest

   {
       "id": "",
       "type": "",
       "properties": {}
   }

``id`` is the identifier of the item being created, 
``type`` is the ``item-type`` of the item being created and
``properties`` are key value pairs that are validated against the ``item-type`` properties

When creating an inherited item, the key ``inherit`` replaces ``type`` and its value contains the path of the source item, while the ``properties`` contains the overwritten properties.

.. code-block:: rest

   {
       "id": "",
       "inherit": "",
       "properties": {}
   }

Response Header
---------------

The Header includes the HTTP status code for after the operation and the ``Content-Type`` of the response data.

.. code-block:: rest

   HTTP/1.1 201 Created
   Date: Fri, 18 Oct 2013 14:51:38 GMT
   Content-Length: 857
   Content-Type: application/json

Example: Create an ``item`` - ``os-profile``
--------------------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/software/profiles

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       "id": "rhel_6_6",
       "type": "os-profile",
       "properties": {
           "name": "sample-profile",
           "path": "/profiles/node-iso/"
       }
   }

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
    "item-type-name": "os-profile",
    "state": "Initial",
    "applied_properties_determinable": true,
    "_links": {
        "self": {
            "href": "{base_uri}/software/profiles/rhel_6_6"
        },
        "item-type": {
            "href": "{base_uri}/item-types/os-profile"
        }
    },
    "id": "rhel_6_6",
    "properties": {
        "name": "sample-profile",
        "kopts_post": "console=ttyS0,115200",
        "breed": "redhat",
        "version": "rhel6",
        "path": "/profiles/node-iso/",
        "arch": "x86_64"
    }
   }

Example: Inherit an item - ``os-profile``
-----------------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/deployments/d1/clusters/cluster1/nodes/node1

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       "id": "os",
       "inherit": "/software/profiles/os-profile1",
       "properties": {
           "name": "sample-profile"
       }
   }

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

    {
        "properties-overwritten": [
            "name"
        ],
        "required": "system",
        "id": "os",
        "applied_properties_determinable": true,
        "item-type-name": "reference-to-os-profile",
        "state": "Initial",
        "_links": {
            "inherited-from": {
                "href": "{base_uri}/software/profiles/os-profile1"
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
            "path": "/profiles/node-iso/",
            "arch": "x86_64"
        }
    }


Example: Create a ``plan``
--------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

   {base_uri}/plans/

Request Body
^^^^^^^^^^^^

.. code-block:: rest

   {
       "id": "plan",
       "type": "plan"
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
       "state": "valid"
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
