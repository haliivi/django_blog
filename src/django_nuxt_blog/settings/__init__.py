try:
    from .local_settings import *
except ImportError:
    from .develop_settings import *
