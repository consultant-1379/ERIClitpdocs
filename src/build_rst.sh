#!/bin/sh

# Global section
lib_litp="/target/deps/litp/opt/ericsson/nms/litp/lib/"
lib_gen="/src/generate"

if [ -z "$1" ] ; then 
   echo "Please provide base directory containing pom.xml as an argument for the script"
   exit 1
else
   base_dir=$1
fi

# Setup PYTHONPATH
export PYTHONPATH=${base_dir}${lib_litp}:${base_dir}${lib_gen}:$PYTHONPATH

# Generate Restructured Docs from Plugins
echo "python ${base_dir}/..${lib_gen}/create_sphinx_doc.py -d ${base_dir}/rstFiles -p ${base_dir}/target/deps/litp/opt/ericsson/nms/litp/etc"
python ${base_dir}/..${lib_gen}/create_sphinx_doc.py -d ${base_dir}/rstFiles -p ${base_dir}/target/deps/litp/opt/ericsson/nms/litp/etc
