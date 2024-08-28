Developer Troubleshooting Guide
================================

The document provides information for developers to help troubleshoot common development issues.

Common Issues
^^^^^^^^^^^^^

Listed below are common developer issues and solutions to these issues:

1. python-crypto attribute errors
---------------------------------

  If you experience attribute errors similar to those listed below, the most likely cause is conflicting python-crypto versions.

  .. code-block:: bash

      Traceback (most recent call last):
      File "/usr/lib/python2.6/site-packages/nose/loader.py", line 413, in loadTests 
      FromName
      addr.filename, addr.module)
      "/usr/lib/python2.6/site-packages/nose/importer.py", line 47, in importFromPath
      ...
      File "/root/ERIClitpamanda/target/deps/opt/ericsson/nms/litp/lib/libp/core/callbackapi.py", line 12, in <module>
      from litp.encryption.encryption import EncryptionAES
      File "/root/ERIClitpamanda/target/deps/opt/ericsson/nms/litp/lib/litp/encryption/encryption.py", line 15, in <module>
      from Crypto.Util.randpool import RandomPool
      ...
      from Crypto.Util.number import ceil_shift, exact_log2, exact_div
      File "/usr/lib64/python2.6/site-packages/Crypto/Util/number.py", line 56, module>
      if _fastmath is not None and not _fastmath.HAVE_DECL_MPZ_POWM_SEC:
      AttributeError: 'module' object has no attribute 'HAVE_DECL_MPZ_POWM_SEC

  Run the following commands to resolve this issue:

  .. code-block:: bash

      sudo pip uninstall pycrypto
      sudo yum erase python-crypto
      sudo pip install pycrypto==2.6.1

2. Item type not found in plugin AT
-----------------------------------

  Accelerated tests may need to reference item types delivered by model
  extensions.

  These tests will fail with output similar to the following if the
  extension delivering these item types is not present when the tests are
  executed.

  ::

    Item type not registered: libvirt-provider

3. Removal of plugins and extensions
------------------------------------

  Removal of plugins and model extensions is only possible if the model
  items associated with the plugins or extensions are first removed from
  the model.

  If a plugin or model extensions is attempted to be removed
  while items still exist in the model, the user will get an error with
  the litpd service failing to restart.

  Example removing of a ERIClitpexample plugin:

  .. code-block:: bash

      # Remove associated items from the model and run a plan
      litp remove -p /software/services/example1
      litp create_plan
      litp run_plan

      # Remove plugin and extension after the plan has complete successfuly
       yum remove ERIClitpexample ERIClitpexampleapi


4. Clean up of the LITP Model
-----------------------------
  While a plugin is being developed the item types defined may undergo a lot
  of change. This may result in the need to clean up a model which may contains
  old model items which are inconsistent with the updated item types.

  This should only be in a development environment.

  Example model clean up :

  .. code-block:: bash

     # Stop the litpd service
     service litpd stop
     # Clean out the current model
     rm -f /var/lib/litp/core/model/*
     # Restart the litpd service
     service litpd start


5. Failed Plan While Applying a Config Task
-------------------------------------------
  If the plan failed while applying a :py:class:`litp.core.task.ConfigTask`,
  a copy of the failed Puppet manifest is logged in
  /opt/ericsson/nms/litp/etc/puppet/manifests/plugins.failed/filename.pp and
  should be reviewed. Note: filename.pp is a placeholder relating to the host
  for which it was generated (e.g. node1.pp). The resource which caused the
  failure will be present in these files. This resource can be isolated by 
  comparing these files to the current manifests, for example:

  .. code-block:: bash

    [root@ms1 ~]# diff -r /opt/ericsson/nms/litp/etc/puppet/manifests/plugins/ms1.pp  /opt/ericsson/nms/litp/etc/puppet/manifests/plugins.failed/ms1.pp
    1a2,8
    > class task_ms1__package__qwerty(){
    >     package { "qwerty":
    >         ensure => "installed",
    >         require => []
    >     }
    > }
    >
    21a29,32
    >     class {'task_ms1__package__qwerty':
    >     }
    >
    >

  The backup manifest files are also useful for debugging complex Puppet
  failures when the Puppet logs point to the failing line in the manifest.
