.. |external| raw:: html

   <img alt="external" src="../_static/external_link_icon.svg">

LITP |release| XML Schema Definitions
========================================
Overview
========================================


The deployment model can be created "offline" (that is, without using a 
running LITP system) by creating an XML file. To ensure that a deployment
model created in this way is valid, it is strongly recommended to load the
XML Schema Definitions (XSDs) into your XML editor. 

A set of XSDs for the system is available at ``/opt/ericsson/nms/litp/share/xsd``.
This XSD set is automatically generated following a LITP install, or whenever
the LITP service restarts, for example during LITP upgrade, or on update or delete of
plugins.
The parent file, which includes all the other XSDs, is ``litp.xsd``. The
filenames are mapped after the element name they represent, so to get details
on which fields your XML file must contain in order to be validated
successfully against the XSDs, review the contents of the associated XSD file.
In addition, a HTTP GET request can be used to retrieve the parent file
``litp.xsd`` from the system (from the directory ``/opt/ericsson/nms/litp/share/xsd``)
using the following URI:

``https://{host}:9999/xsd/litp.xsd``

A sample set of XSDs is provided below:

`Download ZIP file`_

For more information on using XML and XSDs see LITP Deployment Manager User Guide in the `LITP User Community`_ |external|


.. _Download ZIP file: ../attachments/litp.zip
.. _LITP User Community: https://confluence-oss.lmera.ericsson.se/display/LITP2UC
