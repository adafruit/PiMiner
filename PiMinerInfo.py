#!/usr/bin/python

#Portions of this file use code from fcicq's cgmonitor.py:
#https://gist.github.com/fcicq/4975730

import subprocess
import socket
import time

class PiMinerInfo:
	
	host = ''
	port = 4028
	screen1 = ['no data','no data']
	screen2 = ['no data','no data']
	screen3 = ['no data','no data']
	screen4 = ['no data','no data']

	def __init__(self):
	  self.host = self.get_ipaddress()
	  self.refresh()
	
	def value_split(self, s):
	  r = s.split('=')
	  if len(r) == 2: return r
	  return r[0], ''
	
	def response_split(self, s):
	  try:
		r = s.split(',')
		title = r[0]
		d = dict(map(self.value_split, r[1:]))
		return title, d
	  except ValueError:
		print s
	
	def get_ipaddress(self):
		arg = 'ip route list'
		p = subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
		data = p.communicate()
		split_data = data[0].split()
		self.ipaddr = split_data[split_data.index('src')+1]
		return self.ipaddr
	
	def cg_rpc(self, host, port, command):
	  try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((host, port))
		s.sendall(command)
		time.sleep(0.02)
		data = s.recv(8192)
		s.close()
	  except Exception as e:
		print str(e)
		data = ''
	  if data:
		d = data.strip('\x00|').split('|')
		return map(self.response_split, d)
	  return None
	
	def hashrate(self, h):
	  u = 'Mh/s'
	  if h >= 1000.0:
		u = 'Gh/s'
		h = h / 1000.0
	  elif h >= 1000000.0:
		u = 'Th/s'
		h = h / 1000000.0
	  s = '%s %s' % (h, u)
	  return s
	  
	def parse_summary(self, r):
	  if not (isinstance(r, (list, tuple)) and len(r) == 2):
		return
	  try:
		if not r[0][0] == 'STATUS=S' and r[1][0] == 'SUMMARY':
		  return
		d = r[1][1]
		s1 = 'A:%s R:%s H:%s' % (d['Accepted'], d['Rejected'], d['Hardware Errors'])
		s2 = 'avg:%s' % self.hashrate(float(d['MHS av']))
		return [s1, s2]
	  except Exception as e:
		return [str(e), str(e)]

	def conv_prio_dict(self, p):
		if isinstance(p, (tuple, list, )):
			try:
				pd = dict(p)
			except TypeError: # not able to convert
	  			pd = zip(p, range(len(p)))
			return pd
  		if isinstance(p, dict): return p
  		return {}
	
	def parse_pools(self, r):
		if not isinstance(r, (list, tuple)): return ['format', 'error']
		
  		try:
			if not r[0][0] == 'STATUS=S': return ['status', 'error']
			remote_time = int(r[0][1]['When'])
			for rp in r[1:]:
				if rp[0][0:4] != 'POOL': continue
	  			d = rp[1]
	  			if d['URL'].startswith('stratum+tcp://'): d['URL'] = d['URL'][14:]
	  			if d['URL'].startswith('http://'): d['URL'] = d['URL'][7:]
	  			d['URL'] = d['URL'].rstrip('/')
 			if d['Status'] == 'Alive':
				s1 = '%s' % d['URL']
				s2 = '%s' % d['User']
				return [s1, s2]
  		except Exception as e:
			return [str(e), str(e)]

	def parse_config(self, r):
		if not isinstance(r, (list, tuple)): return
		try:
			if not r[0][0] == 'STATUS=S': return
			if not r[1][0] == 'CONFIG': return
			d = r[1][1]
			return 'Devices: %s' % (int(d.get('GPU Count','0')) + int(d.get('PGA Count','0')) + int(d.get('ASC Count','0')))
		except Exception as e:
			return str(e)

	def parse_coin(self, r):
		if not isinstance(r, (list, tuple)): return
		try:
			d = r[1][1]
			return 'Diff:%.0f' % float(d['Network Difficulty'])
		except Exception as e:
			return str(e)
	
	def refresh(self):
		#Screen 1 data
		s = self.cg_rpc(self.host, self.port, 'summary')
		self.screen1 = self.parse_summary(s)
		#Screen 3 data
		s = self.cg_rpc(self.host, self.port, 'pools')
		self.screen3 = self.parse_pools(s)
		#Screen 2 data
		s = self.cg_rpc(self.host, self.port, 'config')
		self.screen2[0] = self.parse_config(s)
		s = self.cg_rpc(self.host, self.port, 'coin')
		self.screen2[1] = self.parse_coin(s)	
