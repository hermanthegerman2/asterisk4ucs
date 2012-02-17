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

name = "asterisk"
description = "Creates configuration files for asterisk"
filter = "(objectClass=ast4ucsServer)"
attributes = ["ast4ucsServerLastupdate"]

__package__='' # workaround for PEP 366
import listener
import univention.debug
import zlib
import tempfile
import shutil
import subprocess

def unpackConfig(configs):
	res = {}
	for config in configs:
		filename, data = config.split(" ", 2)
		res[filename] = zlib.decompress(data.decode("base64"))
	return res

def handler(dn, newdata, olddata):
	if (not newdata or not "ast4ucsServerSshhost" in newdata
			or newdata["ast4ucsServerSshhost"] == ""):
		return

	userhost = "%s@%s" % (newdata["ast4ucsServerSshuser"][0],
			newdata["ast4ucsServerSshhost"][0])
	userhostpath = "%s:%s/ucs_autogen" % (userhost,
			newdata["ast4ucsServerSshpath"][0])
	configs = unpackConfig(newdata.get("ast4ucsServerConfig", []))
	command = "%s -rx 'core reload'" % (newdata["ast4ucsServerSshcmd"][0])

	if not configs:
		return

	listener.setuid(0)

	tempdir = tempfile.mkdtemp()

	for filename, content in configs.items():
		open(tempdir + "/" + filename, "w").write(content)

	files = [(tempdir + "/" + f) for f in configs.keys()]

	try:
		subprocess.check_call(
			["scp", "-Bq"] + files + [userhostpath])
	except subprocess.CalledProcessError, e:
		univention.debug.debug(
			univention.debug.LISTENER,
			univention.debug.ERROR,
			"scp failed with code %i." % (
				e.returncode))
		return

	try:
		subprocess.check_call(
			["ssh", "-oBatchMode=yes", userhost, command])
	except subprocess.CalledProcessError, e:
		univention.debug.debug(
			univention.debug.LISTENER,
			univention.debug.ERROR,
			"ssh failed with code %i." % (
				e.returncode))
		return

	shutil.rmtree(tempdir)

	listener.unsetuid()

def postrun():
	pass

