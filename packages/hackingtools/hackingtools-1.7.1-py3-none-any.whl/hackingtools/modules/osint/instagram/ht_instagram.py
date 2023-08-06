from hackingtools.core import Logger, Config
import hackingtools as ht
import os

config = Config.getConfig(parentKey='modules', key='ht_instagram')
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'output'))

class StartModule():
    
    def __init__(self):
        pass
        
    def help(self):
        return ht.getFunctionsNamesFromModule('ht_instagram')

    def mensaje(self, texto1, texto2='', eres_feo=False):
        return 'Parece que {feo} jaaj {t1} - {t2}'.format(feo='eres muyyyy feo' if eres_feo else 'eres guapete', t1=texto2, t2=texto1)