import os
from subprocess import call, Popen, PIPE

class Locksmith(object):
	def __init__(self, user):
		self.user = user
		if user == 'github':
			self.user == get_github_user()
		self.legend = "{}.lcksmth".format(user)

	def get_github_user():
		return

	def get_secret(self, parameter):
		return

	def encrypt_secret(self, parameter):
		return

