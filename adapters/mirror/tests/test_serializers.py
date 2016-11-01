import pytest

from adapters.mirror.reports.serializers import SummaryReportSerializer, DynamicReportSerializer
from app.exceptions import ValidationError

SUMMARY_DATA = [
    {
        "id": 130,
        "test": "test",
        "region": "test",
        "tags": [
            "tag1",
            "tag2"
        ],
        "title": "Test",
        "csi_score": 100,
        "ms_score": 100,
        "ce_score": 100,
        "csi_projects": [
            {
                "id": 1,
                "title": "project test",
                "score": 100,
                "blocks": [
                    {
                        "title": "test",
                        "uuid": "test",
                        "score": 100,
                        "sections": [
                            {
                                "title": "test",
                                "uuid": "test",
                                "score": 100,
                                "questions": [
                                    {
                                        "title": "test",
                                        "uuid": "test",
                                        "score": 100,
                                        "answers": [
                                            {
                                                "title": "test",
                                                "count": 1
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        "ce_projects": [],
        "ms_projects": []
    }
]

DYNAMIC_DATA = [
    {
        "id": 1,
        "test": "test",
        "region": "test",
        "tags": ["tag1", "tag2"],
        "title": "Test",
        "csi_projects": [
            {
                "project_id": 1,
                "project_title": "project test",
                "score": 100
            }
        ],
        "ce_projects": [
            {
                "project_id": 1,
                "project_title": "project test",
                "score": 100
            }
        ],
        "ms_projects": [
            {
                "project_id": 1,
                "project_title": "project test",
                "score": 99
            }
        ]
    }
]


def test_summary_report_serializer():
    serializer = SummaryReportSerializer(SUMMARY_DATA, many=True)
    assert serializer.is_valid()


def test_summary_report_serializer_wrong_object():
    data = SUMMARY_DATA.copy()
    data[0]['ce_projects'] = [{}]
    with pytest.raises(ValidationError):
        SummaryReportSerializer(data, many=True).is_valid()


def test_dynamic_serializer():
    serializer = DynamicReportSerializer(DYNAMIC_DATA, many=True)
    assert serializer.is_valid()
