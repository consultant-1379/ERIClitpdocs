.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">


=============================================
LITP |release| Plugin and Model Extension API
=============================================


Required Knowledge and Intended Audience
========================================

This API documentation is written for the use of Plugin and Model Extensions
developers. It is assumed that you have set up a development environment by
following :doc:`../plugin_sdk/env_setup`, have read the :doc:`../plugin_sdk/introduction`
and are proficient in the Python programming language.

Overview
========

The functionality offered by the LITP Deployment Manager can be extended by
means of the Plugin and Model Extension Python APIs.

* Model Extensions are used to extend the scope of the core LITP Deployment
  Model by defining new types of items including their properties and
  structural relationships between item types in the model.

* Plugins are used to implement the task generation logic that determines what
  actions will be performed by the Execution Manager to bring the state of a
  deployment in line with what is described in the Deployment Model.

* Both the Model Extension and Plugin APIs offer validation features that let
  developers issue feedback to the end-user when the Deployment Model is in an
  invalid state.

Plugin and Model Extension API Page:
========================================

The pages below document the Plugin and Model Extension API:

* :ref:`plugin_api`

* :ref:`model_extension_api`

Using the Plugin and Model Extension API:
========================================

The pages below provide guidance on using the API:

* :ref:`Understanding-the-Plugin-and-Model-Extension-Structure`

* :ref:`Configuring-Dependencies-between-Plugins-and-Extensions`

* :ref:`Packaging-Puppet-Modules-with-Plugins`.

* :ref:`Packaging-MCollective-Agents`.

* :ref:`Creating-Validation-Errors`

* :ref:`Logging-Messages`

.. toctree::
  :hidden:

  plugin_model_extension_struct
  packaging_puppet_modules_with_plugins
  packaging_mco_agents
  deps_between_plugins_and_ext
  model_ext_api
  plugin_api
  validation_errors
  logging
