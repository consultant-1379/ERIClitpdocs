.. _litp-sdk:

LITP |release| Plugin SDK
==========================

This is the documentation home for the LITP Plugin SDK. LITP 2.x delivers an
SDK which provides documentation and tools so that you can set up your
environment, navigate the Plugin API and write a LITP plugin. We welcome all
feedback on the SDK.
We invite you to raise suggestions for improvements in the future versions of
the SDK - which will form the input for future stories. Please create an issue
in JIRA Project "LITP CDS", Issue Type – "Improvement" and Summary –
"Plugin SDK Feedback".


.. _plugin-dev-doc:

Plugin Development Documentation
-----------------------------------

The documentation provided here will get you started developing plugins for
LITP:

- :doc:`developer_guide`

  This page provides detailed information on plugin development, including plugin
  validation and the methods that need to be implemented in a plugin and
  model extension. This guide outlines the steps to get started writing a LITP
  plugin.

- :doc:`model_migration`

  This page includes information on LITP's migration facility for the item
  types defined in model extensions.

- :doc:`../plugin_api/index`

  This document is the LITP plugin API description. It provides information on
  plugin structure, model extension methods, item type structure, plugin methods,
  plugin validation and item and property types.

The developer's guide and API description are meant to complement each other.
If you are new to LITP or plugin development, you will find the
:doc:`developer_guide` a great place to begin.

.. _deployment-model-info:

Core Deployment Model Information
-----------------------------------

The documents listed below provide detailed information on the core item types
and property types that can be extended by Model Extension developers:

- `Core Item Types <../extensions/core_extension_extension/index.html#defined-item-types>`_

- `Core Property Types <../extensions/core_extension_extension/index.html#defined-property-types>`_

.. seealso::

   :ref:`user-deployment-model-info`
     For the full lists of Plugins, Model Extensions, Item Types and Property Types

.. _reference-doc:

Reference Documentation
----------------------------

The following references may be useful in your plugin development efforts.

- :doc:`../xml_schema/index`

- :doc:`../rest_api/index`


.. toctree::
  :hidden:

  developer_guide
  model_migration
  ../plugin_api/index
  ../plugin_api/snapshot_api
