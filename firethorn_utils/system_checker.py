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
    import sys
    import uuid
    import time
    from argparse import ArgumentParser
    from .util import Utility
except Exception as e:
    logging.exception(e)



class FirethornCheckerResults(object):
    '''
    Firethorn Health Checker Results Class, stores information from a health check run
    '''

    def __init__(self, exceptions={}, message=""):
        '''
        Constructor
        '''
        self.exceptions = exceptions
        self.message = message

        return



class FirethornHealthChecker(object):
    '''
    FirethornHealthChecker class, used to health check a Firethorn System
    '''


    def __init__(self, firethorn_url, verbose = True):
        '''
        Constructor
        '''
        self.verbose = verbose
        self.firethorn_url = firethorn_url
        return
     

    def check_disk_space (self, max_percent=None, min_available_bytes=None):

        exceptions = {}
        message = ""

        try:
            if (self.verbose):
                print ("Checking Firethorn System: " + self.firethorn_url)
           
            usable_bytes = int(self.get_system_info()["java"]["disk"]["usable"])
            total_bytes = int(self.get_system_info()["java"]["disk"]["total"])
            usage_percent = usable_bytes/total_bytes*100
            usable_bytes_in_gb = usable_bytes/1024/1024/1024

            if (min_available_bytes!=None):
                if (usable_bytes<float(min_available_bytes)):
                    if (self.verbose):
                        print ("Disk space usage is too high! Available Disk Space: " + ("%.2f" % usable_bytes_in_gb) + " GB  (" + ("%.2f" % usage_percent) + "% Full)")
                    message = "Disk space usage is too high! Available Disk Space: " + ("%.2f" % usable_bytes_in_gb) + " GB  (" + ("%.2f" % usage_percent) + "% Full)"
                    exceptions["disk"] = message

            elif (max_percent!=None):
                if (usage_percent>float(max_percent)):
                    if (self.verbose):
                        print("Disk space usage is too high! Available Disk Space: " + ("%.2f" % usable_bytes_in_gb) + " GB  (" + ("%.2f" % usage_percent) + "% Full)")
                    message = "Disk space usage is too high! Available Disk Space: " + ("%.2f" % usable_bytes_in_gb) + " GB  (" + ("%.2f" % usage_percent) + "% Full)"
                    exceptions["disk"] = message
            

        except Exception as e:
            exceptions["vm"] = str(e)
            message = str(e)
            logging.exception(e)

        return FirethornCheckerResults(exceptions = exceptions, message = message)

        
    def get_system_info(self):
        """Wrapper function to send a GET request to get the status of a resource and return the JSON
        
                   
        Returns    
        -------
        query_json:
            The JSON response as a string
        
        """
 
        request = urllib.request.Request(self.firethorn_url + "/system/info")
        query_json = {}

        with urllib.request.urlopen(request) as response:
            query_json = json.loads(response.read().decode('utf-8'))

        return query_json            
            

def main():

    '''
    Validator Arguments
    '''
    parser = ArgumentParser()
    parser.add_argument("-ft", "--firethorn_url", dest="firethorn_url",
                    help="Firethorn Instance URL", metavar="FIRETHORN")
    parser.add_argument("-per", "--max-percent", dest="max_percent",
                    help="Firethorn Instance URL", metavar="MAX PERCENT")
    parser.add_argument("-from", "--from", dest="from_email",
                    help="Email from which to send Validation email", metavar="FROM")
    parser.add_argument("-to", "--to", dest="to_email",
                    help="Email to which to send Validation email", metavar="TO")
    parser.add_argument("-v", "--verbose", dest="verbose",
                    help="Print status messages to stdout")

    args = parser.parse_args()    


    fHC_obj = FirethornHealthChecker(args.firethorn_url)

    if (args.max_percent!=None):
        health_check_results = fHC_obj.check_disk_space(max_percent=args.max_percent)
    else : 
        health_check_results = fHC_obj.check_disk_space(max_percent=50)

      
    print (health_check_results.exceptions)
    print (health_check_results.message)

    '''
    Send exceptions by email
    '''
    if ((len(health_check_results.exceptions)>0) and (args.from_email!=None) and (args.to_email!=None)):
        print ("Sending email with exceptions to: " + args.to_email)
        Utility.sendMail(args.from_email, args.to_email, "Health Check Results for: " + args.firethorn_url, str(health_check_results.message))

if __name__ == "__main__":
    main()


