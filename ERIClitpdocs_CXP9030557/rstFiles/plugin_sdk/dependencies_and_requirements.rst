.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. |br| raw:: html

   <br />


.. _dependencies-and-requirements:


Dependencies and Requirements
=============================

Model Extension and Plugins are developed from templates stored as Maven archetypes. The developer toolkit requires Java, Maven, Python, git and other tools on a Red Hat Enterprise Linux (RHEL) 6.6 distribution or an equivalent distribution, such as Scientific Linux 6.6. The full list of dependencies is below.

To facilitate plugin creation, a Docker container and a virtual machine image are provided with the majority of the setup completed. To use them, either go to the :ref:`env-docker-setup` or :ref:`env-ova-vm-setup` sections listed below.

The following lists the requirements needed to set up a plugin development environment:
 - Access to `Gerrit Central <https://gerrit.ericsson.se/#/settings/ssh-keys>`_
 - Red Hat Enterprise Linux 6.6 (or equivalent) with access to the Internet
 - The packages: libxml2-devel libxslt-devel python-devel rpm-build
 - SSH keys registered with Gerrit Central
 - `Java <http://www.oracle.com/technetwork/java/javase/downloads/jdk7-downloads-1880260.html>`_ |external|
 - `Maven <http://maven.apache.org/download.cgi>`_ |external|
 - `Git <https://code.google.com/p/git-core/downloads/list>`_ |external|
 - Python 2.6 (normally this is pre-installed with RHEL 6.6)
 - The pip `requirements file <https://arm1s11-eiffel004.eiffel.gic.ericsson.se:8443/nexus/content/sites/litp2/ERIClitpdocs/latest/_downloads/litp-requirements.txt>`_
 - The `rubygems file <https://arm1s11-eiffel004.eiffel.gic.ericsson.se:8443/nexus/content/sites/litp2/ERIClitpdocs/latest/_downloads/Gemfile>`_
The section :ref:`env-manual-setup` provides instructions on how to install these.

