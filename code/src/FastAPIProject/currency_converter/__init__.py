__version__ = "0.1.0"
from currency_converter import currency_convert
import os
import glob

modules = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith('__init__.py')]
