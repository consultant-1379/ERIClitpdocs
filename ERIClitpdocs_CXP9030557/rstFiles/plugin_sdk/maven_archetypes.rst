.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. |br| raw:: html

   <br />

.. _env-maven-arch:

===============================================
Use Maven Archetypes to Build Skeleton Projects
===============================================

Clone the Maven Archetypes and Install them Locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Starting with a Development VM or a compatible distro with the required
dependencies, complete the following steps to clone the LITP/archetypes project:

.. note::
  Before proceeding, you must have access to Git. For more information, see: `Git Setup <https://confluence-oss.lmera.ericsson.se/pages/viewpage.action?pageId=46597455#InstallingJava%2CMavenandGITontheLinuxovertheVirtualMachine.-InstallGIT>`_
 
1. Clone the ``LITP/archetypes`` repository

  .. code-block:: bash

          ~/$ cd workspace/
          ~/workspace$ git clone ssh://<signum>@gerritmirror.lmera.ericsson.se:29418/LITP/archetypes
          ~/workspace$ cd archetypes/
          ~/workspace/archetypes$ ls -1
          buildArchetypes             # Script to build and install all archetypes
          createLITPProject           # Script to create a LITP project from an archetype
          extension-archetype         # Model Extension Maven archetype
          plugin-archetype            # Plugin Maven archetype

2. From the archetypes directory, run ``mvn clean install`` to build and install all the LITP archetypes locally

   (Any warning messages like "`[WARNING] Property 'init' was not specified...`" can be ignored)

  .. code-block:: bash

          ~/workspace/archetypes$ mvn clean install

          [INFO] Scanning for projects...
          [INFO] ------------------------------------------------------------------------
          [INFO] Reactor Build Order:
          [INFO]
          [INFO] litp-extension-archetype
          [INFO] litp-library-archetype
          [INFO] litp-plugin-archetype
          [INFO] litp-puppet-archetype
          [INFO] litp-puppet-extension-archetype
          [INFO] litp-puppet-plugin-archetype
          [INFO] litp-archetypes
          [INFO]
          [INFO] ------------------------------------------------------------------------
          [INFO] Building litp-extension-archetype 1.0.16
          [INFO] ------------------------------------------------------------------------
          ...
          <SNIP>
          ...
          [INFO] Installing /home/user/workspace/archetypes/extension-archetype/pom.xml to /root/.m2/...
          [INFO]
          [INFO] --- maven-archetype-plugin:2.2:update-local-catalog (default-update-local-catalog) @ litp-extension-archetype ---
          ...
          <SNIP>
          ...
          [INFO] ------------------------------------------------------------------------
          [INFO] Reactor Summary:
          [INFO]
          [INFO] litp-extension-archetype .......................... SUCCESS [9.261s]
          [INFO] litp-library-archetype ............................ SUCCESS [0.370s]
          [INFO] litp-plugin-archetype ............................. SUCCESS [0.306s]
          [INFO] litp-puppet-archetype ............................. SUCCESS [0.197s]
          [INFO] litp-puppet-extension-archetype ................... SUCCESS [0.388s]
          [INFO] litp-puppet-plugin-archetype ...................... SUCCESS [0.310s]
          [INFO] litp-archetypes ................................... SUCCESS [0.445s]
          [INFO] ------------------------------------------------------------------------
          [INFO] BUILD SUCCESS
          [INFO] ------------------------------------------------------------------------
          [INFO] Total time: 12.847s
          [INFO] Finished at: Tue Mar 10 10:57:23 EDT 2015
          [INFO] Final Memory: 12M/30M
          [INFO] ------------------------------------------------------------------------


Create an Example LITP Model Extension Using the Maven Archetype
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete the following steps to create a LITP model extension example using the Maven archetype:

1. Use the ``createLITPProject`` script to generate a LITP Model Extension project from the 'litp-extension' Maven archetype

  A valid CXP number should be provided for your new project, see: `CXP Process <https://confluence-oss.seli.wh.rnd.internal.ericsson.com/pages/viewpage.action?pageId=90717427>`_
  |external|. |br|
  The extension name must comply with rpm naming conventions, see: `Naming Convention
  <https://confluence-oss.lmera.ericsson.se/display/CIE/RPM+Packaging#RPMPackaging-NamingConvention>`_
  |external|.

  Call the ``createLITPProject`` script as follows (see working example below):
   ./createLITPProject ``<project_type>`` ``<name>`` ``<classname>`` ``<CXP_number>``
  where:
   ``<project_type>`` is the project type. Enter 'extension' to generate an extension. |br|
   ``<name>`` is the name of the extension (this must be lower case and must not contain underscores). |br|
   ``<classname>`` is the class name for the extension (this must be capitalised and must not contain underscores). |br|
   ``<CXP_number>`` is the correct CXP number for this extension (for example CXP1234567).

  .. code-block:: bash

    # Create LITP Model project from the 'litp-extension' Maven archetype
    ~/workspace/archetypes$ ./createLITPProject extension foo Foo CXP1234567

  This generates an extension named foo_extension with a extension classname named Foo in a folder named ERIClitpfooapi with the CXP number CXP1234567. |br|
  Extensions are named "<name>_extension" so as to differentiate from a plugin which may have the same name. 

  .. code-block:: bash

    ### Generating extension foo
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
    [INFO] Archetype [com.ericsson.nms.litp:litp-extension-archetype:1.0.5] found in catalog local
    [INFO] ----------------------------------------------------------------------------
    [INFO] Using following parameters for creating project from Archetype: litp-extension-archetype:1.0.5
    [INFO] ----------------------------------------------------------------------------
    [INFO] Parameter: groupId, Value: com.ericsson.nms.litp
    [INFO] Parameter: artifactId, Value: ERIClitpfooapi
    [INFO] Parameter: version, Value: 1.0.1-SNAPSHOT
    [INFO] Parameter: package, Value: com.ericsson.nms.litp
    [INFO] Parameter: packageInPathFormat, Value: com/ericsson/nms/litp
    [INFO] Parameter: package, Value: com.ericsson.nms.litp
    [INFO] Parameter: version, Value: 1.0.1-SNAPSHOT
    [INFO] Parameter: groupId, Value: com.ericsson.nms.litp
    [INFO] Parameter: extensionName, Value: foo
    [INFO] Parameter: testPrefix, Value: test
    [INFO] Parameter: extensionClassname, Value: Foo
    [INFO] Parameter: artifactId, Value: ERIClitpfooapi
    [INFO] Parameter: cxpNumber, Value: CXP1234567
    [WARNING] Property 'init' was not specified, so the token in 'src///foo_extension/__init__.py' is not being replaced.
    [WARNING] Property 'init' was not specified, so the token in 'src///__init__.py' is not being replaced.
    [INFO] project created from Archetype in dir: /home/user/workspace/archetypes/ERIClitpfooapi
    [INFO] ------------------------------------------------------------------------
    [INFO] BUILD SUCCESS
    [INFO] ------------------------------------------------------------------------
    [INFO] Total time: 1.676s
    [INFO] Finished at: Wed Sep 17 10:23:59 IST 2014
    [INFO] Final Memory: 9M/116M
    [INFO] ------------------------------------------------------------------------


  A Maven project will be created with the following layout:

  .. code-block:: bash

    ~/workspace/archetypes$ ls -1
        ERIClitpfooapi

    ~/workspace/archetypes$ mv ERIClitpfooapi ~/workspace/
    ~/workspace$ cd ../ERIClitpfooapi/
    ~/workspace/ERIClitpfooapi$ find .
     .
     ./.gitignore
     ./ERIClitpfooapi_CXP1234567
     ./ERIClitpfooapi_CXP1234567/README
     ./ERIClitpfooapi_CXP1234567/pom.xml                     # Used by Maven to build rpm (dependencies can be added here)
     ./test
     ./test/test_foo_extension.py                            # Python unit-tests for model extension
     ./src
     ./src/__init__.py
     ./src/foo_extension
     ./src/foo_extension/__init__.py
     ./src/foo_extension/foo_extension.py                    # Model Extension python code (add item types here)
     ./pom.xml
     ./etc
     ./etc/extensions
     ./etc/extensions/foo_extension.conf
     ./etc/extensions/README.txt
     ./expand_dep_rpms.sh
     ./ats
     ./ats/example_test.at                                   # AT's can be added here (CLI snippets run as tests during build)

  .. note::
    The pom file at ``./pom.xml`` will need to be updated with a LITP integration
    version which matches your target LITP version. The integration version for
    each version of LITP can be found in the
    `LITP Release Notes <https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/LITP2UC/LITP+2+Release+Information>`_.

  .. note::
    The pom file at ``./ERIClitp*_CXP***/pom.xml`` will need to be updated with a
    LITP bom version which matches the target LITP version. The bom version can
    also be found in the `LITP Release Notes <https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/LITP2UC/LITP+2+Release+Information>`_.

2. Use ``mvn clean install`` to build the extension RPM:

  .. code-block:: bash

    ~/workspace/ERIClitpfooapi$ mvn clean install
     [INFO] Scanning for projects...
     [INFO] ------------------------------------------------------------------------
     [INFO] Reactor Build Order:
     [INFO]
     [INFO] ERIClitpfooapi
     [INFO] [ERIClitpfooapi] RPM module
     [INFO]                                                                        
     [INFO] ------------------------------------------------------------------------
     [INFO] Building ERIClitpfooapi 1.0.1-SNAPSHOT
     [INFO] ------------------------------------------------------------------------
     [INFO]
     ...
     <SNIP>
     ...
     [INFO] --- maven-install-plugin:2.4:install (default-install) @ ERIClitpfooapi_CXP1234567 ---
     [INFO] Installing /home/user/workspace/ERIClitpfooapi/ERIClitpfooapi_CXP1234567/target/rpm/
     ERIClitpfooapi_CXP1234567/RPMS/noarch/ERIClitpfooapi_CXP1234567-1.0.1-SNAPSHOT20131128113746.noarch.rpm to
     /home/user/.m2/repository/com/ericsson/nms/litp/ERIClitpfooapi_CXP1234567/1.0.1-SNAPSHOT/ERIClitpfooapi_CXP1234567-1.0.1-SNAPSHOT.rpm
     [INFO] Installing /home/user/workspace/ERIClitpfooapi/ERIClitpfooapi_CXP1234567/pom.xml to
     /home/user/.m2/repository/com/ericsson/nms/litp/ERIClitpfooapi_CXP1234567/1.0.1-SNAPSHOT/ERIClitpfooapi_CXP1234567-1.0.1-SNAPSHOT.pom
     [INFO] ------------------------------------------------------------------------
     [INFO] Reactor Summary:
     [INFO]
     [INFO] ERIClitpfooapi .................................... SUCCESS [1.379s]
     [INFO] [ERIClitpfooapi] RPM module ....................... SUCCESS [3.439s]
     [INFO] ------------------------------------------------------------------------
     [INFO] BUILD SUCCESS
     [INFO] ------------------------------------------------------------------------
     [INFO] Total time: 5.551s
     [INFO] Finished at: Thu Nov 28 11:37:49 GMT 2013
     [INFO] Final Memory: 13M/333M
     [INFO] ------------------------------------------------------------------------


  The built Extension RPM will have the following contents:

  .. code-block:: bash

    # Contents of the built RPM
    ~/workspace/ERIClitpfooapi$ rpm -qpl ERIClitpfooapi_CXP1234567/target/rpm/ERIClitpfooapi_CXP1234567/RPMS/noarch/ERIClitpfooapi_CXP1234567-1.0.1-*.noarch.rpm
     /opt/ericsson
     /opt/ericsson/nms/litp/etc/extensions
     /opt/ericsson/nms/litp/etc/extensions/foo_extension.conf                     # Conf file used to register model extension
     /opt/ericsson/nms/litp/lib
     /opt/ericsson/nms/litp/lib/foo_extension
     /opt/ericsson/nms/litp/lib/foo_extension/__init__.py
     /opt/ericsson/nms/litp/lib/foo_extension/foo_extension.py                    # Model extension python code

Create an Example LITP Plugin Using the Maven Archetype
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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

Repackage a 3PP Puppet Module Using the Maven Archetype
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Complete the following steps to repackage a 3PP Puppet Module using the Maven archetype:

1. Use the ``createLITPProject`` script to generate a puppet module project from the 'litp-puppet' mvn archetype

  A valid CXP number should be provided for your new project, see:
  `CXP Process <https://confluence-oss.seli.wh.rnd.internal.ericsson.com/pages/viewpage.action?pageId=90717427>`_
  |external|. |br|
  The 3PP puppet module must be FOSS approved and a tarball of the
  module must be uploaded in nexus, see: `FOSS Process
  <https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/ELITP/LITP+3PP+Process+-+Commercial+and+FOSS>`_
  |external| and `Uploading Artifacts to Nexus
  <https://confluence-oss.seli.wh.rnd.internal.ericsson.com/display/CIE/Uploading+Artifacts+to+Nexus>`_
  |external|.

  Call  the ``createLITPProject`` script as follows (see working example below):
   ./createLITPProject ``<project_type>`` ``<name>`` ``<version>`` ``<CXP_number>``
  where:
   ``<project_type>`` is the project type. Enter 'puppet' to generate a project to repackage a puppet module. |br|
   ``<name>`` is the name of the puppet module (this must be lower case and must not include underscores). |br|
   ``<version>`` is the version of the puppet module (for example 1.0.2). |br|
   ``<CXP_number>`` is the correct CXP number for this puppet module (for example CXP1234567).

  .. code-block:: bash

    # Create project module project from the 'litp-puppet' Maven archetype
    ~/workspace/archetypes$ ./createLITPProject puppet firewall 1.0.2 CXP1234567

  This generates a project to repackage version 1.0.2 of a puppet module named firewall in a folder named EXTRlitppuppetfirewall with the CXP number CXP1234567.

  .. code-block:: bash

    ### Generating puppet-module firewall
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
    [INFO] Archetype [com.ericsson.nms.litp:litp-puppet-archetype:1.0.1] found in catalog local
    [INFO] ----------------------------------------------------------------------------
    [INFO] Using following parameters for creating project from Archetype: litp-puppet-archetype:1.0.1
    [INFO] ----------------------------------------------------------------------------
    [INFO] Parameter: groupId, Value: com.ericsson.nms.litp
    [INFO] Parameter: artifactId, Value: EXTRlitppuppetfirewall
    [INFO] Parameter: version, Value: 1.0.1-SNAPSHOT
    [INFO] Parameter: package, Value: com.ericsson.nms.litp
    [INFO] Parameter: packageInPathFormat, Value: com/ericsson/nms/litp
    [INFO] Parameter: package, Value: com.ericsson.nms.litp
    [INFO] Parameter: version, Value: 1.0.1-SNAPSHOT
    [INFO] Parameter: moduleName, Value: firewall
    [INFO] Parameter: groupId, Value: com.ericsson.nms.litp
    [INFO] Parameter: moduleVersion, Value: 1.0.2
    [INFO] Parameter: artifactId, Value: EXTRlitppuppetfirewall
    [INFO] Parameter: cxpNumber, Value: CXP1234567
    [INFO] project created from Archetype in dir: /data/LITP/git/external/archetypes/EXTRlitppuppetfirewall
    [INFO] ------------------------------------------------------------------------
    [INFO] BUILD SUCCESS
    [INFO] ------------------------------------------------------------------------
    [INFO] Total time: 1.039s
    [INFO] Finished at: Thu Dec 11 21:03:34 GMT 2014
    [INFO] Final Memory: 8M/116M
    [INFO] ------------------------------------------------------------------------


  A mvn project will be created with the following layout:

  .. code-block:: bash

    ~/workspace/archetypes$ ls -1
        EXTRlitppuppetfirewall

    ~/workspace/archetypes$ mv EXTRlitppuppetfirewall ~/workspace/
    ~/workspace$ cd ../EXTRlitppuppetfirewall/
    ~/workspace/EXTRlitppuppetfirewall$ find .
     .
     ./EXTRlitppuppetfirewall_CXP1234567
     ./EXTRlitppuppetfirewall_CXP1234567/README
     ./EXTRlitppuppetfirewall_CXP1234567/pom.xml             # Main pom (may need updates with explicit module details)
     ./pom.xml

  .. note::
    The pom file at ``./EXTRlitppuppet*_CXP***/pom.xml`` may need to be updated with
    explicit rpm or build dependencies. For more information, see: :ref:`dependencies`.

  .. code-block:: bash

    ~/workspace/EXTRlitppuppetfirewall$ cat EXTRlitppuppetfirewall_CXP1234567/pom.xml
    <SNIP>
      <plugin>
        <groupId>org.codehaus.mojo</groupId>
        <artifactId>exec-maven-plugin</artifactId>
        <version>1.2.1</version>
        <executions>
          <execution>
            <id>rename firewall directory</id>
            <phase>prepare-package</phase>
            <goals>
              <goal>exec</goal>
            </goals>
            <configuration>
              <executable>mv</executable>

              <!-- update the following arguments to match your module -->
              <workingDirectory>${project.build.directory}/puppet</workingDirectory>
              <arguments>
                  <argument>puppetlabs-firewall-1.0.2</argument>
                  <argument>firewall</argument>
              </arguments>
            </configuration>
          </execution>
        </executions>
      </plugin>
    <SNIP>
   <dependencies>
   
    <!-- update the following dependency info to match your module -->
    <dependency>
      <groupId>com.puppetlabs</groupId>
      <artifactId>puppetlabs-firewall</artifactId>
      <version>1.0.2</version>
      <type>tar.gz</type>
    </dependency>
   </dependencies>


2. Use ``mvn clean install`` to build the extension RPM

  .. code-block:: bash

    # Using 'mvn clean install' you can build the plugin RPM
    ~/workspace/ERIClitpbar$ mvn clean install
    [INFO] Scanning for projects...
    [INFO] ------------------------------------------------------------------------
    [INFO] Reactor Build Order:
    [INFO]
    [INFO] EXTRlitppuppetfirewall
    [INFO] [EXTRlitppuppetfirewall] RPM module
    [INFO]
    [INFO] ------------------------------------------------------------------------
    [INFO] Building EXTRlitppuppetfirewall 1.0.1-SNAPSHOT
    [INFO] ------------------------------------------------------------------------
    ...
    <SNIP>
    ...
    [INFO] ------------------------------------------------------------------------
    [INFO] Reactor Summary:
    [INFO]
    [INFO] EXTRlitppuppetfirewall ............................ SUCCESS [1.186s]
    [INFO] [EXTRlitppuppetfirewall] RPM module ............... SUCCESS [2.083s]
    [INFO] ------------------------------------------------------------------------
    [INFO] BUILD SUCCESS
    [INFO] ------------------------------------------------------------------------
    [INFO] Total time: 3.997s
    [INFO] Finished at: Thu Dec 11 22:14:32 GMT 2014
    [INFO] Final Memory: 13M/399M
    [INFO] ------------------------------------------------------------------------


  The built RPM will contain the puppet module:

  .. code-block:: bash

    # Contents of the built RPM
    ~/workspace/ERIClitpbar$ rpm -qpl EXTRlitppuppetfirewall_CXP1234567/target/rpm/EXTRlitp*/RPMS/noarch/EXTRlitppuppet*.rpm
    /opt/ericsson/nms/litp/etc/puppet/modules
    /opt/ericsson/nms/litp/etc/puppet/modules/firewall
    /opt/ericsson/nms/litp/etc/puppet/modules/firewall/manifests           # 3PP Puppet Module
    /opt/ericsson/nms/litp/etc/puppet/modules/firewall/manifests/init.pp
    /opt/ericsson/nms/litp/etc/puppet/modules/firewall/manifests/linux
    /opt/ericsson/nms/litp/etc/puppet/modules/firewall/manifests/linux.pp
    ... ETC ...

