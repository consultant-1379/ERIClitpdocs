.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. _logging-messages:

================
Logging Messages
================

.. currentmodule:: litp.core.litp_logging

Plugin and Model Extension developers may want to make use of the logging
subsystem provided by the LITP core. This is particularly useful for debugging
purposes as well as for documenting internal states of a plugin's task
generation logic on the management server when the user runs ``litp create_plan``.

LITP logs are always handled by the :class:`LitpLogger` class, which is built
on top of the native Python logging module.

.. autoclass:: LitpLogger

The :class:`LitpLogger` class offers two logger attributes to Plugin and Model
Extension developers: ``event`` and ``trace``.

These attributes are native `logging.Logger
<http://docs.python.org/2/library/logging.html#logger-objects>`_ |external|
objects. Each object provides a logging method for each severity level
(``critical``, ``error``, ``warning``, ``info`` and ``debug``).
The use-cases for each logger object are as follows:

- The ``event`` logger is used for messages targeted at operations engineers.
  To this end there should be considerable thought given to the log levels
  assigned to events that occur in the system. For example ``event.error`` or
  ``event.critical`` should only be used for log messages that are intended to
  require action from the operations team.

  The ``error`` severity should be reserved for situations where something has
  occurred that is unexpected and that will require operator intervention to
  correct.

  The ``critical`` severity level should be reserved for unexpected events that
  will leave the system in an unusable condition. Exceptions should not
  necessarily always be logged at an ``error`` or ``critical`` level (as they
  may not put the system in an operationally erroneous state), the ``info`` or
  ``warning`` severity levels should be considered based on the operational
  impact of the exception.

- The ``trace`` logger is used to document internal states of a Plugin's
  validation or task generation logic. This logger is intended for use
  primarily as a debugging tool. In general debug logs should be disabled in
  production and only switched on for short periods to catch logs that can be
  used by the development team for debugging purposes.

.. note::
  Messages created by Plugins and Model Extensions are written to
  ``/var/log/messages`` on the management server.

Usage
-----

Each Plugin or Model Extension module that makes use of LITP logging has to
import module ``litp.core.litp_logging`` and create an instance of
:class:`LitpLogger`:

.. code-block:: python

  from litp.core.litp_logging import LitpLogger

  log = LitpLogger()

  def foo():
      log.event.info("foo successfully installed")
      log.trace.info("All done")

