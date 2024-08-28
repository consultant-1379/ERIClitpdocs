.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. _env-manual-setup:


Manual Setup of a Developer Environment
=======================================
To manually set up a developer environment, complete the following:

.. note::
  A docker image is also available which is the recommended approach to take, see :ref:`env-docker-setup`

1. Git installed and configured with access to Gerrit central (`Git Setup <https://confluence-oss.lmera.ericsson.se/pages/viewpage.action?pageId=46597455#InstallingJava%2CMavenandGITontheLinuxovertheVirtualMachine.-InstallGIT>`_ |external| ).

2. Generate ssh keys

  .. code-block:: bash

    ssh-keygen -t rsa -f ~/.ssh/id_rsa

3. Register key for Ericsson Gerrit
    - Log into Gerrit account (https://gerrit.ericsson.se/#/settings/ssh-keys)
    - Click ‘Add Key’
    - Paste in the whole line from ~/.ssh/id_rsa.pub (get it using ``cat ~/.ssh/id_rsa.pub``)
    - Click ‘Add’

4. Maven installed and configured with access to Gerrit central (`Maven Setup <https://confluence-oss.lmera.ericsson.se/pages/viewpage.action?pageId=46597455#InstallingJava%2CMavenandGITontheLinuxovertheVirtualMachine.-InstallMaven>`_ |external| ).

5. The ``libxml2-devel``, ``libxslt-devel``, ``python-devel`` and ``rpm-build`` packages will need to be installed using yum:

  .. code-block:: bash

    $ sudo yum install libxml2-devel libxslt-devel python-devel rpm-build

6. Python 2.6 is recommended (installed with RHEL 6.6)

  The following dependencies must also be installed:

  .. literalinclude:: ../attachments/litp-requirements.txt

  You can use `pip <https://pypi.python.org/pypi/pip>`_ |external| to install
  these dependencies from the litp-requirements.txt file using the following
  command (depending on your setup you may need to use ``--allow-all-external`` option):

  .. code-block:: bash

        $ sudo pip install -r litp-requirements.txt

  Depending on your network configuration when using pip you may need to add a proxy option; for example ``--proxy=http://www-proxy.ericsson.se:8080``.

  .. note::
    The ``pip`` requirements file for LITP development can be downloaded :download:`here <../attachments/litp-requirements.txt>`.

    If you do not have pip installed, run the following command:

    .. code-block:: bash
    
      $ sudo yum install python-pip

|

7. Puppet and MCollective test dependencies

  The following rubygems must be installed to test Puppet modules and MCollective agents:

  .. literalinclude:: ../attachments/Gemfile

  You can use `bundler <http://bundler.io>`_ |external| to install
  these dependencies using the following command (from the same directory as the Gemfile):

  .. code-block:: bash

        $ bundler install

  .. note::
    The ``Gemfile`` file for LITP development can be downloaded :download:`here <../attachments/Gemfile>`.

    If you do not have bundler installed, run the following command:

    .. code-block:: bash

      $ gem install bundler

