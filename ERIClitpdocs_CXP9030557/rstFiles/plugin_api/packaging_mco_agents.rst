.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. _packaging-mcollective-agents:

============================
Packaging MCollective Agents
============================
:ref:`remote-execution-tasks` and :ref:`callback-tasks` make use of
`Marionette Collective`_ |external| (MCollective) which carries
out actions on the nodes using agents. If a plugin requires remote
execution tasks, the accompanying agents must be placed in the
``puppet/mcollective_agents/files`` directory in order to be packaged inside
the plugin RPM. When the nodes are deployed, the agents are copied onto the
nodes to ``/opt/ericsson/nms/litp/etc/mcollective/mcollective`` directory.
A README.txt file is required, as described in
`Packaging Puppet Modules with Plugins`_.

.. _`Marionette Collective`: http://docs.puppetlabs.com/mcollective/

.. _dependencies:
