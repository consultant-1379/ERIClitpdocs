.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. |br| raw:: html

   <br />

.. _env-maven-arch-ext:


Create an Example LITP Model Extension Using the Maven Archetype
================================================================

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



