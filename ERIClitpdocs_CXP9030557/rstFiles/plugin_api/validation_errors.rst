.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. _Creating-validation-errors:

==========================
Creating Validation Errors
==========================

.. currentmodule:: litp.core.validators

Validation steps can be implemented in Model Extensions (property validators
and item validators) and Plugins (cross-item validators). All validators
return iterable sequences of :class:`ValidationError` objects.

.. autoclass:: ValidationError
   :members: __init__

It is recommended that you avoid using the
error_message argument to the ValidationError constructor as a way of providing
information about the names of properties or the paths of items on which errors
have been found - the optional ``property_name`` and
``item_path`` parameters are preferred for that purpose.

.. toctree::
   :hidden:

   validators
   puppet
   operations
   deployment_api

.. _logging:

