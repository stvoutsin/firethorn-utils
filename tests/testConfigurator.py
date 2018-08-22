'''
Created on Jul 17, 2018

@author: stelios
'''

import firethorn_utils.configurator as configurator
import firethorn

if __name__ == "__main__":
    
    ft = firethorn.Firethorn(endpoint="http://tap.metagrid.xyz/firethorn")
    ft.login(firethorn.config.adminuser, firethorn.config.adminpass, firethorn.config.admingroup)
    testConfigurator = configurator.Configurator(ft)
    testConfigurator.load_resources("https://raw.githubusercontent.com/stvoutsin/firethorn.py/master/firethorn/data/osa-tap.json")