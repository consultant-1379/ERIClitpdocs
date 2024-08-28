Installing The Plugin and Model Extension
=========================================

To install your plugin, complete the following:


1. Create the plugin RPM
2. Create a Model Extension RPM if required
3. Copy the RPMs to a test environment that has LITP installed
4. Copy the new RPMs into the ``/var/www/html/litp`` directory

  .. code-block:: bash
    
    [root@ms ~]# cp <RPMs> /var/www/html/litp

5. Change directory to ``/var/www/html/litp``

  .. code-block:: bash
    
    [root@ms ~]# cd /var/www/html/litp

6. Stop the puppet service

  .. code-block:: bash
    
    [root@ms ~]# service puppet stop

7. Run createrepo

  .. code-block:: bash
    
    [root@ms litp]# createrepo --update . -g comps.xml

  Note: The dot at the end of the command updates the repo in the current
  directory (``/var/www/html/litp`` in this example)

8. Update the yum cache when the litp repository has been recreated

  .. code-block:: bash
    
    [root@ms litp]# cd
    [root@ms ~]# yum clean all

9. Run yum install 'ERIClitpnewplugin...' and yum install 'ERIClitpnewmodelextension...'

  .. code-block:: bash
    
    [root@ms ~]# yum install ERIClitpnewplugin_CXP1234567

  ``yum post-transactions-actions`` will automatically restart the litpd demon.

10. Start the puppet service

  .. code-block:: bash
    
    [root@ms ~]# service puppet start

When a plugin is added to LITP, the ``/opt/ericsson/nms/litp/lib`` directory is
updated and this prompts yum post-transactions-actions to restart the LITP
service. The daemon is restarted once, regardless of the number of LITP
plugin and model extension packages installed.
