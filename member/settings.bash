

UNI_REGINFO_PATH=/etc/univention/registry.info
UNI_LISTENER_PATH=/usr/lib/univention-directory-listener/system
AST_PREFIX=/
AST_CONF_PATH="$AST_PREFIX"etc/asterisk
UNI_JOIN_PATH=/usr/lib/univention-install/

# --------------- UCR Settings -------------------------

## Confpath:
## In diesem Verzeichnis werden die automatisch generierten Asterisk-Configs
## abgelegt.
ast4ucs_ucr_confpath="$AST_CONF_PATH/ucs_autogen"

## Asteriskbin:
## Der Pfad zur ausführbaren Asterisk-Binary.
#ast4ucs_ucr_asteriskbin=/usr/sbin/asterisk
ast4ucs_ucr_asteriskbin="$AST_PREFIX"sbin/asterisk

