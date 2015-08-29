#!/bin/bash

PATH_RPWC_CONFIG=/etc/rpwc
PATH_RPWC_CONTENTS=/var/tmp/rpwc/docroot

case "$1" in
    "clean")
        sudo rm -rf ${PATH_RPWC_CONFIG}
        sudo rm -rf ${PATH_RPWC_CONTENTS}
        echo All configuration and contents files have been cleaned.
        exit 0
        ;;
    *)
        python3 setup.py build
        python3 setup.py install

        if [ -d ${PATH_RPWC_CONFIG} ]; then
            echo ${PATH_RPWC_CONFIG} already exists.
        else
            sudo cp -rf ./etc/rpwc ${PATH_RPWC_CONFIG}
        fi

        if [ -d ${PATH_RPWC_CONTENTS} ]; then
            echo ${PATH_RPWC_CONTENTS} already exists.
        else
            mkdir -p ${PATH_RPWC_CONTENTS}
            cp -rf ./templates ./static ${PATH_RPWC_CONTENTS}
        fi
        echo All configuration and contents files have been setup.
        exit 0
        ;;
esac
