import os
from subprocess import Popen, PIPE

class Locksmith():
	def __init__(self, user):
		"""
		Initializes the Locksmith
		  user - the name of the user for which secrets will be decoded
		  legend - the name of the legend file, in format {user}.lcksmth.gpg
		"""
		self.user = user
		self.legend = "{}.lcksmth.gpg".format(user)
		if not os.path.isfile(self.legend):
			raise EnvironmentError("Could not find legend file {}".format(self.legend))

		self.__secrets = self.__get_secrets()

	def __get_secrets(self):
		"""
		Intentionally private method to obtain user's secrets
		"""
		cmd = 'echo RELOADAGENT | gpg-connect-agent'
		proc = Popen(cmd, stdout=PIPE, shell=True)
		out, err = proc.communicate()

		cmd = 'gpg -d {}'.format(self.legend)
		proc = Popen(cmd, stdout=PIPE, shell=True)
		out, err = proc.communicate()

		secrets = {}
		for index, line in enumerate(out.splitlines()):
			key, value = line.decode('utf-8').split("=", 1)
			secrets[key] = value

		return secrets

	def get_secret(self, parameter):
		"""
		Get a specific secret from the user's secrets
		"""
		if parameter == "":
			raise ValueError("Empty secret")
		if not parameter in self.__secrets.keys():
			raise LookupError("Could not find a value for {} in {}'s secrets".format(parameter, self.user))
		return self.__secrets[parameter]

	def add_secret(self, secret, value):
		"""
		Add a specific secret to the user's secrets
		"""
		if secret == "":
			raise ValueError("Empty secret")
		if value == "":
			raise ValueError("Empty value") 
		if secret in self.__secrets.keys():
			raise LookupError("There's already a value for {} in {}'s secrets".format(secret, self.user))
		self.__secrets[secret] = value

	def update_secret(self, secret, value):
		"""
		Update the value of a user's secrets
		"""
		if secret == "":
			raise ValueError("Empty secret")
		if value == "":
			raise ValueError("Empty value")
		if not secret in self.__secrets.keys():
			raise LookupError("Could not find a value for {} in {}'s secrets".format(secret, self.user))
		self.__secrets[secret] = value

	def save(self):
		"""
		Save changes to secrets
		"""
		secret_text = "\n".join(["{}={}".format(key, value) for key, value in self.__secrets.items()])
		cmd = "yes | echo {} | gpg -c -o {}.lcksmth.gpg".format(secret_text, self.user)
		proc = Popen(cmd)

	def encrypt_secrets(self):
		"""
		Encrypt a secrets file
		# TODO: do we really need this?
		"""
		return

