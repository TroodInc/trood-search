from app import serializers


class PointSerializer(serializers.Serializer):
    fields = {
        'x_value': serializers.DecimalField(),
        'y_value': serializers.DecimalField(),
    }


class LineChartSerializer(serializers.Serializer):
    fields = {
        'type': serializers.CharField(),
        'adaptor_id': serializers.IntegerField(required=False),
        'name': serializers.CharField(),
        'x_name': serializers.CharField(),
        'y_name': serializers.CharField(),
        'points': PointSerializer(many=True),
    }

    async def save(self, cache):
        await cache.common.reports.insert(self.validated_data)
        self._validated_data['id'] = str(self._validated_data['_id'])
        self._validated_data.pop('_id')


class BarSerializer(serializers.Serializer):
    fields = {
        'name': serializers.CharField(),
        'previous': serializers.DecimalField(),
        'current': serializers.DecimalField(),
    }


class BarChartSerializer(serializers.Serializer):
    fields = {
        'type': serializers.CharField(),
        'adaptor_id': serializers.IntegerField(required=False),
        'name': serializers.CharField(),
        'y_name': serializers.CharField(),
        'bars': BarSerializer(many=True),
    }

    async def save(self, cache):
        await cache.common.reports.insert(self.validated_data)
        self._validated_data['id'] = str(self._validated_data['_id'])
        self._validated_data.pop('_id')
