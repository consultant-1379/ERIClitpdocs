.. _rest-api-response_format:

==================================================
REST API response format - LITP |release| REST API
==================================================

################
Response Headers
################

Content-Type
------------
The content-type returned by the REST interface is

.. code-block:: rest

   application/json

HTTP Response Code Mapping
--------------------------
Response headers also contain a HTTP Response Code indicating if an operation completed successfully or the error type in the case of a limited number of errors.
The standard HTTP response codes currently in use are:

.. csv-table::
   :header: "HTTP Code", "Text", "Description"

   "200", "OK", "The request has succeeded"
   "201", "Created", "The request has been fulfilled and resulted in a new resource being created"
   "400", "Bad Request", "The request could not be understood by the server due to malformed syntax"
   "401", "Unauthorised", "The request requires user authentication"
   "404", "Not Found", "The server has not found anything matching the Request-URI"
   "405", "Method Not Allowed", "The method specified in the Request-Line is not allowed for the resource identified by the Request-URI"
   "406", "Not Acceptable", "The requested ``item`` is only capable of generating content which is not acceptable according to the Accept headers send in the request"
   "409", "Conflict", "The request could not be completed due to a conflict with the current state of the resource"
   "422", "Unprocessable", "The request was well formed but was not fully processed due to semantic errors - see ``https://tools.ietf.org/html/rfc4918#section-11.2``"
   "500", "Internal Server Error", "The server encountered an unexpected condition which prevented it from fulfilling the request"
   "503", "Server Unavailable Error", "The request cannot be processed because a service LITP depends on is not currently available."

Example Response header
-----------------------
.. code-block:: rest

   HTTP/1.1 200 OK
   Date: Fri, 18 Oct 2013 14:51:38 GMT
   Content-Length: 857
   Content-Type: application/json

##################
Response structure
##################
When any resource is accessed via an operation, the object being operated upon (or its immediate parent in the case of a successful ``DELETE``) is returned after the operation completes. The general HAL JSON format is as follows:

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": ""
           }
       },
       "properties": {},
       "properties_overwritten": [],
       "applied_properties_determinable": true,
       "id": "",
       "_embedded": {
           "item": [resource_structure]
       },
       "messages": [message_structure]
   }

All fields are optional, and if empty will be removed.

The components in the body of this response are:

_links
------
Links relevant to this ``item``. ``Self`` is the object itself.

.. code-block:: rest

       "_links": {
           "self": {
               "href": ""
           }
       },

Where links to other resources are directly related to the ``self`` object, these will be included in this section, for example:

The ``item-type`` of the ``self`` object

.. code-block:: rest

           "item-type": {
               "href": "{base_uri}/item-types/{item-type-id}"
           }

or the ``item-type`` of the objects contained within the ``self`` collection object

.. code-block:: rest

           "collection-of": {
               "href": "{base_uri}/item-types/{item-type-name}"
           }

or the object the ``self`` object was inherited from:

.. code-block:: rest

           "inherited-from": {
               "href": ""
           }

or the base ``item-type`` of the ``self`` object

.. code-block:: rest

           "base-type": {
               "href": "{base_uri}/item-types/{item-type-id}"
           }

properties
----------
User accessible/updatable properties of the ``item``. As defined by the ``item-types`` schema.

.. code-block:: rest

       "properties": {},

properties-overwritten
----------------------
List of the names of properties that are overwritten in the ``item``. Only defined if ``item`` was created by ``inherit`` command and there are such properties.

.. code-block:: rest

       "properties_overwritten": [],

id
--
The identifier name of the object, relative to its position in the model. This is a unique identifier under the parent item rather than under the entire model tree.

.. code-block:: rest

       "id": "",

_embedded
---------
Sub objects accessible directly from this object. Each object in the list follows the same HAL structure and is of the type of the key for the list.

.. code-block:: rest

       "_embedded": {
           "item": [{
               "_links": {
                   "self": {
                       "href": ""
                   }
               },
               "properties": {},
               "id": ""
               "_embedded": {
                   "item": []
               },
               "messages": []
           }]
       },

Other examples for embedded data types are ``item-types`` and ``property-types``.
| For ``item-type`` operations see :ref:`item-type-operations`
| For ``property-type`` operations see :ref:`property-type-operations`

messages
--------
Messages relating to the request, response or the ``item`` may be returned as a list of ``message_structure`` objects. For information on message handling, please see :doc:`message_handling`

.. code-block:: rest

       "messages": []

Additional properties
---------------------

Any other properties relevant to the ``item`` being returned may be included as key value pairs. For example:

.. code-block:: rest

       "item-type-name": "Deployment",
       "status": "Applied",
       "applied_properties_determinable": true

#################
Message structure
#################

The ``message_structure`` object returns messages directly associated with the "self" object:

.. code-block:: rest

   {
       "_links": {
           "self": {
               "href": ""
           }
       },
       "type": "",
       "message": ""
   }

For information on message handling, please see :doc:`message_handling`

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
