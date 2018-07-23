try:
    import logging
    from .firethorn_utils import configurator
    from .firethorn_utils import validator

except Exception as e:
    print ("Error during py imports..(py.py): " + str(e))
    logging.exception(e)
