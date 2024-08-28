.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

.. _configuring-dependencies-between-plugins-and-extensions:

=======================================================
Configuring Dependencies between Plugins and Extensions
=======================================================

Because plugins and model extensions are built and delivered separately, plugin
developers need a mechanism to mandate that the model extensions they consume
be present. There are two aspects to the declaration of dependencies:
*build-time* and *install-time*. Both **must be** declared in the Project Object
Model (``POM``).

- **Build-time dependencies** are configured by adding ``<dependency>`` elements
  to the ``<dependencies>`` collection in the ``current-dep`` and ``latest-dep`` profiles.

  .. code-block:: xml
    :emphasize-lines: 16-17,24-35,39-40,43-52
    
    <project xmlns="http://maven.apache.org/POM/4.0.0"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.ericsson.nms.litp</groupId>
    <artifactId>ERIClitpnetwork_CXP9030513</artifactId>
    <packaging>rpm</packaging>
    <name>[${project.parent.artifactId}] RPM module</name>
    <description>LITP network plugin implementation</description>
    <properties>
        <bom_version>RELEASE</bom_version>
    </properties>
    ...
            <profiles>
                <profile>
                    <!-- profile to build current specified dependencies -->
                    <id>current-dep</id>
                    ...
                    <properties>
                        <litpcore_version>1.17.16</litpcore_version>
                        <litpnetworkapi_version>1.18.2</litpnetworkapi_version>
                    </properties>
                    <dependencies>
                        <dependency>
                            <groupId>com.ericsson.nms.litp</groupId>
                            <artifactId>ERIClitpcore_CXP9030418</artifactId>
                            <version>${litpcore_version}</version>
                            <type>rpm</type>
                        </dependency>
                        <dependency>
                            <groupId>com.ericsson.nms.litp</groupId>
                            <artifactId>ERIClitpnetworkapi_CXP9030514</artifactId>
                            <version>${litpnetworkapi_version}</version>
                            <type>rpm</type>
                        </dependency>
                    </dependencies>
                </profile>
                <profile>
                    <!-- profile to build latest dependencies as defined by the ci-bom -->
                    <id>latest-dep</id>
                    ...
                    <dependencies>
                        <dependency>
                            <groupId>com.ericsson.nms.litp</groupId>
                            <artifactId>ERIClitpcore_CXP9030418</artifactId>
                            <type>rpm</type>
                        </dependency>
                        <dependency>
                            <groupId>com.ericsson.nms.litp</groupId>
                            <artifactId>ERIClitpnetworkapi_CXP9030514</artifactId>
                            <type>rpm</type>
                        </dependency>
                    </dependencies>
                </profile>
            </profiles>
    </project>


- **Install-time dependencies** are configured by adding ``<require>`` elements
  under the ``<requires>`` collection for the ``rpm-maven-plugin``.

  .. code-block:: xml
    :emphasize-lines: 15,20-22,34-35
    
    <project xmlns="http://maven.apache.org/POM/4.0.0"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.ericsson.nms.litp</groupId>
    <artifactId>ERIClitpnetwork_CXP9030513</artifactId>
    <packaging>rpm</packaging>
    <name>[${project.parent.artifactId}] RPM module</name>
    <description>LITP network plugin implementation</description>
    ...
    <build>
        <plugins>
            <plugin>
                <groupId>org.codehaus.mojo</groupId>
                <artifactId>rpm-maven-plugin</artifactId>
                <extensions>true</extensions>
                <inherited>true</inherited>
                <configuration>
                    <requires>
                        <require>python &gt;= 2.6</require>
                        <require>ERIClitpcore_CXP9030418 &gt;= ${litpcore_version}</require>
                        <require>ERIClitpnetworkapi_CXP9030514 &gt;= ${litpnetworkapi_version}</require>
                    </requires>
                </configuration>
            </plugin>
        </plugins>
    </build>
    ...
    <profiles>
        <profile>
            <id>current-dep</id>
            ...
            <properties>
                <litpcore_version>1.17.16</litpcore_version>
                <litpnetworkapi_version>1.18.2</litpnetworkapi_version>
            </properties>
        ...


.. note::
  The Core extension is delivered by ``ERIClitpcore``, which is already
  declared as a dependency in the skeleton code provided by the Maven
  archetypes for plugins and extensions.

