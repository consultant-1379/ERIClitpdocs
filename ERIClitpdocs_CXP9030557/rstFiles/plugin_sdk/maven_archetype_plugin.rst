.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. |br| raw:: html

   <br />

.. _env-maven-arch-plugin:


Create an Example LITP Plugin Using the Maven Archetype
=======================================================

Complete the following steps to create an example LITP plugin using the Maven archetype:

1. Use the ``createLITPProject`` script to generate a LITP plugin project from the 'litp-plugin' mvn archetype

  A valid CXP number should be provided for your new project, see: `CXP
  Process <https://confluence-oss.seli.wh.rnd.internal.ericsson.com/pages/viewpage.action?pageId=90717427>`_
  |external|. |br|
  The plugin name must comply with rpm naming conventions,
  see: `Naming Convention
  <https://confluence-oss.lmera.ericsson.se/display/CIE/RPM+Packaging#RPMPackaging-NamingConvention>`_
  |external|. 

  Call  the ``createLITPProject`` script as follows (see working example below):
   ./createLITPProject ``<project_type>`` ``<name>`` ``<classname>`` ``<CXP_number>``
  where:
   ``<project_type>`` is the project type. Enter 'plugin' to generate an plugin. |br|
   ``<name>`` is the name of the plugin (this must be lower case and must not include underscores). |br|
   ``<classname>`` is the class name for the plugin (this must be capitalised and must not include underscores). |br|
   ``<CXP_number>`` is the correct CXP number for this plugin (for example CXP1234567).

  .. code-block:: bash

    # Create LITP Plugin project from the 'litp-plugin' Maven archetype
    ~/workspace/archetypes$ ./createLITPProject plugin bar Bar CXP1234567
 
  This generates a plugin named bar with a plugin classname named Bar in a folder named ERIClitpbar with the CXP number CXP1234567. |br|
  Plugins are named with the specified "<name>", they do not receive a "_plugin" suffix. 

  .. code-block:: bash

    ### Generating plugin bar
    [INFO] Scanning for projects...
    [INFO]                                                                         
    [INFO] ------------------------------------------------------------------------
    [INFO] Building Maven Stub Project (No POM) 1
    [INFO] ------------------------------------------------------------------------
    [INFO] 
    [INFO] >>> maven-archetype-plugin:2.2:generate (default-cli) @ standalone-pom >>>
    [INFO] 
    [INFO] <<< maven-archetype-plugin:2.2:generate (default-cli) @ standalone-pom <<<
    [INFO] 
    [INFO] --- maven-archetype-plugin:2.2:generate (default-cli) @ standalone-pom ---
    [INFO] Generating project in Batch mode
    [INFO] Archetype [com.ericsson.nms.litp:litp-plugin-archetype:1.0.9] found in catalog local
    [INFO] ----------------------------------------------------------------------------
    [INFO] Using following parameters for creating project from Archetype: litp-plugin-archetype:1.0.9
    [INFO] ----------------------------------------------------------------------------
    [INFO] Parameter: groupId, Value: com.ericsson.nms.litp
    [INFO] Parameter: artifactId, Value: ERIClitpbar
    [INFO] Parameter: version, Value: 1.0.1-SNAPSHOT
    [INFO] Parameter: package, Value: com.ericsson.nms.litp
    [INFO] Parameter: packageInPathFormat, Value: com/ericsson/nms/litp
    [INFO] Parameter: package, Value: com.ericsson.nms.litp
    [INFO] Parameter: version, Value: 1.0.1-SNAPSHOT
    [INFO] Parameter: groupId, Value: com.ericsson.nms.litp
    [INFO] Parameter: testPrefix, Value: test
    [INFO] Parameter: pluginClassname, Value: Bar
    [INFO] Parameter: pluginName, Value: bar
    [INFO] Parameter: artifactId, Value: ERIClitpbar
    [INFO] Parameter: cxpNumber, Value: CXP1234567
    [WARNING] Property 'init' was not specified, so the token in 'src///__init__.py' is not being replaced.
    [WARNING] Property 'init' was not specified, so the token in 'src///bar_plugin/__init__.py' is not being replaced.
    [WARNING] Property 'init' was not specified, so the token in 'test///test_bar_plugin/__init__.py' is not being replaced.
    [INFO] project created from Archetype in dir: /home/user/workspace/archetypes/ERIClitpbar
    [INFO] ------------------------------------------------------------------------
    [INFO] BUILD SUCCESS
    [INFO] ------------------------------------------------------------------------
    [INFO] Total time: 1.033s
    [INFO] Finished at: Wed Sep 17 17:48:22 IST 2014
    [INFO] Final Memory: 9M/146M
    [INFO] ------------------------------------------------------------------------


  A mvn project will be created with the following layout:

  .. code-block:: bash

    ~/workspace/archetypes$ ls -1
        ERIClitpbar

    ~/workspace/archetypes$ mv ERIClitpbar ~/workspace/
    ~/workspace$ cd ../ERIClitpbar/
    ~/workspace/ERIClitpbar$ find .
     .
     ./.gitignore
     ./test
     ./test/bar_plugin_test
     ./test/bar_plugin_test/test_bar.py                      # Python unit-tests for plugin
     ./test/bar_plugin_test/__init__.py
     ./src
     ./src/__init__.py
     ./src/bar_plugin
     ./src/bar_plugin/bar_plugin.py                          # Main plugin code (start adding to the create_configuration method here)
     ./src/bar_plugin/__init__.py
     ./pom.xml
     ./etc
     ./etc/plugins
     ./etc/plugins/bar_plugin.conf                           # Conf file to register plugin with LITP
     ./etc/plugins/README.txt
     ./expand_dep_rpms.sh
     ./puppet                                                # Puppet modules can be optionally added here
     ./ERIClitpbar_CXP1234567
     ./ERIClitpbar_CXP1234567/README
     ./ERIClitpbar_CXP1234567/pom.xml
     ./ats
     ./ats/example_test.at                                   # AT's can be added here (CLI snippets run as tests during build)

  .. note::
    The pom file at ``./pom.xml`` will need to be updated with a LITP integration
    version which matches your target LITP version. The integration version for
    each version of LITP can be found in the
    `LITP Release Notes <https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/LITP2UC/LITP+2+Release+Information>`_ |external|.

  .. note::
    The pom file at ``./ERIClitp*_CXP***/pom.xml`` will need to be updated with a LITP bom version and any
    rpm or build dependencies. For more information, see: :ref:`dependencies`.


2. Use ``mvn clean install`` to build the extension RPM

  .. code-block:: bash

    # Using 'mvn clean install' you can build the plugin RPM
    ~/workspace/ERIClitpbar$ mvn clean install
    [INFO] Scanning for projects...
    [INFO] ------------------------------------------------------------------------
    [INFO] Reactor Build Order:
    [INFO]
    [INFO] ERIClitpbar
    [INFO] [ERIClitpbar] RPM module
    [INFO]                                                                        
    [INFO] ------------------------------------------------------------------------
    [INFO] Building ERIClitpbar 1.0.1-SNAPSHOT
    [INFO] ------------------------------------------------------------------------
    [INFO]
     ...
     <SNIP>
     ...
     [INFO] Installing /home/user/workspace/ERIClitpbar/ERIClitpbar_CXP1234567/pom.xml to
     /home/user/.m2/repository/com/ericsson/nms/litp/ERIClitpbar_CXP1234567/1.0.1-SNAPSHOT/ERIClitpbar_CXP1234567-1.0.1-SNAPSHOT.pom
     [INFO] ------------------------------------------------------------------------
     [INFO] Reactor Summary:
     [INFO]
     [INFO] ERIClitpbar ....................................... SUCCESS [1.230s]
     [INFO] [ERIClitpbar] RPM module .......................... SUCCESS [3.446s]
     [INFO] ------------------------------------------------------------------------
     [INFO] BUILD SUCCESS
     [INFO] ------------------------------------------------------------------------
     [INFO] Total time: 5.379s
     [INFO] Finished at: Thu Nov 28 12:27:13 GMT 2013
     [INFO] Final Memory: 13M/331M
     [INFO] ------------------------------------------------------------------------


  The built plugin RPM will have the following contents:

  .. code-block:: bash

    # Contents of the built RPM
    ~/workspace/ERIClitpbar$ rpm -qpl ERIClitpbar_CXP1234567/target/rpm/ERIClitpbar_CXP1234567/RPMS/noarch/ERIClitpbar_CXP1234567-1.0.1-*.rpm
    /opt/ericsson
    /opt/ericsson/nms/litp/etc/plugins
    /opt/ericsson/nms/litp/etc/plugins/bar_plugin.conf                      # Conf file used to register the plugin
    /opt/ericsson/nms/litp/lib
    /opt/ericsson/nms/litp/lib/bar_plugin
    /opt/ericsson/nms/litp/lib/bar_plugin/__init__.py
    /opt/ericsson/nms/litp/lib/bar_plugin/bar_plugin.py                     # Plugin Python code

