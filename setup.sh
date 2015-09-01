#!/bin/bash

PATH_RPWC_DAEMON=/etc/init.d/rpwcweb
PATH_RPWC_DEFAULT=/etc/default/rpwcweb
PATH_RPWC_CONFIG=/etc/rpwcweb
PATH_RPWC_CONTENTS=/var/tmp/rpwcweb/docroot

FILES_TOBE_COPIED="${PATH_RPWC_DAEMON} ${PATH_RPWC_DEFAULT} ${PATH_RPWC_CONFIG}"

COLOR_WARN="\e[31m"
COLOR_BG="\e[47m"
COLOR_OFF="\e[m"

case "$1" in
    "clean")
        sudo rm -rf ${FILES_TOBE_COPIED} ${PATH_RPWC_CONTENTS}
        echo All configuration and contents files have been cleaned.
        exit 0
        ;;
    *)
        python3 setup.py build
        python3 setup.py install

        for FILE in ${FILES_TOBE_COPIED}
        do
            if [ -e ${FILE} ]; then
                echo -e "${COLOR_WARN}${FILE} already exists.${COLOR_OFF}"
            else
                sudo cp -rf .${FILE} ${FILE}
            fi
        done

        if [ -d ${PATH_RPWC_CONTENTS} ]; then
            echo -e "${COLOR_WARN}${PATH_RPWC_CONTENTS} already exists.${COLOR_OFF}"
        else
            mkdir -p ${PATH_RPWC_CONTENTS}
            cp -rf ./templates ./static ${PATH_RPWC_CONTENTS}
        fi
        echo All configuration and contents files have been setup.
        exit 0
        ;;
esac
