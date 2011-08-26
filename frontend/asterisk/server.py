# coding=utf-8

import univention.admin.filter
import univention.admin.handlers
from univention.admin.handlers import asterisk
import univention.admin.syntax
import time

module = "asterisk/server"
childs = 1
short_description = u"Asterisk-Server"
long_description = u"Asterisk-Server"
operations = ['add', 'edit', 'remove', 'search', 'move']
options = {}

layout = [
	univention.admin.tab('Allgemein', 'Allgemeine Einstellungen', [
		[ univention.admin.field("commonName") ],
		[ univention.admin.field("host") ],
		[ univention.admin.field("lastupdate_gui"),
			univention.admin.field("apply") ],
	]),
	univention.admin.tab('Vorwahlen', 'Gesperrte Vorwahlen', [
		[ univention.admin.field("blockedAreaCodes"),
			univention.admin.field("blockInternational") ],
	]),
	univention.admin.tab('Anrufbeantworter', 'Anrufbeantworter', [
		[ univention.admin.field("mailboxMaxlength") ],
		[ univention.admin.field("mailboxEmailsubject"),
			univention.admin.field("mailboxEmailbody") ],
		[ univention.admin.field("mailboxEmaildateformat"),
			univention.admin.field("mailboxAttach") ],
		[ univention.admin.field("mailboxMailcommand") ],
	]),
	univention.admin.tab('Musik', 'Warteschlangenmusik', [
		[ univention.admin.field("music") ],
	], advanced=True),
	univention.admin.tab('Nummernkreise', 'Nummernkreise', [
		[ univention.admin.field("extnums"),
			univention.admin.field("defaultext") ],
	], advanced=True),
]

property_descriptions = {
	"commonName": univention.admin.property(
		short_description="Name",
		syntax=univention.admin.syntax.string,
		identifies=True,
		required=True
	),
	"host": univention.admin.property(
		short_description="Host",
		syntax=univention.admin.syntax.LDAP_Search(
                        filter="objectClass=univentionHost",
                        attribute=['computers/computer: name'],
                        value='computers/computer: dn',
                ),
		required=True
	),
	"lastupdate": univention.admin.property(
		syntax=univention.admin.syntax.integer,
	),
	"lastupdate_gui": univention.admin.property(
		short_description=u"Konfiguration zuletzt eingespielt am:",
		syntax=univention.admin.syntax.string,
		editable=False,
	),
	"apply": univention.admin.property(
		short_description=u"Konfiguration jetzt einspielen?",
		syntax=univention.admin.syntax.boolean,
		default=False,
	),
	"configs": univention.admin.property(
		syntax=univention.admin.syntax.string,
		multivalue=True,
	),
	"blockedAreaCodes": univention.admin.property(
		short_description=u"Blockierte Vorwahlen",
		syntax=univention.admin.syntax.string,
		multivalue=True,
	),
	"blockInternational": univention.admin.property(
		short_description=u"Auslandsgespräche blockieren",
		long_description=u"Blockiert die Vorwahlen 00 und +",
		syntax=univention.admin.syntax.boolean,
		default=False,
	),
	"music": univention.admin.property(
		short_description="Installierte Musikklassen",
		syntax=univention.admin.syntax.string,
		multivalue=True,
		default=["moh"],
	),
	"extnums": univention.admin.property(
		short_description="Eigene externe Rufnummer(n)",
		syntax=univention.admin.syntax.phone,
		multivalue=True,
	),
	"defaultext": univention.admin.property(
		short_description="Standard-Extension",
		syntax=univention.admin.syntax.phone,
	),
	"mailboxMaxlength": univention.admin.property(
		short_description=u"Maximale Länge einer Sprachnachricht (Sekunden)",
		syntax=univention.admin.syntax.integer,
		required=True,
		default="300",
	),
	"mailboxEmailsubject": univention.admin.property(
		short_description="Betreff der eMails",
		syntax=univention.admin.syntax.string,
		required=True,
		default="New message from ${VM_CALLERID}",
	),
	"mailboxEmailbody": univention.admin.property(
		short_description="Textkörper der eMails",
		syntax=univention.admin.syntax.long_string,
		required=True,
		default="Hello ${VM_NAME},\n\nThere is a new message " + \
			"in mailbox ${VM_MAILBOX}.",
	),
	"mailboxEmaildateformat": univention.admin.property(
		short_description="Datumsformat in eMails",
		syntax=univention.admin.syntax.string,
		required=True,
		default="%d.%m.%Y %H:%M",
	),
	"mailboxAttach": univention.admin.property(
		short_description="Sprachnachricht an eMails anhängen?",
		syntax=univention.admin.syntax.boolean,
		required=True,
		default="1",
	),
	"mailboxMailcommand": univention.admin.property(
		short_description="Befehl zum Versenden der eMails",
		long_description=u"Programm zum Versenden von E-Mails " + \
			"(unbedingt den absoluten Pfad angeben!)",
		syntax=univention.admin.syntax.string,
		required=True,
		default="/usr/sbin/sendmail -t",
	),
}

mapping = univention.admin.mapping.mapping()
mapping.register("commonName", "cn",
	None, univention.admin.mapping.ListToString)
mapping.register("host", "ast4ucsServerHost",
	None, univention.admin.mapping.ListToString)
mapping.register("lastupdate", "ast4ucsServerLastupdate",
	None, univention.admin.mapping.ListToString)
mapping.register("configs", "ast4ucsServerConfig")
mapping.register("blockedAreaCodes", "ast4ucsServerBlockedareacode")
mapping.register("music", "ast4ucsServerMusic")
mapping.register("extnums", "ast4ucsServerExtnum")
mapping.register("defaultext", "ast4ucsServerDefaultext",
	None, univention.admin.mapping.ListToString)

mapping.register("mailboxMaxlength", "ast4ucsServerMailboxmaxlen",
	None, univention.admin.mapping.ListToString)
mapping.register("mailboxEmailsubject", "ast4ucsServerMailboxemailsubject",
	None, univention.admin.mapping.ListToString)
mapping.register("mailboxEmailbody", "ast4ucsServerMailboxemailbody",
	None, univention.admin.mapping.ListToString)
mapping.register("mailboxEmaildateformat", "ast4ucsServerMailboxemaildateformat",
	None, univention.admin.mapping.ListToString)
mapping.register("mailboxAttach", "ast4ucsServerMailboxattach",
	None, univention.admin.mapping.ListToString)
mapping.register("mailboxMailcommand", "ast4ucsServerMailboxemailcommand",
	None, univention.admin.mapping.ListToString)

class object(univention.admin.handlers.simpleLdap):
	module=module

	def __init__(self, co, lo, position, dn='', superordinate=None,
			arg=None):
		global mapping
		global property_descriptions
		self.co = co
		self.lo = lo
		self.dn = dn
		self.position = position
		self._exists = 0
		self.mapping = mapping
		self.descriptions = property_descriptions
		univention.admin.handlers.simpleLdap.__init__(self, co, lo, 
			position, dn, superordinate)

	def exists(self):
		return self._exists

	def open(self):
		try:
			self.info["lastupdate_gui"] = time.strftime(
				"%d.%m.%Y %H:%M:%S", time.localtime(
				int(self.info.get("lastupdate",""))))
		except ValueError:
			self.info["lastupdate_gui"] = "never"

		univention.admin.handlers.simpleLdap.open(self)
		self.save()

		for areaCode in ["+", "00"]:
			if not areaCode in self.info.get("blockedAreaCodes", []):
				break
		else:
			self.info["blockInternational"] = "1"
			for areaCode in ["+", "00"]:
				self.info["blockedAreaCodes"].remove(areaCode)

	def saveCheckboxes(self):
		if "1" in self.info.get("blockInternational",[]):
			self.info.setdefault("blockedAreaCodes", []).extend(["+", "00"])
			if "" in self.info["blockedAreaCodes"]:
				self.info["blockedAreaCodes"].remove("")
			self.info["blockedAreaCodes"] = list(set(
				self.info["blockedAreaCodes"]))

        def _ldap_pre_modify(self):
		self.saveCheckboxes()
		if self.info.get('apply') == "1":
	                self.info['lastupdate'] = str(int(time.time()))
			self.info['configs'] = asterisk.genConfigs(
							self.co, self.lo, self)

	def _ldap_pre_create(self):
		self.dn = '%s=%s,%s' % (
			mapping.mapName('commonName'),
			mapping.mapValue('commonName', self.info['commonName']),
			self.position.getDn()
		)
		self.info["lastupdate"] = "0"
		self.saveCheckboxes()

	def _ldap_addlist(self):
		return [('objectClass', ['top', 'ast4ucsServer' ])]


def lookup(co, lo, filter_s, base='', superordinate=None, scope='sub', 
		unique=False, required=False, timeout=-1, sizelimit=0):
	filter = univention.admin.filter.conjunction('&', [
		univention.admin.filter.expression(
			'objectClass', "ast4ucsServer")
	])
 
	if filter_s:
		filter_p = univention.admin.filter.parse(filter_s)
		univention.admin.filter.walk(filter_p, 
			univention.admin.mapping.mapRewrite, arg=mapping)
		filter.expressions.append(filter_p)
 
	res = []
	for dn in lo.searchDn(unicode(filter), base, scope, unique, required, 
			timeout, sizelimit):
		res.append(object(co, lo, None, dn))
	return res

def identify(dn, attr, canonical=0):
	return 'ast4ucsServer' in attr.get('objectClass', [])
