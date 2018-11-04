try:
    import logging
    from . import configurator
    from . import validator
    from .util import *
except Exception as e:
    print ("Error during py imports..(py.py): " + str(e))
    logging.exception(e)
