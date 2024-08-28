.. _rest-litp-operations:

==========================================
LITP Operations  - LITP |release| REST API
==========================================

###############
LITP Operations
###############

Some LITP functions are available via standard REST interface operations at:

.. code-block:: rest

   {base_uri}/litp

The ``item-type`` of these functions extend ``litp-service-base``. These do not have a model item ``state``.

The /litp ``collection-of-litp-service-base`` is an immutable object listing the available functions exposed by ``LITP``.

.. csv-table::
   :header: "HTTP method", "CRUD operation", "Description", "Status"

   "GET", "READ", "Lists the current collection of ``litp-service-base`` functions", 200
   "PUT", "UPDATE", "Not allowed - returns ``MethodNotAllowedError``", 405
   "POST", "CREATE", "Not allowed - returns ``MethodNotAllowedError``", 405
   "DELETE", "REMOVE", "Not allowed - returns ``MethodNotAllowedError``", 405

Each ``litp-service-base`` object supports ``GET`` operations and may optionally support ``PUT`` operations.

.. csv-table::
   :header: "HTTP method", "CRUD operation", "Description", "Status"

   "GET", "READ", "Requests the current state of a specific ``litp-service-base``", 200
   "PUT", "UPDATE", "Updates an existing ``litp-service-base`` with given parameters", 200
   "POST", "CREATE", "Not allowed - returns ``MethodNotAllowedError``", 405
   "DELETE", "REMOVE", "Not allowed - returns ``MethodNotAllowedError``", 405

Example: Read the content of the ``/litp`` ``litp-service-base-collection``
---------------------------------------------------------------------------

Request URI
^^^^^^^^^^^

.. code-block:: rest

    {base_uri}/litp

Response Body
^^^^^^^^^^^^^

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": "{base_uri}/litp"
           },
           "collection-of": {
              "href": "{base_uri}/item-types/litp-service-base"
           }
       },
       "id": "litp",
       "_embedded": {
           "item": [
               {
                   "_links": {
                       "self": {
                           "href": "{base_uri}/litp/{service}"
                       },
                       "item-type": {
                           "href": "{base_uri}/item-types/litp-service-base"
                       }
                   },
                   "properties": {},
                   "id": "{service}",
                   "item-type-name": "litp-service-base"
               }
           ]
       },
       "item-type-name": "collection-of-litp-service-base"
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
