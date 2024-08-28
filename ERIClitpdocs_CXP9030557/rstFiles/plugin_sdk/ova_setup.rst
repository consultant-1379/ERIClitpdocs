.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. |br| raw:: html

   <br />

.. _env-ova-setup:


Using the Provided Ova Virtual Machine
======================================

.. note::
        A docker image is also available which is the recommended approach to take, see :ref:`env-docker-setup`

To set up a developer environment VM, complete the following:

1. Download a copy of the 1.0.8 ova file from: `<https://arm1s11-eiffel004.eiffel.gic.ericsson.se:8443/nexus/content/repositories/prototype/com/ericsson/nms/litp/sdkvm/sdkvm/1.0.8/sdkvm-1.0.8.ova>`_
2. Import it into Oracle VM VirtualBox (version 4.3.12 and above which can be downloaded from `<https://www.virtualbox.org/wiki/Downloads>`_ |external| ) or your preferred VM software.
3. The initial root password on the developer environment VM is ``passw0rd``. You are asked to change this on first login.
4. From the virtual machine make sure you have access to the Internet - you may need to modify the machine settings to achieve this.
5. The FILLME property In /root/.bashrc must be replaced with your XID.
6. The name and email fields in /root/.gitconfig must be updated to contain real information.
7. Generate ssh keys

  .. code-block:: bash

    ssh-keygen -t rsa -f ~/.ssh/id_rsa

8. Register key for Ericsson Gerrit
    - Log into Gerrit account (https://gerrit.ericsson.se/#/settings/ssh-keys)
    - Click ‘Add Key’
    - Paste in the whole line from ~/.ssh/id_rsa.pub (get it using ``cat ~/.ssh/id_rsa.pub``)
    - Click ‘Add’

.. note::
  The networking setup for the VM may vary based upon your environment.

If you are using the Developer Environment VM, you can skip the next section on "RHEL 6.6 Dependencies" and continue to the section entitled ":ref:`plugin-sdk-archetypes`"

.. _env-manual-setup:

