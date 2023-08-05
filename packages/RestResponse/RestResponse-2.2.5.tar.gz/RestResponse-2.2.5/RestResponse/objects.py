import json
import simplejson
import six
import warnings
from datetime import datetime, date
from dateutil import parser as dateutil_parser
from sqlalchemy.ext.mutable import Mutable
from RestResponse import utils


class RestEncoder(utils.CustomObjectEncoder):
    __opts__ = {
        'encode_binary': True,
        'encode_callable': True,
        'decode_binary': True,
        'decode_callable': True
    }

    def isinstance(self, obj, cls):
        if isinstance(obj, (RestResponseObj, NoneProp)):
            if isinstance(obj, RestResponseObj):
                self.__opts__.update(obj.__opts__)
            return False
        return isinstance(obj, cls)

    def _walk_dict(self, obj):
        result = {}
        for k, v in six.iteritems(obj):
            if isinstance(v, NoneProp):
                result[k] = None
            elif isinstance(v, dict):
                result[k] = self._walk_dict(v)
            elif isinstance(v, list):
                result[k] = self._recurse_list(v)
            else:
                result[k] = utils.encode_item(v, **self.__opts__)
        return result

    def _recurse_list(self, obj):
        result = []
        for item in obj:
            if isinstance(item, NoneProp) or item is None:
                result.append(None)
            elif isinstance(item, list):
                result.append(self._recurse_list(item))
            elif isinstance(item, dict):
                result.append(self._walk_dict(item))
            else:
                result.append(utils.encode_item(item, **self.__opts__))
        return result

    def default(self, obj):
        if isinstance(obj, ApiModel):
            return self.default(obj._data)
        if isinstance(obj, list):
            return self._recurse_list(obj)
        elif isinstance(obj, dict):
            return self._walk_dict(obj)
        elif isinstance(obj, NoneProp) or obj is None:
            return None
        else:
            return utils.encode_item(obj, **self.__opts__)


json._default_encoder = RestEncoder()
simplejson._default_encoder = RestEncoder()


class RestResponseObj(Mutable, object):
    __parent__ = None
    __opts__ = {
        'encode_binary': True,
        'encode_callable': True,
        'decode_binary': True,
        'decode_callable': True
    }

    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, dict) and not isinstance(value, RestObject):
            return RestObject(value)
        elif isinstance(value, list) and not isinstance(value, RestList):
            return RestList(value)
        else:
            return value

    def changed(self):
        if self.__parent__:
            self.__parent__.changed()
        else:
            super(RestResponseObj, self).changed()

    def __call__(self):
        return json.loads(json.dumps(self, cls=RestEncoder))


class NoneProp(object):
    def __init__(self, parent, prop):
        self.__parent__ = parent
        self.__prop__ = prop

    def __eq__(self, other):
        return other is None

    def __lt__(self, other):
        return other is not None

    def __gt__(self, other):
        return False

    def __str__(self):
        return 'None'

    def __repr__(self):
        return 'None'

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False

    def __len__(self):
        return 0

    def __call__(self):
        return None

    def __iter__(self):
        for i in []:
            yield i

    def __contains__(self, key):
        return False

    def __unicode__(self):
        return u'None'

    def __setattr__(self, name, value):
        if name == '__parent__' or name == '__prop__':
            super(NoneProp, self).__setattr__(name, value)
        else:
            parent = self.__parent__
            props = [self.__prop__]
            while type(parent) != RestObject:
                props.append(parent.__prop__)
                parent = parent.__parent__

            result = {
                name: value
            }

            for p in props:
                result = {
                    p: result
                }

            parent._update_object(result)

    def __delattr__(self, name):
        pass

    def __getattr__(self, name):
        return NoneProp(self, name)

    def __getitem__(self, name):
        return self.__getattr__(name)

    def __setitem__(self, name, value):
        self.__setattr__(name, value)


class RestList(RestResponseObj, list):
    def __init__(self, data, parent=None, **kwargs):
        if not isinstance(data, list):
            raise ValueError('RestList data must be list object')

        self.__parent__ = parent
        self.__opts__.update(kwargs)

        for item in data:
            self.append(item)

    @property
    def __data__(self):
        return json.loads(self.pretty_print())

    def pretty_print(self, indent=4):
        return json.dumps(self, cls=RestEncoder, indent=indent)

    def __repr__(self):
        return super(RestList, self).__repr__()

    def __getitem__(self, index):
        item = super(RestList, self).__getitem__(index)
        return utils.decode_item(item, **self.__opts__)

    def __setitem__(self, index, value):
        if index >= 0 and index < len(self):
            self.pop(index)
            self.insert(index, value)
        else:
            raise IndexError('list index out of range')

    def __contains__(self, item):
        if not (isinstance(item, RestResponseObj) or isinstance(item, NoneProp)):
            item = utils.encode_item(item, **self.__opts__)
        return super(RestList, self).__contains__(item)

    def __iter__(self):
        for item in list.__iter__(self):
            yield utils.decode_item(item, **self.__opts__)

    def append(self, item):
        if not (isinstance(item, RestResponseObj) or isinstance(item, NoneProp)):
            item = utils.encode_item(item, **self.__opts__)
        super(RestList, self).append(RestResponse.parse(item, parent=self))
        self.changed()

    def extend(self, items):
        for item in items:
            self.append(item)

    def insert(self, index, item):
        if not (isinstance(item, RestResponseObj) or isinstance(item, NoneProp)):
            item = utils.encode_item(item, **self.__opts__)
        super(RestList, self).insert(index, RestResponse.parse(item, parent=self))
        self.changed()

    def pop(self, index=None):
        if index:
            value = super(RestList, self).pop(index)
        else:
            value = super(RestList, self).pop()
        self.changed()
        return utils.decode_item(value, **self.__opts__)

    def remove(self, item):
        super(RestList, self).remove(item)
        self.changed()


class RestObject(RestResponseObj, dict):
    def __init__(self, data, parent=None, **kwargs):
        if not isinstance(data, dict):
            raise ValueError('RestObject data must be dict object')
        self.__data__ = {}
        self.__parent__ = parent
        self.__opts__.update(kwargs)

        for k, v in six.iteritems(data):
            self.__data__[k] = self._init_data(v)

    def __repr__(self):
        return json.dumps(self, cls=RestEncoder, indent=None)

    def __str__(self):
        return self.pretty_print(indent=None)

    def __contains__(self, key):
        return key in self.__data__

    def __len__(self):
        return len(self.__data__)

    def pretty_print(self, indent=4):
        return json.dumps(self, cls=RestEncoder, indent=indent)

    def __dir__(self):
        return dir(self.__data__) + list(self.keys())

    def __delattr__(self, name):
        if name in self.__data__:
            del self.__data__[name]
            self.changed()

    def clear(self):
        self.__data__ = {}
        self.changed()

    def pop(self, name, default=None):
        if name in self.__data__:
            value = self.__data__.pop(name)
            self.changed()
            return value
        else:
            return default

    def popitem(self):
        key_value = self.__data__.popitem()
        self.changed()
        return key_value

    def __iter__(self):
        for x in self.keys():
            yield x

    def __eq__(self, other):
        if type(other) == type(self):
            return self.__data__ == other.__data__
        else:
            return False

    def __bool__(self):
        return bool(self.__data__)

    def __nonzero__(self):
        return bool(self.__data__)

    def __getattr__(self, name):
        if name in self.__data__:
            return self.__data__.get(name)
        elif name == '__clause_element__':
            # SQLAlchmey TypeDecorator support
            # if we don't filter this prop, SQLAlchemy will __call__ on NoneProp
            raise AttributeError(name)
        elif name == '__parent__':
            return self.__parent__
        else:
            return NoneProp(self, name)

    def __setattr__(self, name, value):
        if name == '__data__' or name == '__parent__':
            super(RestObject, self).__setattr__(name, value)
        else:
            self._update_object({name: value})

    def __getitem__(self, name):
        if name not in self.__data__:
            return NoneProp(self, name)
        else:
            return self.__data__.__getitem__(name)

    def __setitem__(self, name, value):
        self.__setattr__(name, value)

    def keys(self):
        return self.__data__.keys()

    def get(self, key, default=None):
        return self.__data__.get(key, default)

    def has_key(self, key):
        return key in self.__data__

    def items(self):
        return self.__data__.items()

    def iteritems(self):
        return six.iteritems(self.__data__)

    def iterkeys(self):
        return self.__data__.iterkeys()

    def itervalues(self):
        return self.__data__.itervalues()

    def values(self):
        return self.__data__.values()

    def viewitems(self):
        return self.__data__.viewitems()

    def viewkeys(self):
        return self.__data__.viewkeys()

    def viewvalues(self):
        return self.__data__.viewvalues()

    def update(self, data):
        if isinstance(data, dict):
            self._update_object(data)

    def _init_data(self, v):
        if isinstance(v, dict) and not isinstance(v, RestObject):
            return RestObject(v, parent=self, **self.__opts__)
        elif isinstance(v, list) and not isinstance(v, RestList):
            return RestList(v, parent=self, **self.__opts__)
        else:
            return utils.decode_item(v, **self.__opts__)

    def _update_object(self, data):
        for k, v in six.iteritems(data):
            self.__data__[k] = self._init_data(v)
        self.changed()


class RestResponse(object):
    def __new__(self, data, **kwargs):
        if isinstance(data, str) or not utils.PYTHON3 and isinstance(data, unicode):
            return RestResponse.loads(data, **kwargs)
        else:
            return RestResponse.parse(data, **kwargs)

    @staticmethod
    def parse(data, parent=None, **kwargs):
        if isinstance(data, RestResponseObj) or isinstance(data, NoneProp):
            return data
        elif isinstance(data, dict):
            return RestObject(data, parent=parent, **kwargs)
        elif isinstance(data, list):
            return RestList(data, parent=parent, **kwargs)
        elif isinstance(data, type(None)):
            return RestObject({}, parent=parent, **kwargs)
        else:
            return utils.encode_item(data, **kwargs)

    @staticmethod
    def loads(data, **kwargs):
        try:
            data = json.loads(data)
        except Exception:
            raise ValueError('RestResponse data must be JSON deserializable')

        return RestResponse.parse(data, **kwargs)


class ApiModel(object):
    __opts__ = {
        'encode_binary': False,
        'encode_callable': False,
        'decode_binary': False,
        'decode_callable': False,
        'encode_datetime': lambda x: datetime.strftime(x, '%Y-%m-%dT%H:%M:%SZ'),
        'encode_date': lambda x: datetime.strftime(x, '%Y-%m-%d'),
        '_overrides': [],
    }

    def __bool__(self):
        return bool(self._data)

    def __nonzero__(self):
        return bool(self._data)

    def __eq__(self, other):
        if not isinstance(other, ApiModel):
            return False
        return self._data == other._data

    @property
    def _data(self):
        return self.__data

    @_data.setter
    def _data(self, data):
        data = data or RestResponse.parse({}, **self.__opts__)
        if isinstance(data, dict) or isinstance(data, list):
            data = RestResponse.parse(data, **self.__opts__)
        elif isinstance(data, str) or not utils.PYTHON3 and isinstance(data, unicode):
            try:
                data = RestResponse.loads(data or "{}", **self.__opts__)
            except ValueError as e:
                six.raise_from(ValueError('{0} data must be JSON serializable'.format(self.__class__)), e)
        elif isinstance(data, ApiModel):
            data = data._data

        self.__data = RestResponse.parse({})
        for prop in dir(self):
            if (not prop.startswith('_') or prop in self.__opts__.get('_overrides', [])) and prop in data:
                eval('self.__setattr__("{0}", data[prop])'.format(prop))

    @property
    def _as_json(self):
        return self._data()

    def _set_datetime(self, d, format='%Y-%m-%dT%H:%M:%SZ'):
        return self._format_datetime(d, format=format, raises_value_error=True)

    def _get_datetime(self, d, format='%Y-%m-%dT%H:%M:%SZ'):
        return self._format_datetime(d, format=format, raises_value_error=False)

    def _format_datetime(self, d, format='%Y-%m-%dT%H:%M:%SZ', raises_value_error=False):
        if not isinstance(d, datetime) or not isinstance(d, date):
            try:
                d = dateutil_parser.parse(d)
                return datetime.strptime(d.strftime(format), format)
            except ValueError:
                if raises_value_error:
                    raise
                else:
                    warnings.warn('Value must be date or datetime')
                    return None
        else:
            return d

    def _set_date(self, d, format='%Y-%m-%d'):
        return self._format_date(d, format=format, raises_value_error=True)

    def _get_date(self, d, format='%Y-%m-%d'):
        return self._format_date(d, format=format, raises_value_error=False)

    def _format_date(self, d, format='%Y-%m-%d', raises_value_error=False):
        if not isinstance(d, date):
            try:
                d = dateutil_parser.parse(d)
                return datetime.strptime(d.strftime(format), format).date()
            except ValueError:
                if raises_value_error:
                    raise
                else:
                    warnings.warn('Value must be date')
                    return None
        else:
            return d

    def _set_string(self, s):
        return self._format_string(s, raises_value_error=True)

    def _get_string(self, s):
        return self._format_string(s, raises_value_error=False)

    def _format_string(self, s, raises_value_error=False):
        if (
            raises_value_error and (
                utils.PYTHON3 and not isinstance(s, str)
                or not utils.PYTHON3 and not isinstance(s, str) and not isinstance(s, unicode)
            )
        ):
            raise ValueError('Value must be str')
        return '%s' % (s or '')

    def _set_float(self, f):
        return self._format_float(f, raises_value_error=True)

    def _get_float(self, f):
        return self._format_float(f, raises_value_error=False)

    def _format_float(self, f, raises_value_error=False):
        try:
            return float(f)
        except (ValueError, TypeError):
            if raises_value_error:
                raise
            else:
                warnings.warn('Value must be float')
                return None

    def _set_int(self, i):
        return self._format_int(i, raises_value_error=True)

    def _get_int(self, i):
        return self._format_int(i, raises_value_error=False)

    def _format_int(self, i, raises_value_error=False):
        try:
            return int(i)
        except (ValueError, TypeError):
            if raises_value_error:
                raise
            else:
                warnings.warn('Value must be integer')
                return None

    def _set_bool(self, b):
        return self._format_bool(b, raises_value_error=True)

    def _get_bool(self, b):
        return self._format_bool(b, raises_value_error=False)

    def _format_bool(self, b, raises_value_error=False):
        if (
            raises_value_error
            and not isinstance(b, bool)
        ):
            raise ValueError('Value must be bool')
        return b in [True, 'True', 'true', '1', 1]


class ApiCollection(RestList):
    def __init__(self, setter, **setter_kwargs):
        self.setter = setter
        self.setter_kwargs = setter_kwargs

    @property
    def _data(self):
        if issubclass(self.setter, ApiModel):
            return RestResponse.parse([x._data for x in self])
        else:
            return RestResponse.parse([x for x in self])

    @property
    def _as_json(self):
        return self._data()

    def append(self, item):
        value = self.setter(item, **self.setter_kwargs)
        if value is not None:
            super(ApiCollection, self).append(value)

    def insert(self, index, item):
        value = self.setter(item, **self.setter_kwargs)
        if value is not None:
            super(ApiCollection, self).insert(index, value)

    def extend(self, items):
        for item in items:
            self.append(item)

    def __setitem__(self, index, value):
        if index >= 0 and index < len(self):
            self.pop(index)
            self.insert(index, value)
        else:
            raise IndexError('list index out of range')
