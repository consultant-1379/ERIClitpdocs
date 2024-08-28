.. _rest-api-crud:

===============================================================
REST API and CRUD Operations overview - LITP |release| REST API
===============================================================

########################
REST API CRUD Operations
########################

********
Overview
********

The LITP REST API follows a set of REST conventions to allow client applications make HTTP requests and receive responses for ``CREATE``, ``READ``, ``UPDATE`` and ``DELETE`` (CRUD) operations to the LITP Deployment Model.

****************
REST Conventions
****************

Operations
----------
Client applications make requests using standard HTTP methods to specify what action is to be done in a specified URL.

.. csv-table::
   :header: "REST operation", "CRUD operation", "Description"

   :ref:`rest-post-operations`, "CREATE", "Creates a new ``item`` instance in the model."
   :ref:`rest-get-operations`, "READ", "Requests the details of a specific ``item`` or a list of ``items``."
   :ref:`rest-put-operations`, "UPDATE", "Updates an existing ``item`` with given parameters."
   :ref:`rest-delete-operations`, "DELETE", "Removes an existing ``item`` and everything below that ``item`` in the model."

Items
-----
Client applications make requests against LITP model items. These are either objects or collections of objects.

This returns a list of all of the items of the named type

.. code-block:: rest

   {item_name}s

This returns the attributes of the identified ``item``:

.. code-block:: rest

   /{item_name}s/{specific_item_id}

This refers to the ``items`` found after navigating the ``item`` tree composed of ``items``:

.. code-block:: rest

   /{item_name}s/{specific_item_id}/{child_item}

The plural form of adding *s* is for example purposes only. Some plurals may not be expressed in this way.

Base URI
--------
The base Uniform Resource Identifier (URI) is:

.. code-block:: rest

   https://{host}:{port}/{application}/{REST API version}/

The form {base_uri} used in examples refers to this expansion.

The base URI application for LITP is (``litp/rest``)

Versioning
----------
REST API versioning, initially ``v1``, is used for managing the major versions of the REST API itself. This should not be confused with changes in the structure or content of items delivered by the REST API.

For example, to query the structure of a specific deployment (``deployment1``), a HTTP ``GET`` is used against the ``item`` in the URI below:

.. code-block:: rest

   https://{host}:{port}/{application}/{REST API version}/deployments/deployment1

Item and Property Type Discovery
--------------------------------
All ``item-types`` are registered in the system. These are found under

.. code-block:: rest

   https://{host}:{port}/{application}/{REST API version}/item-types

and ``property-types`` associated with items are found under

.. code-block:: rest

   https://{host}:{port}/{application}/{REST API version}/property-types

------------
 REST Pages
------------
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

.. toctree::
   :hidden:

   request_format
   response_format
   POST_operation
   GET_operation
   PUT_operation
   DELETE_operation
   Plan_operation
   snapshot_operations
   item_discovery
   message_handling
   litp_operations
