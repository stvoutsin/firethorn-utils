'''
Created on Jul 17, 2018

@author: stelios
'''

import firethorn_utils.validator as validator
import firethorn

if __name__ == "__main__":
    
    ft = firethorn.Firethorn(endpoint="http://tap.metagrid.xyz/firethorn")
    print (ft.identity())
    ft.login(firethorn.config.adminuser, firethorn.config.adminpass, firethorn.config.admingroup)
    print (ft.identity())
    testValidator = validator.Validator(ft)
    testValidator.validate("http://tap.metagrid.xyz/firethorn/adql/resource/54")