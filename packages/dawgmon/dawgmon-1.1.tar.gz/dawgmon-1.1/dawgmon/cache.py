import json 
from datetime import datetime

from dawgmon.utils import ts_to_str, str_to_ts

class CacheException(Exception):
	pass

class Cache:
	def __init__(self, fn):
		self.fn = fn
		self.data = {}

	def load(self, create=True):
		try:
			with open(self.fn, "r") as fd:
				self.data = json.load(fd)
		except FileNotFoundError:
			# try and create and empty cache
			self.data = {}
			self.save()
		return

	def save(self):
		with open(self.fn, "w+") as fd:
			json.dump(self.data, fd)

	def purge(self, no):
		if not no or type(no) != int or no < 0:
			return False
		for hostname in self.data:
			self.data[hostname] = self.data[hostname][-no:]
		return True

	def get_hostnames(self):
		hostnames = list(self.data.keys())
		hostnames.sort()
		return hostnames

	def get_entries(self, hostname=None):
		if hostname and hostname not in self.get_hostnames():
			return []
		res = []
		for entry_hostname in self.data:
			if hostname and hostname != entry_hostname:
				continue
			entries = self.data[entry_hostname]
			count = 0
			for entry in entries:
				res.append({"hostname":entry_hostname, "timestamp":entry["timestamp"], "id":count})
				count = count + 1
		return res

	def get_entry(self, entry_id, hostname="localhost"):
		entries = self.get_entries(hostname)
		if len(entries) == 0:
			return None
		if entry_id == -1:
			# default to the last entry
			entry_id = entries[-1]["id"]
		elif entry_id >= len(self.data[hostname]):
			return None
		return self.data[hostname][entry_id]["data"]

	def get_entry_timestamp(self, entry_id, hostname="localhost"):
		entries = self.get_entries(hostname)
		if len(entries) == 0:
			return None
		if entry_id == -1:
			# default to the last entry
			entry_id = entries[-1]["id"]
		elif entry_id >= len(self.data[hostname]):
			return None

		# fall back automatically on timestamps that do not record
		# subsecond intervals such as the timestamps that are in old
		# caches
		ts = self.data[hostname][entry_id]["timestamp"]
		try:
			return str_to_ts(ts)
		except ValueError:
			return str_to_ts(ts, False)

	def get_last_entry(self, hostname="localhost"):
		return self.get_entry(-1, hostname)

	def get_last_entry_timestamp(self, hostname="localhost"):
		return self.get_entry_timestamp(-1, hostname)

	def add_entry(self, data, hostname="localhost", timestamp=None):
		self.data.setdefault(hostname, [])
		if not timestamp:
			timestamp = datetime.utcnow()
		tsnow = ts_to_str(timestamp)
		self.data[hostname].append({"timestamp":tsnow, "data":data})
