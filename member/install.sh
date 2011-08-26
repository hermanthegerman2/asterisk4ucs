#!/bin/bash

set -e
set -u
shopt -s extglob

cd "`dirname $0`"

. settings.sh

echo "Moving current asterisk configuration to preUCS.bak..."
mkdir -p "$AST_CONF_PATH"
mkdir preUCS.bak
mv "$AST_CONF_PATH"/* preUCS.bak
mv preUCS.bak "$AST_CONF_PATH/"
echo -e "\t\t\t\t\t\t\tdone."

echo "Installing asterisk4UCS' default asterisk configuration..."
cp -r defaultconf/* "$AST_CONF_PATH/"
echo -e "\t\t\t\t\t\t\tdone."

echo "Installing info-texts for UCR variables..."
install -m664 ucr/category.cfg \
			"$UNI_REGINFO_PATH/categories/asterisk_member.cfg"
install -m664 ucr/variables.cfg \
			"$UNI_REGINFO_PATH/variables/asterisk_member.cfg"
echo -e "\t\t\t\t\t\t\tdone."

echo "Setting default values for UCR variables..."
ucr set asterisk/confpath="$ast4ucs_ucr_confpath"
ucr set asterisk/asteriskbin="$ast4ucs_ucr_asteriskbin"
echo -e "\t\t\t\t\t\t\tdone."

echo "Installing directory listener module..."
install -m664 listener/asterisk.py "$UNI_LISTENER_PATH/asterisk.py"
echo -e "\t\t\t\t\t\t\tdone."

echo "Restarting univention directory listener..."
invoke-rc.d univention-directory-listener restart
echo -e "\t\t\t\t\t\t\tdone."

echo "Installation successful."
