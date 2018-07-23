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
except Exception as e:
    logging.exception(e)


class Validator(object):
    '''
    classdocs
    '''


    def __init__(self, firethorn_object ):
        '''
        Constructor
        '''
        self.firethorn_object = firethorn_object
        return
     
    def validate (self, resource_url):
        '''
        Validate an Adql Resource, Check all tables by querying and checking result row count
        '''

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
                    py_table = query_obj.results().as_astropy()
                    py_table.pprint()
                    rowcount = query_obj.results().rowcount()
                    processed[fullname] = rowcount
                    if (rowcount < 10):
                        candidates[fullname] = rowcount
                        print(
                            "Candidate [{}] [{}]".format(
                                fullname,
                                rowcount
                                )
                            )
                except:
                    message = sys.exc_info()[0]
                    exceptions[fullname] = message
                    print(
                    "Exception [{}] [{}]".format(
                        fullname,
                        message
                        )
                    )