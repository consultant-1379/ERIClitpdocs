.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. _model_extension_api:

===================
Model Extension API
===================

.. currentmodule:: litp.core.extension

Extensions to the LITP model are delivered by :dfn:`Model Extensions`. A Model
Extension is a Python class that extends class :class:`ModelExtension`.

.. _base-extension-class:

Base Model Extension class
--------------------------

.. autoclass:: litp.core.extension.ModelExtension
    :members:

.. _plugin-api-item-types:

Defining New ItemTypes
----------------------

Model Extensions can define new ItemTypes for use in the LITP model by
overriding the base class's :func:`ModelExtension.define_item_types` method.

Implementations of this method will return a list of
:class:`~litp.core.model_type.ItemType` objects in no particular order:

.. currentmodule:: litp.core.model_type

.. autoclass:: ItemType
    :members: __init__

.. note::
   There are a number of Item Types defined for reuse in the LITP core
   Model Extension. See :doc:`../extensions/core_extension_extension/index`

ItemType Structure
------------------

When defining new ItemTypes, the structure of the item is described using
keyword arguments passed to the :class:`ItemType` constructor. The name of each
argument represents the name of an entry in the ItemType's structure
and its value is an instance of one of the following classes:

.. currentmodule:: litp.core.model_type

* Defining an ItemType property

.. autoclass:: Property
   :members: __init__

* Defining an ItemType View

.. autoclass:: View
   :members: __init__

The static methods that implement views take two parameters, as follows:

.. py:function:: view_method(plugin_api_context, query_item)

.. note::
   The :class:`View` structural elements are evaluated when they are accessed
   from a plugin using the dot-notation. The logic implemented in
   a :class:`View`'s ``callable_method`` may raise a Python exception of
   type :class:`ViewError`. It is the plugin developer's responsibility to
   use ``try`` and ``except`` to catch these exceptions and react accordingly.

.. warning::
   Any :class:`ViewError` exceptions that are not caught in a plugin will be
   propagated and cause plan creation to fail with an ``Internal Server Error``
   response returned to the REST API client.

* Defining a child for an ItemType in the model

.. autoclass:: Child
   :members: __init__

* Defining a collection under an ItemType in the model

.. autoclass:: Collection
   :members: __init__

* Defining a reference to an item under an ItemType in the model

.. autoclass:: Reference
   :members: __init__

* Defining a collection of reference to other items under an ItemType in the
  model

.. autoclass:: RefCollection
   :members: __init__

Item Type Validators
--------------------

The constructor for :class:`ItemType` takes a ``validators`` argument, which is
a list of instances of classes that extend
:class:`litp.core.validators.ItemValidator`:

.. autoclass:: litp.core.validators.ItemValidator
    :members: validate

.. currentmodule:: litp.core.validators

When an implementation of :class:`ItemValidator` is called on a Deployment
Model item according to that item's :class:`~litp.core.model_type.ItemType`,
the argument passed to the validator's :func:`ItemValidator.validate`
method is a Python ``dict`` object in which the keys are ``str`` objects
bearing the names of the Item's properties, with the value of each key being
a ``str`` representing the value given by the user to that property.

Model Extension developers who wish to implement their own
:class:`ItemValidator` must do so in their extension module.

.. note::
   Module ``litp.core.validators`` contains a number of implementations
   of :class:`ItemValidator` that can be used by Model Extension authors.
   See :ref:`item-validators`


Defining New PropertyTypes
**************************

.. currentmodule:: litp.core.extension

Model Extensions can define new PropertyTypes for use in the structure of
ItemTypes by overriding the base class's
:func:`ModelExtension.define_property_types` method.

.. currentmodule:: litp.core.model_type

Implementations of this method will return a list of
:class:`PropertyType` objects in no particular order:

.. autoclass:: PropertyType
   :members: __init__

PropertyTypes are constructed with an id, a regex that will be used to
validate values at data input time and an optional list of validator objects
that will be applied at model validation time.

.. note::
   There are a number of Property Types defined for reuse in the LITP core
   Model Extension. See :doc:`../extensions/core_extension_extension/index`


Property Validators
-------------------

.. currentmodule:: litp.core.validators

The constructor for :class:`~litp.core.model_type.PropertyType` takes a
``validators`` argument which is a list of instances of classes that extend
:class:`PropertyValidator` and implement its :func:`PropertyValidator.validate`
method.

.. autoclass:: PropertyValidator
    :members: __init__, validate

.. note::
   Module ``litp.core.validators`` contains a number of implementations
   of :class:`PropertyValidator` that can be used by Model Extension authors
   See :ref:`prop-validators`

.. currentmodule:: litp.migration.base_migration

Model Migration
---------------

Model Extensions can provide model migration scripts to perform changes to the
model between versions. Migrations must extend the :class:`Migration` class:

.. autoclass:: BaseMigration

.. note::
   Examples and more information on migration can be found in the
   plugin SDK at :ref:`model-migration-guide`

A Migration consists of a list of operations. Custom operations can be implemented
by extending the :class:`BaseOperation` class:

.. currentmodule:: litp.migration.operations.base_operation
.. autoclass:: BaseOperation
   :members: mutate_forward, mutate_backward

.. note::
   A set of operations are provided by core for common use cases.
   These can be found at :doc:`operations`


Documenting Model Extensions
****************************

.. currentmodule:: litp.core.model_type

ItemTypes and PropertyTypes defined in Model Extensions are automatically
picked up by the LITP documentation generator and will appear in the following
references:

:doc:`../property_types/index`
    Complete documentation of LITP property types

:doc:`../item_types/index`
    Complete documentation of LITP item types

The content of the documentation pages is derived from the parameters given
when PropertyType and ItemType objects are instantiated in model extensions.

In particular, the ``description`` parameter given for :class:`ItemType`, its
structural elements or :class:`PropertyType` should be descriptive and
informative enough for the resulting Model Extension documentation page to make
sense on its own.

.. note::
  The documentation generator relies on the config file provided by Model
  Extensions (see :ref:`structure`) for discovery.
  No additional action is required to trigger the generation of documentation
  pages for a Model Extension.


