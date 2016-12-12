import datetime

from dateutil import parser
from decimal import Decimal, InvalidOperation

from app.exceptions import ValidationError


class Field(object):
    def __init__(self, required=True, read_only=False):
        assert not (required and read_only), 'You can\'t set required_field to read_only'
        self.required = required
        self.read_only = read_only

    def validate(self, value):
        raise NotImplementedError


class CharField(Field):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValidationError('value must be string')
        return value


class ChoiceField(CharField):
    def __init__(self, choice, *args, **kwargs):
        super(ChoiceField, self).__init__(*args, **kwargs)
        self._available_values = set(choice)

    def validate(self, value):
        super(ChoiceField, self).validate(value)
        if value not in self._available_values:
            raise ValidationError('value must be one of following: {}'.format(list(self._available_values)))
        return value


class IntegerField(Field):
    def validate(self, value):
        if not isinstance(value, int):
            raise ValidationError('value must be int')
        return value


class DecimalField(Field):
    def validate(self, value):
        try:
            validated_value = Decimal(value)
        except (InvalidOperation, TypeError):
            raise ValidationError('value must be int or float')
        return str(validated_value)


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
    def __init__(self, child_field, *args, **kwargs):
        assert isinstance(child_field, Field) or isinstance(child_field, Serializer), (
            'List field should take Field or Serializer as child_field'
        )
        self.child_field = child_field
        super(ListField, self).__init__(*args, **kwargs)

    def validate(self, value):
        if not isinstance(value, list):
            raise ValidationError('value must be list')
        validated_data = []
        try:
            for instance in value:
                if isinstance(instance, Field):
                    validated_data.append(self.child_field.validate(instance))
                elif isinstance(instance, Serializer):
                    validated_data.append(self.child_field.is_valid())
        except ValidationError as e:
            message = [e.message, ]
            raise ValidationError(message)
        return validated_data


class Serializer(object):
    required_fields = {}
    fields = {}

    def __init__(self, data=None, many=False, required=True, read_only=False):
        self.is_validated = False
        self.many = many
        self.initial_data = None
        self.read_only = read_only
        if data:
            self.initial_data = data.copy()
        elif self.many:
            self.initial_data = []
        self._validated_data = {}
        self.required = required
        self.required_fields = {attr for attr, field in self.fields.items() if field.required}

    @property
    def validated_data(self):
        assert self.is_validated, 'You can\'t access validated data before calling is_valid()'
        return self._validated_data

    def is_valid(self):
        if self.initial_data is None:
            errors = {}
            for field in self.required_fields:
                errors[field] = 'this field is required'
            raise ValidationError(errors)
        elif self.many:
            for obj in self.initial_data:
                self._have_required_fields(obj)
        else:
            self._have_required_fields(self.initial_data)
        errors = {}
        if not self.many:
            validated_data, errors = self._validate_data(self.initial_data)
        else:
            validated_data = []
            for obj in self.initial_data:
                validated_object, errors = self._validate_data(obj)
                if errors:
                    raise ValidationError([errors, ])
                validated_data.append(validated_object)
        if errors:
            raise ValidationError(errors)
        self.is_validated = True
        self._validated_data = validated_data
        return True

    def _have_required_fields(self, data):
        keys = data.keys()
        if not set(self.required_fields).issubset(set(keys)):
            errors = {}
            for attr in self.required_fields:
                if attr not in keys:
                    errors[attr] = 'this field is required'
            if self.many:
                errors = [errors, ]
            raise ValidationError(errors)

    def _validate_data(self, data):
        errors = {}
        validated_data = {}
        fields = {attr: field for attr, field in self.fields.items() if not field.read_only}
        for attr, field in fields.items():
            try:
                if isinstance(self.fields.get(attr), Field) and data.get(attr):
                    validated_data[attr] = field.validate(data[attr])
                elif isinstance(self.fields.get(attr), Serializer) and data.get(attr):
                    field.initial_data = data.get(attr)
                    field.is_valid()
                    validated_data[attr] = field.validated_data
                elif attr in self.required_fields:
                    raise ValidationError('this field is required')
                else:
                    validated_data[attr] = None
            except ValidationError as e:
                errors[attr] = e.message
        return validated_data, errors


class DateRangeSerializer(Serializer):
    fields = {
        'date_from': DateField(),
        'date_to': DateField()
    }
