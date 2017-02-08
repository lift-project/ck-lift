#! /bin/bash

cd ${INSTALL_DIR}/${PACKAGE_SUB_DIR}

sbt compile

if [ "${?}" != "0" ] ; then
  echo "Error: building Lift failed!"
  exit 1
fi

exit 0
