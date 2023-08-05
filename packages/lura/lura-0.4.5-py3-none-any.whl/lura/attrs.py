'''
Data structure helpers.

``attr`` and ``ottr`` are analogs to ``dict`` and ``OrderedDict`` which treat
attributes as keys to the backing dict.
```
>>> a = attr()
>>> a.foo = 'oof'
>>> a.foo
'oof'
>>> a['foo']
'oof'
>>> a['bar'] = 'rab'
>>> a['bar']
'rab'
>>> a.bar
'rab'
```
These classes behave like ``dict`` in every other way. Of course, only keys
which conform to Python's syntax requirements for attribute names are
accessible in this way. Traditional dict syntax must be used for keys
which cannot be used as a valid Python attribute name. Example:
```
>>> a = attr()
>>> a['foo bar'] = "python attribute names can't have spaces"
```
'''

from collections import OrderedDict
from collections import defaultdict

class AttributesMixin:
  'Mixin for dict types allowing attributes to be treated as keys.'

  def __init__(self, *args, **kwargs):
    super().__init__()

  def __getattr__(self, k):
    try:
      return self[k]
    except KeyError:
      pass
    err = f"'{type(self).__name__}' object has no attribute '{k}'"
    raise AttributeError(err)

  def __setattr__(self, k, v):
    self[k] = v

class DefaultMixin:
  'Mixin for dict types implementing defaultdict behavior.'

  def __init__(self, default_factory=None, *args, **kwargs):
    super().__init__()
    self.default_factory = default_factory

  def __missing__(self, key):
    if self.default_factory is None:
      raise KeyError(key)
    value = self.default_factory()
    self[key] = value
    return value

  def __getitem__(self, k):
    try:
      return super().__getitem__(k)
    except KeyError:
      pass
    return self.__missing__(k)

  def copy(self):
    return self.__class__(self.default_factory, self)

class Attributes(dict, AttributesMixin):
  'A subclass of ``dict`` that treats attributes as keys.'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  def copy(self):
    return self.__class__(self)

  def __repr__(self):
    return f'Attributes({super().__repr__()})'

class DefaultAttributes(defaultdict, AttributesMixin):
  'A subclass of ``defaultdict`` that treats attributes as keys.'

  def __init__(self, default_factory, *args, **kwargs):
    super().__init__(default_factory, *args, **kwargs)

  def copy(self):
    return self.__class__(self.default_factory, self)

class RecursiveAttributes(DefaultAttributes):
  '''
  A subclass of ``DefaultAttributes`` that uses its own constructor as its
  factory.
  '''

  def __init__(self, *args, **kwargs):
    super().__init__(self.__class__, *args, **kwargs)

  def copy(self):
    return self.__class__(self)

class OrderedAttributes(OrderedDict, AttributesMixin):
  'A subclass of ``OrderedDict`` that treats attributes as keys.'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

class DefaultOrderedAttributes(OrderedAttributes, DefaultMixin):
  '''
  A subclass of ``OrderedAttributes`` that implements the behavior of
  ``defaultdict``.
  '''

  def __init__(self, default_factory=None, *args, **kwargs):
    DefaultMixin.__init__(self, default_factory)
    del self['default_factory']
    OrderedDict.__setattr__(self, 'default_factory', default_factory)
    OrderedAttributes.__init__(self, *args, **kwargs)

class RecursiveOrderedAttributes(DefaultOrderedAttributes):
  '''
  A subclass of ``DefaultOrderedAttributes`` that uses its own constructor as
  its factory.
  '''

  def __init__(self, *args, **kwargs):
    super().__init__(self.__class__, *args, **kwargs)

class AttributesWrapper:

  # FIXME generalize and test; recursive AttributesWrapper

  def __init__(self, target):
    super().__init__()
    self.__dict__['__target__'] = target

  def __getitem__(self, *args, **kwargs):
    return self.__target__.__getitem__(*args, **kwargs)

  def __setitem__(self, *args, **kwargs):
    self.__target__.__setitem__(*args, **kwargs)

  def __delitem__(self, *args, **kwargs):
    self.__target__.__delitem__(*args, **kwargs)

  def __iter__(self):
    return self.__target__.__iter__()

  def __len__(self):
    return self.__target__.__len__()

  def __getattr__(self, name):
    if hasattr(self.__target__, name):
      return getattr(self.__target__, name)
    try:
      return self.__target__[name]
    except KeyError:
      pass
    err = f"'{type(self).__name__}' object has no attribute '{name}'"
    raise AttributeError(err)

  def __setattr__(self, name, value):
    if name in self.__dict__:
      self.__dict__[name] = value
      return
    target = self.__target__
    if hasattr(target, name):
      setattr(target, name, value)
    else:
      target[name] = value

attr = Attributes
dattr = DefaultAttributes
rattr = RecursiveAttributes
defaultattr = DefaultAttributes

ottr = OrderedAttributes
dottr = DefaultOrderedAttributes
rottr = RecursiveOrderedAttributes
defaultottr = DefaultOrderedAttributes

wttr = AttributesWrapper
