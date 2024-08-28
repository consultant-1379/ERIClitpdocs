.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. |br| raw:: html

   <br />

.. _env-maven-arch-puppet:

=======================================================
Repackage a 3PP Puppet Module Using the Maven Archetype
=======================================================

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

