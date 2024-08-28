#!/bin/bash

set -e
set -x

LITP_ROOT="target/deps/litp/opt/ericsson/nms/litp"

SCHEMA_PATH=$1
if [ "${SCHEMA_PATH}" == "" ]; then
    echo "XML schema path is not specified."
    exit 1
fi
SCHEMA_PATH=${SCHEMA_PATH}/../target/site/attachments

mkdir -p ${SCHEMA_PATH}
TMP_PATH=`mktemp -d --tmpdir=${SCHEMA_PATH}`

[ -f ${SCHEMA_PATH}/litp.zip ] && rm ${SCHEMA_PATH}/litp.zip

mkdir ${TMP_PATH}/xsd
PYTHONPATH=${LITP_ROOT}/lib:${PYTHONPATH} ${LITP_ROOT}/bin/schemawriter.py ${TMP_PATH}/xsd ${LITP_ROOT}/etc/extensions

cd ${TMP_PATH}/xsd
RET=0
zip -r ../litp . || RET=1
cd - >/dev/null

cp rstFiles/attachments/*.txt ${SCHEMA_PATH}
mv ${TMP_PATH}/litp.zip ${SCHEMA_PATH}

rm -rf ${TMP_PATH}

exit ${RET}
