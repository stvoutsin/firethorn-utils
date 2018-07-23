try:
    import logging
    from . import configurator
    from . import validator

except Exception as e:
    print ("Error during py imports..(py.py): " + str(e))
    logging.exception(e)
