import logging
import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(__file__))

try:
    import configurator
except Exception as e:
    print ("Error during py imports..(py.py): " + str(e))
    logging.exception(e)
