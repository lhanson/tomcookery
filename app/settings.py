
# Now load sensitive settings from a local file, if present
try:
    from local_settings import *
except Exception:
    pass
