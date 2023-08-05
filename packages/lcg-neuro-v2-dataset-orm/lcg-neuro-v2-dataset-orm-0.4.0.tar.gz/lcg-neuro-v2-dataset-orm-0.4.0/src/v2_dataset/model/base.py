"""Basic tools for defining entity classes.
"""
import numpy as np

from cached_property import cached_property
from v2_dataset.orm import declarative_base

#: `SQLAlchemy declarative base`_ (created by :func:`v2.orm.declarative_base`) from which all entity-types in the
#: :mod:`v2.db.model` package are derived.
Model = declarative_base()


def auto_cached_properties(cls):
    """Modifies a class containing cached property-decorated methods (:func:`cached_property.cached_property`) so that
    any attribute change invalidates all cached properties. This should be applied on top of any decorators that might
    change the ``__setattr__`` special method.
    """
    old_setattr = cls.__setattr__

    def __setattr__(self, key, val):
        try:
            old_val = getattr(self, key)
            if np.any(old_val != val):
                for attr in self.__dict__:
                    if type(self.__dict__[attr]) == cached_property:
                        del self.__dict__[attr]
        except AttributeError:
            pass
        old_setattr(self, key, val)

    cls.__setattr__ = __setattr__
    return cls
