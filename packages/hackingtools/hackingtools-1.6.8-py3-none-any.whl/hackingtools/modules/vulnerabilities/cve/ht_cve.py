from hackingtools.core import Logger, Utils, Config
import hackingtools as ht
import os

config = Config.getConfig(parentKey='modules', key='ht_cve')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():

	def __init__(self):
		pass

	def help(self):
		Logger.printMessage(message=ht.getFunctionsNamesFromModule('ht_cve'), debug_module=True)

	def search(self, cve_id='', product_name='', version='', year=''):
		pass