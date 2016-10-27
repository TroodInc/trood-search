from app import serializers


class EventSerializer(serializers.Serializer):
    fields = {
        'name': serializers.CharField(),
        'description': serializers.CharField(),
        'documents': serializers.ListField(child_field=serializers.CharField()),
        'source': serializers.CharField(),
        'created': serializers.DatetimeField()
    }

    async def save(self, cache):
        return cache.common.events.insert(self.validated_data)
