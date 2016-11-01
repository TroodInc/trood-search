from app import serializers


class AnswerSerializer(serializers.Serializer):
    fields = {
        'title': serializers.CharField(),
        'count': serializers.IntegerField(),
    }


class QuestionSerializer(serializers.Serializer):
    fields = {
        'title': serializers.CharField(),
        'uuid': serializers.CharField(),
        'score': serializers.IntegerField(),
        'answers': AnswerSerializer(many=True),
    }


class SectionSerializer(serializers.Serializer):
    fields = {
        'title': serializers.CharField(),
        'uuid': serializers.CharField(),
        'score': serializers.IntegerField(),
        'questions': QuestionSerializer(many=True),
    }


class BlockSerializer(serializers.Serializer):
    fields = {
        'title': serializers.CharField(),
        'uuid': serializers.CharField(),
        'score': serializers.IntegerField(),
        'sections': SectionSerializer(many=True),
    }


class ProjectBlockSerializer(serializers.Serializer):
    fields = {
        'id': serializers.IntegerField(),
        'title': serializers.CharField(),
        'score': serializers.IntegerField(),
        'blocks': BlockSerializer(many=True),
    }


class ProjectSerializer(serializers.Serializer):
    fields = {
        'project_id': serializers.IntegerField(),
        'project_title': serializers.CharField(),
        'score': serializers.IntegerField(),
    }


class DynamicReportSerializer(serializers.Serializer):
    fields = {
        'id': serializers.IntegerField(),
        'title': serializers.CharField(),
        'tags': serializers.ListField(child_field=serializers.CharField()),
        'region': serializers.CharField(),
        'csi_projects': ProjectSerializer(many=True),
        'ms_projects': ProjectSerializer(many=True),
        'ce_projects': ProjectSerializer(many=True),
    }

    async def save(self, cache):
        return cache.mirror.dynamic_report.insert(self.validated_data)


class SummaryReportSerializer(serializers.Serializer):
    fields = {
        'id': serializers.IntegerField(),
        'title': serializers.CharField(),
        'tags': serializers.ListField(child_field=serializers.CharField()),
        'region': serializers.CharField(),
        'csi_score': serializers.IntegerField(),
        'ms_score': serializers.IntegerField(),
        'ce_score': serializers.IntegerField(),
        'csi_projects': ProjectBlockSerializer(many=True),
        'ms_projects': ProjectBlockSerializer(many=True),
        'ce_projects': ProjectBlockSerializer(many=True),
    }

    async def save(self, cache):
        return cache.mirror.summary_report.insert(self.validated_data)
