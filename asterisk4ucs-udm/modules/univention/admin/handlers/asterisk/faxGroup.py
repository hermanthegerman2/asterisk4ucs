# coding=utf-8

"""
Copyright (C) 2012 DECOIT GmbH <asterisk4ucs@decoit.de>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3 as
published by the Free Software Foundation

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

import univention.admin.filter
import univention.admin.handlers
import univention.admin.syntax
from univention.admin.layout import Tab

module = "asterisk/faxGroup"
short_description = u"Asterisk4UCS-Management: Faxgruppe"
operations = ['add', 'edit', 'remove', 'search', 'move']
options = {}

childs = 0
usewizard = 1
superordinate = "asterisk/server"

layout = [
	Tab('Allgemein', 'Allgemeine Einstellungen', layout = [
		[ "extension" ],
		[ "members" ],
	])
]

property_descriptions = {
	"extension": univention.admin.property(
		short_description="Durchwahl",
		syntax=univention.admin.syntax.string,
		identifies=True,
		required=True,
	),
	"members": univention.admin.property(
		short_description="Teilnehmer",
		syntax=univention.admin.syntax.LDAP_Search(
			filter="objectClass=inetOrgPerson",
			attribute=['users/user: username'],
			value='users/user: dn',
		),
		multivalue=True,
	),
}

mapping = univention.admin.mapping.mapping()
mapping.register("extension", "ast4ucsExtensionExtension",
	None, univention.admin.mapping.ListToString)
mapping.register("members", "ast4ucsFaxgroupMember")

class object(univention.admin.handlers.simpleLdap):
	module=module

	def __init__(self, co, lo, position, dn='', superordinate=None,
			attributes=[]):
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

		self.openSuperordinate()
		if not self.superordinate:
			raise univention.admin.uexceptions.insufficientInformation, \
					 'superordinate object not present'
		if not dn and not position:
			raise univention.admin.uexceptions.insufficientInformation, \
					 'neither DN nor position present'

	def openSuperordinate(self):
		if self.superordinate:
			return

		self.open()
		serverdn = self.oldattr.get("ast4ucsSrvchildServer")
		if not serverdn:
			return

		if serverdn.__iter__:
			serverdn = serverdn[0]

		univention.admin.modules.update()
		servermod = univention.admin.modules.get("asterisk/server")
		univention.admin.modules.init(self.lo, self.position, servermod)
		self.superordinate = servermod.object(self.co, self.lo,
				self.position, serverdn)
		self.superordinate.open()

	def exists(self):
		return self._exists

	def open(self):
		univention.admin.handlers.simpleLdap.open(self)
		self.save()

	def _ldap_pre_create(self):
		self.dn = '%s=%s,%s' % (
			mapping.mapName('extension'),
			mapping.mapValue('extension', self.info['extension']),
			self.position.getDn()
		)
	
	def _ldap_addlist(self):
		return [('objectClass', ['ast4ucsFaxgroup']),
				('ast4ucsSrvchildServer', self.superordinate.dn)]


def lookup(co, lo, filter_s, base='', superordinate=None, scope='sub', 
		unique=False, required=False, timeout=-1, sizelimit=0):
	filter = univention.admin.filter.conjunction('&', [
		univention.admin.filter.expression(
			'objectClass', "ast4ucsFaxgroup")
	])

	if superordinate:
		filter.expressions.append(univention.admin.filter.expression(
				'ast4ucsSrvchildServer', superordinate.dn))
 
	if filter_s:
		filter_p = univention.admin.filter.parse(filter_s)
		univention.admin.filter.walk(filter_p, 
			univention.admin.mapping.mapRewrite, arg=mapping)
		filter.expressions.append(filter_p)

	res = []
	for dn, attrs in lo.search(unicode(filter), base, scope, [], unique,
			required, timeout, sizelimit):
		res.append(object(co, lo, None, dn=dn,
				superordinate=superordinate, attributes=attrs))
	return res

def identify(dn, attr, canonical=0):
	return 'ast4ucsFaxgroup' in attr.get('objectClass', [])

