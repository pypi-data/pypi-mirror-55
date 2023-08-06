import json
import urllib

try:
    import typing
    has_typing = True
except ImportError:  # pragma: no cover
    has_typing = False  # pragma: no cover

from enum import Enum
from .schema import wrap_dict, wrap_raw_json


class Property(object):
    def __init__(self, type=str, name=None, default=None, enum=None,
                 required=False, validator=None, wrap=False, none=None,
                 is_list=False, calculated=False):

        self._check_type(type, is_list, default, none)

        self.serialized_name = name
        self.type = enum if enum else type
        self.enum = enum
        self.required = required
        self.validator = validator
        self.default = default
        self.wrap = wrap
        self.none = none
        self.is_list = is_list
        self._property_name = None
        self.calculated = calculated

    @staticmethod
    def _check_type(type, is_list, default, none):
        if type not in (str, int, float, bool) or is_list:
            if default is not None:
                raise ValueError('Can only use default values for simple types')
            elif none is not None:
                raise ValueError('None value only makes sense for simple types')

        if is_list and not issubclass(type, PropertySet):
            raise ValueError('Please use is_list only with ProperySet')

    def __property_config__(self, model_class, property_name):
        self.model_class = model_class
        self._property_name = property_name
        if self.serialized_name is None:
            self.serialized_name = property_name

        if has_typing and hasattr(model_class, '__annotations__'):
            annotation = model_class.__annotations__.get(property_name)
            if annotation is not None:
                if hasattr(annotation, '__origin__') and annotation.__origin__ in (list, typing.List):
                    is_list = True
                    type = annotation.__args__[0]
                    if isinstance(type, typing.TypeVar):
                        raise TypeError('List annotations must be typed (just "List" is not supported)')
                elif hasattr(annotation, '__origin__') and annotation.__origin__ in (dict, typing.Dict):
                    is_list = False
                    type = dict
                elif issubclass(annotation, (EnumProperty, )):
                    is_list = False
                    type = str
                    self.enum = annotation
                else:
                    is_list = False
                    type = annotation

                self._check_type(type, is_list, self.default, self.none)
                self.is_list = is_list
                self.type = type

    def __get__(self, model_instance, model_class):
        if model_instance is None:
            return self

        if self.type in (dict, list) or self.is_list:
            try:
                value = getattr(model_instance, self.property_name)
                if self.is_list and value is None:
                    value = list()
                return value
            except AttributeError:
                if self.is_list:
                    value = list()
                else:
                    value = self.type()
                setattr(model_instance, self.property_name, value)
                return value
        else:
            try:
                value = getattr(model_instance, self.property_name)
            except AttributeError:
                value = self.default
            if value is None:
                return self.none
            else:
                return value

    def __set__(self, model_instance, value):
        value = self.validate(value)
        setattr(model_instance, self.property_name, value)

    def __delete__(self, model_instance):
        value = self.validate(None)
        setattr(model_instance, self.property_name, value)

    def is_empty(self, value):
        return value is None

    def validate(self, value):
        # Required
        if value is None and not self.required:
            return None
        elif value is None and self.is_empty(value):
            raise ValueError("Property %s is required" % self._property_name)

        # Bool
        if self.type is bool:
            try:
                if isinstance(value, bool):
                    pass
                elif value == 0:
                    value = False
                elif value == 1:
                    value = True
                elif value.lower() in ('yes', 'true', '1'):
                    value = True
                elif value.lower() in ('no', 'false', '0'):
                    value = False
                else:
                    raise ValueError('Invalid bool value %s' % str(value))
            except AttributeError:
                raise ValueError('Invalid bool value %s' % str(value))

        # PropertySet - Static
        elif issubclass(self.type, PropertySet):
            if isinstance(value, dict):
                value = self.type.FromDict(value)
            elif isinstance(value, str):
                value = self.type.FromJSON(value)

        # PropertySet - Wrapped (Dynamic)
        elif self.wrap:
            if isinstance(value, dict):
                value = wrap_dict(value)
            elif isinstance(value, str):
                value = wrap_raw_json(value)

        # Enum
        elif self.enum:
            value = self.enum(value)

        # Built-ins
        elif self.type in (int, float, str, bool):
            value = self.type(value)

        # Regular list or dict
        elif self.type in (list, dict):
            if not issubclass(value.__class__, self.type):
                raise ValueError('Property %s must be of type %s (was %s)' %
                                 (self._property_name, repr(self.type), value.__class__))

        # External Validator
        if callable(self.validator):
            self.validator(value)

        return value

    @property
    def property_name(self):
        return '_' + self._property_name

    @property
    def is_embedded(self):
        return hasattr(self.type, 'to_dict') and callable(getattr(self.type, 'to_dict'))


def _initialize_properties(model_class, name, bases, dct):
    model_class._properties = {}
    property_source = {}

    def get_attr_source(name, cls):
        for src_cls in cls.mro():
            if name in src_cls.__dict__:
                return src_cls

    defined = set()

    for base in bases:
        if hasattr(base, '_properties'):
            property_keys = set(base._properties.keys())
            duplicate_property_keys = defined & property_keys
            for dupe_prop_name in duplicate_property_keys:
                old_source = property_source[dupe_prop_name] = get_attr_source(
                    dupe_prop_name, property_source[dupe_prop_name]
                )
                new_source = get_attr_source(dupe_prop_name, base)
                if old_source != new_source:
                    raise AttributeError(
                        'Duplicate property, %s, is inherited from both %s and %s.' %
                        (dupe_prop_name, old_source.__name__, new_source.__name__)
                     )

        property_keys -= duplicate_property_keys
        if property_keys:
            defined |= property_keys
            property_source.update(dict.fromkeys(property_keys, base))
            model_class._properties.update(base._properties)

    for property_name in dct.keys():
        prop = dct[property_name]
        if isinstance(prop, Property):
            if property_name in defined:
                raise AttributeError('Duplicate property: %s' % property_name)
            defined.add(property_name)
            model_class._properties[property_name] = prop
            prop.__property_config__(model_class, property_name)

    model_class._all_properties = tuple(
        (prop._property_name, prop.serialized_name) for name, prop in model_class._properties.items()
    )


class ClassWithProperties(type):
    def __init__(cls, name, bases, dct):
        super(ClassWithProperties, cls).__init__(name, bases, dct)
        _initialize_properties(cls, name, bases, dct)


class PropertySet(metaclass=ClassWithProperties):
    def __init__(self, *args, **values):
        if len(args) == 1:
            self.from_dict(args[0])
        for key, value in values.items():
            setattr(self, key, value)

    def to_json(self, pretty=True, include_calculated=False):
        return json.dumps(
            self,
            default=lambda x: x.to_dict(include_calculated=include_calculated),
            indent=(2 if pretty else None),
            sort_keys=True
        )

    def from_json(self, json_string, include_calculated=False):
        if json_string is None:
            self.from_dict({})
        else:
            self.from_dict(json.loads(json_string), include_calculated=include_calculated)

    def to_dict(self, include_calculated=False):
        dct = {}
        for property_name, dict_name in self._all_properties:
            value = getattr(self, property_name)
            prop = self._properties[property_name]
            if not include_calculated and prop.calculated:
                continue
            try:
                if prop.is_list and value is not None:
                    dct[dict_name] = [value.to_dict(include_calculated=include_calculated) for value in value]
                else:
                    dct[dict_name] = value.to_dict(include_calculated=include_calculated)
            except AttributeError:
                dct[dict_name] = value
        dct['*schema'] = self.__class__.__name__
        return dct

    def from_dict(self, dct, include_calculated=False):
        for property_name, dict_name in self._all_properties:
            if dict_name in dct:
                prop = self._properties[property_name]
                if not include_calculated and prop.calculated:
                    continue
                if prop.is_list:
                    setattr(self, property_name, [
                        prop.type.FromDict(d, include_calculated=include_calculated) for d in dct.get(dict_name)
                    ])
                else:
                    setattr(self, property_name, dct.get(dict_name))

    @classmethod
    def FromDict(cls, dct, include_calculated=False):
        if dct is not None:
            inst = cls()
            inst.from_dict(dct, include_calculated=include_calculated)
            return inst

    @classmethod
    def FromJSON(cls, json_string, include_calculated=False):
        inst = cls()
        inst.from_json(json_string, include_calculated=include_calculated)
        return inst


class Query(PropertySet):
    def to_query_string(self):
        return urllib.parse.urlencode(
            tuple(
                (str(key), str(value))
                for key, value
                in sorted(self.to_dict().items())
                if not key.startswith('*')
            )
        )


class EnumProperty(Enum):
    def to_dict(self, **kwargs):
        return self.name
