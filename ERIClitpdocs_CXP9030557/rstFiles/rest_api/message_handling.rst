.. _rest-message-handling:

==========================================
Message Handling - LITP |release| REST API
==========================================

Messages can be returned for any operation as part of the response object. There are two defined message types: Error and Warning.

Error Types
-----------

.. csv-table::
   :header: "Message Type", "Description"

   "CardinalityError", "``Plan`` ``item`` fails property validation"
   "ChildNotAllowedError", "Item not allowed"
   "HeaderNotAcceptableError", "Invalid header type in request"
   "InternalServerError", "Error occurred processing the request"
   "ItemExistsError", "Item already exists"
   "InvalidChildTypeError", "Invalid ``item`` for location"
   "InvalidLocationError", "Wrong path is given"
   "InvalidReferenceError", "Invalid reference for location"
   "InvalidRequestError", "Invalid request"
   "InvalidTypeError", "Type doesn't exist"
   "InvalidXMLError", "Error occurred processing the XML"
   "MethodNotAllowedError","Unsupported action at location"
   "MissingRequiredItemError", "``Plan`` missing required ``item``"
   "MissingRequiredPropertyError", "Property missing from ``item``"
   "DoNothingPlanError", "``Plan`` ``item`` failed, no tasks generated"
   "PropertyNotAllowedError", "Invalid property value"
   "ServerUnavailableError", "Server is not available"
   "UnallocatedPropertyError", "Missing property value"
   "ValidationError", "Property value fails validation rule"
   "CredentialsNotFoundError", "Authentication credentials not found in keyring"

Warning Types
-------------

.. csv-table::
   :header: "Message Type", "Description"

   "DeprecationWarning", "The ``item`` is set for removal in a subsequent release"

Message Structure
-----------------

The structure of each message is as follows:

.. code-block:: rest

   {
       "_links": {
           "self": {"href": ""}
       },
       "type": "",
       "message": ""
   }

Additional properties
---------------------

Any other properties relevant to the ``message`` being returned may be included as key value pairs if they exist on the object being operated on. For example:

.. code-block:: rest

   "internalErrorCode": 2SAE33,
   "developerMessage": "Specific message to help developers solve the issue",
   "localisedMessage": {
       "locale" : "",
       "message" : "Translated message"
   }
   "time": “2013-04-30T10:27:12”

Sample structure of messages list
---------------------------------

.. code-block:: rest

   "messages": [
       {
           "_links": {
               "self": {"href": uri}
           },
           "type": "ValidationError",
           "message": "Invalid value: 'null' for property 'hostname'"
       },
       {
           "_links": {
               "self": {"href": uri}
           },
           "type": "MissingRequiredPropertyError",
           "message": "ItemType 'os-profile' is required to have a 'property' with id 'path' and type 'file_path_string'"
       },
       {
           "_links": {
               "self": {"href": uri}
           },
           "type": "ItemExistsError",
           "message": "Item already exists in model: rhel7"
       }
   ]

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
