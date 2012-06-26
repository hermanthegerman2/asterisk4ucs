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
import univention.admin.syntax
import univention.admin.handlers
import univention.admin.handlers.asterisk
import univention.admin.handlers.asterisk.contact
import univention.admin.handlers.asterisk.phoneGroup
import univention.admin.handlers.asterisk.waitingLoop
import univention.admin.handlers.asterisk.sipPhone
import univention.admin.handlers.asterisk.conferenceRoom
import univention.admin.handlers.asterisk.phoneType
import univention.admin.handlers.asterisk.mailbox
import univention.admin.handlers.asterisk.faxGroup
import univention.admin.handlers.asterisk.server
import univention.admin.handlers.asterisk.fax
import univention.admin.handlers.asterisk.phoneBook
import univention.admin.handlers.asterisk.music
import univention.admin.handlers.asterisk.agiscript
import operator

module = "asterisk/asterisk"
short_description = u"Asterisk"
long_description = ''
operations = ['search']
default_containers = [ "cn=asterisk" ]

childs = 0
virtual = 1

modulesWithSuperordinates = {
	"None": [
		univention.admin.handlers.asterisk.server,
		univention.admin.handlers.asterisk.phoneBook,
	],
	"asterisk/server": [
		univention.admin.handlers.asterisk.phoneGroup,
		univention.admin.handlers.asterisk.waitingLoop,
		univention.admin.handlers.asterisk.sipPhone,
		univention.admin.handlers.asterisk.conferenceRoom,
		univention.admin.handlers.asterisk.phoneType,
		univention.admin.handlers.asterisk.mailbox,
		univention.admin.handlers.asterisk.faxGroup,
		univention.admin.handlers.asterisk.fax,
		univention.admin.handlers.asterisk.music,
		univention.admin.handlers.asterisk.agiscript,
	],
	"asterisk/phoneBook": [
		univention.admin.handlers.asterisk.contact,
	]
}

usewizard = 1
wizardmenustring="Asterisk"
wizarddescription="Asterisk verwalten"
childmodules = [x.module for x in
	reduce(operator.add, modulesWithSuperordinates.values())]

def superordinatecmp(x, y):
	if x == "None":
		return -1
	elif y == "None":
		return 1
	return cmp(x, y)

wizardsuperordinates = sorted(modulesWithSuperordinates.keys(), cmp=superordinatecmp)
wizardtypesforsuper = {}
for key, value in modulesWithSuperordinates.items():
	wizardtypesforsuper[key] = [x.module for x in value]

wizardoperations={"add":["Add", "Add DNS object"],"find":["Search", "Search DNS object(s)"]}
options = {}
layout = []
property_descriptions = {}
mapping = univention.admin.mapping.mapping()

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

def lookup(co, lo, filter_s, base='', superordinate=None, scope='sub',
		unique=0, required=0, timeout=-1, sizelimit=0):
	ret = []
	supi = "None"
	if superordinate:
		supi = superordinate.module
	for module in modulesWithSuperordinates[supi]:
		if module == univention.admin.handlers.asterisk.music:
			continue
		ret += module.lookup(co, lo, filter_s, base, superordinate,
			scope, unique, required, timeout, sizelimit)
	return ret

def identify(dn, attr, canonical=0):
	pass

