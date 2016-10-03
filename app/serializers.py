import datetime


class Serializer(object):
    required_fields = {}
    fields = {}

    def __init__(self, data):
        self.is_validated = False
        self._validated_data = {}
        self.initial_data = data.copy()

    @property
    def validated_data(self):
        assert self.is_validated, 'You can\'t access validated data before calling is_valid()'
        return self._validated_data


class DateRangeSerializer(Serializer):
    required_fields = {'date_from', 'date_to'}
    fields = {'date_from', 'date_to'}
    date_fields = {'date_from', 'date_to'}

    def is_valid(self):
        for key, value in self.initial_data.items():
            if key in self.fields:
                if key in self.date_fields:
                    self._validated_data[key] = datetime.datetime.strptime(value, '%Y-%m-%d').date()
                else:
                    self._validated_data[key] = self.initial_data.get(value)
        if not self.required_fields.issubset(self._validated_data.keys()):
            raise ValueError
        self.is_validated = True

