import datetime

from dateutil import parser
from app.exceptions import ValidationError


class Field(object):
    def __init__(self, required=True):
        self.required = required

    def validate(self, value):
        raise NotImplementedError


class CharField(Field):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValidationError('value must be string')
        return value


class DateField(Field):
    def __init__(self, date_format='%Y-%m-%d', *args, **kwargs):
        self.format = date_format
        super(DateField, self).__init__(*args, **kwargs)

    def validate(self, value):
        if not isinstance(value, str):
            raise ValidationError('value must be string representing date')
        try:
            value = datetime.datetime.strptime(value, self.format).date()
        except ValueError:
            raise ValidationError('wrong datetime format')
        return value


class DatetimeField(Field):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValidationError('value must be string representing date')
        try:
            value = parser.parse(value)
        except ValueError:
            raise ValidationError('wrong datetime format')
        return value


class ListField(Field):
    def __init__(self, child_field_type, *args, **kwargs):
        self.child_field_type = child_field_type
        super(ListField).__init__(*args, **kwargs)

    def validate(self, value):
        if not isinstance(value, list):
            raise ValidationError('value must be list')
        try:
            for instance in value:
                self.child_field_type.validate(instance)
        except ValidationError as e:
            message = '[{}]'.format(e.message)
            raise ValidationError(message)
        return value


class Serializer(object):
    required_fields = {}
    fields = {}

    def __init__(self, data):
        self.is_validated = False
        self.initial_data = data.copy()
        self._validated_data = {}
        self.required_fields = {attr for attr, field in self.fields.items() if field.required}

    @property
    def validated_data(self):
        assert self.is_validated, 'You can\'t access validated data before calling is_valid()'
        return self._validated_data

    def is_valid(self):
        errors = {}
        validated_data = {}
        if not set(self.required_fields).issubset(set(self.initial_data.keys())):
            message = '{} are required fields'.format(list(self.required_fields))
            raise ValidationError(message)
        for attr, field in self.fields.items():
            try:
                if self.initial_data.get(attr):
                    validated_data[attr] = field.validate(self.initial_data[attr])
                elif attr in self.required_fields:
                    raise ValidationError('this field is required')
                else:
                    validated_data[attr] = None
            except ValidationError as e:
                errors[attr] = e.message
        if errors:
            raise ValidationError(errors)
        self.is_validated = True
        self._validated_data = validated_data
        return True


class DateRangeSerializer(Serializer):
    fields = {
        'date_from': DateField(),
        'date_to': DateField()
    }


