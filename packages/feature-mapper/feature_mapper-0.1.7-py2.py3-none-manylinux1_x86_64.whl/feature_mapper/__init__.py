# __import__('pkg_resources').declare_namespace(__name__)

from .feature_mapper import lib
from .wrapper import map_feature, map_feature_smin

# initialize Rust (logging)
lib.init()

__all__ = [
    'map_feature',
    'map_feature_smin',
]
