from . import *

class IsRestartRequiredCommand(Command):
	name = "needs_restart"
	shell = True 
	command = "/bin/sh -c 'if test -f /var/run/reboot-required.pkgs ; then cat /var/run/reboot-required.pkgs; fi'"
	desc = "checks whether a reboot is required (Ubuntu-only)"

	def parse(output):
		return output

	def compare(prev, cur):
		if len(cur) > 0:
			pkgs = cur.splitlines()
			pkgs.sort()
			return [W("reboot required"), D("reboot required because of packages [%s]" % (",".join(pkgs)))]
		return []
