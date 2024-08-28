.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. |br| raw:: html

   <br />
.. warning::
 The **selidocker** docker registry is temporarily unavailable. Steps given below will no longer work as expected.
.. _env-docker-setup:

Using the Docker Development Container
======================================

To set up the development container, complete the following steps:

1. Install Docker by following the appropriate instructions for your operating system as detailed in the Docker documentation: `<https://docs.docker.com/engine/installation/>`_ |external|

2. Log in using your Ericsson credentials and download the Docker container image using the following commands:
   (You are prompted for your Ericsson signum / XID, your Ericsson password and your email address.)

  .. code-block:: bash

    docker login selidocker.lmera.ericsson.se
    docker pull selidocker.lmera.ericsson.se/proj_enm/sdk_container:latest

3. Run the SDK Docker container, mounting your workspace directory as follows:

  **On Linux:**

  .. code-block:: bash

    docker run -v <MY_WORKSPACE>:/root -w=/root/ -i -t selidocker.lmera.ericsson.se/proj_enm/sdk_container bash

  Where ``<MY_WORKSPACE>`` is your home directory ("/home/${USER}") within which you have cloned your plugin.


  **On Windows:**

  .. code-block:: bash

    docker run -v <MY_WORKSPACE>:/root -w=/tmp/ -i -t selidocker.lmera.ericsson.se/proj_enm/sdk_container bash

  Where ``<MY_WORKSPACE>`` must be a directory under the Windows User directory ("/c/Users/<USER>/workspace") within which you have cloned your plugin.

  .. note::

    Depending on your Docker installation, `sudo` may be needed in the commands listed above.
    If your host OS is Linux, you may need to set SELinux to be in permissive mode.

  It may also be helpful to add the following (or similar) aliases to your bash profile:

  .. code-block:: bash

    # Run the supplied command in the LITP SDK build container, for example, "dk-litp mvn clean install"
    alias dk-litp='docker run -v /home/${USER}:/root -w=`pwd | sed "s/\/home\/${USER}/\/root/"` -i -t selidocker.lmera.ericsson.se/proj_enm/sdk_container
    # Run "bash" in the LITP SDK build container
    alias dk-bash="dk-litp bash"
    # Run "mvn clean install" in the LITP SDK build container
    alias dk-mvnci="dk-litp mvn clean install"
