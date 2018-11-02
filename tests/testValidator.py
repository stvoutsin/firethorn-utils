'''
Created on Jul 17, 2018

@author: stelios
'''

import firethorn_utils.validator as validator
import firethorn
from argparse import ArgumentParser

if __name__ == "__main__":

    '''
    Validator Arguments
    '''
    parser = ArgumentParser()
    parser.add_argument("-ft", "--firethorn_url", dest="firethorn_url",
                    help="Firethorn Instance URL", metavar="Firethorn")
    parser.add_argument("-r", "--resource_id", dest="resource_id",
                    help="Resource ID", metavar="RESOURCE")
    parser.add_argument("-u", "--username", dest="username",
                    help="Firethorn username", metavar="USERNAME")
    parser.add_argument("-p", "--pass", dest="password",
                    help="Firethorn password", metavar="PASSWORD")
    parser.add_argument("-g", "--group", dest="group",
                    help="Firethorn group", metavar="GROUP")
    parser.add_argument("-v", "--verbose", dest="verbose", default=True,
                    help="Print status messages to stdout")
    args = parser.parse_args()

    ft = firethorn.Firethorn(endpoint=args.firethorn_url)
    ft.login(args.username, args.password, args.group)

    validator_obj = validator.Validator(ft, args.verbose)
    validator_obj.validate(args.firethorn_url + "/adql/resource/"  + args.resource_id)

