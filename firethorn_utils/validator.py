'''
Created on Jul 17, 2018

@author: stelios
'''

try:
    
    import urllib.request
    import firethorn
    import json    
    import logging
    import os
    from firethorn.models.resource import Resource
    from firethorn.models.adql.adql_resource import AdqlResource 
    import sys
    import uuid
    import time
    from argparse import ArgumentParser
    from util import Utility
except Exception as e:
    logging.exception(e)



class ValidatorResults(object):
    '''
    Validator Results Class, stores information from a validation run
    '''

    def __init__(self, processed, candidates, exceptions, total_time = 0):
        '''
        Constructor
        '''
        self.processed = processed
        self.candidates = candidates
        self.exceptions = exceptions
        self.total_time = 0

        return


    @property
    def processed(self):
        return self.__processed
        
        
    @processed.setter
    def processed(self, processed):
        self.__processed = processed


    @property
    def candidates(self):
        return self.__candidates


    @candidates.setter
    def candidates(self, candidates):
        self.__candidates = candidates


    @property
    def exceptions(self):
        return self.__exceptions


    @exceptions.setter
    def exceptions(self, exceptions):
        self.__exceptions = exceptions


    @property
    def total_time(self):
        return self.__total_time


    @total_time.setter
    def total_time(self, total_time):
        self.__total_time = total_time





class Validator(object):
    '''
    Validator class, used to validate an AdqlResource
    '''


    def __init__(self, firethorn_object , verbose):
        '''
        Constructor
        '''
        self.firethorn_object = firethorn_object
        self.verbose = verbose
        return
     

    def validate (self, resource_url):
        '''
        Validate an Adql Resource, Check all tables by querying and checking result row count
        '''

        start_time = time.time()
        print ("--- Starting validation on Resource: " + resource_url + "---")

        acc = self.firethorn_object.identity()

        resource = Resource(
            adql_resource = AdqlResource(
                account = acc,
                url = resource_url,
                )
            )
    
        #
        # Iterate the catalog/schema/tables tree querying each and
        # building a list of candidates where the result rowcount
        # is less than expected. 
    
        processed = dict()
        candidates = dict()
        exceptions =  dict()
    
        for schema in resource.get_schemas():
            for table in schema.get_tables():
                fullname = schema.name() + "." + table.name()
                if (self.verbose=='True'):
                    print(
                        "Testing [{}]".format(
                            fullname
                            )
                        )
                try:
                    query_str = "SELECT TOP 10 * FROM {}.{}".format(
                        schema.name(),
                        table.name()
                        )
                    query_obj = resource.query(
                        query_str
                        )


                    #py_table = query_obj.results().as_astropy()
                    #py_table.pprint()
                    rowcount = query_obj.results().rowcount()
                    processed[fullname] = rowcount
                    if (rowcount < 10):
                        candidates[fullname] = rowcount
                        if (self.verbose=='True'):
                            print(
                                "Candidate [{}] [{}]".format(
                                    fullname,
                                    rowcount
                                    )
                                )
                except:
                    message = sys.exc_info()[0]
                    exceptions[fullname] = message
                    if (self.verbose=='True'):
                        print(
                           "Exception [{}] [{}]".format(
                                fullname,
                                message
                                )
                            )

        total_time = time.time() - start_time 
        print("--- Validation completed after  %s seconds ---" % (total_time))
       
        return  ValidatorResults(candidates=candidates, processed=processed, exceptions=exceptions, total_time=total_time)



def main():

    '''
    Validator Arguments
    '''
    parser = ArgumentParser()
    parser.add_argument("-ft", "--firethorn_url", dest="firethorn_url",
                    help="Firethorn Instance URL", metavar="FIRETHORN")
    parser.add_argument("-r", "--resource_id", dest="resource_id",
                    help="Resource ID", metavar="RESOURCE")
    parser.add_argument("-u", "--username", dest="username",
                    help="Firethorn username", metavar="USERNAME")
    parser.add_argument("-p", "--pass", dest="password",
                    help="Firethorn password", metavar="PASSWORD")
    parser.add_argument("-g", "--group", dest="group",
                    help="Firethorn group", metavar="GROUP")
    parser.add_argument("-v", "--verbose", dest="verbose", 
                    help="Print status messages to stdout")
    parser.add_argument("-from", "--from", dest="from_email",
                    help="Email from which to send Validation email", metavar="FROM")
    parser.add_argument("-to", "--to", dest="to_email",
                    help="Email to which to send Validation email", metavar="TO")
    args = parser.parse_args()    


    ft = firethorn.Firethorn(endpoint=args.firethorn_url)
    ft.login(args.username, args.password, args.group)

    validator_obj = Validator(ft, args.verbose)
    validator_results = validator_obj.validate(args.firethorn_url + "/adql/resource/"  + args.resource_id)
    

    print ("Processed: ")
    print (validator_results.processed)
    print ("------------")
 
    print ("Candidates: ")
    print (validator_results.candidates)
    print ("------------")


    print ("Exceptions: ")
    print (validator_results.exceptions)
    print ("------------")

    '''
    Send exceptions by email
    '''
    if ((len(validator_results.exceptions)>0) and (args.from_email!=None) and (args.to_email!=None)):
        print ("Sending email with exceptions to: " + args.to_email)
        Utility.sendMail(args.from_email, args.to_email, "Validation Results - Database Exeptions", json.dumps(validator_results.exceptions))

if __name__ == "__main__":
    main()



