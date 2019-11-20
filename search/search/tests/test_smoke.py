import json
import random


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200, response.json()
    assert response.json() == {"status": "OK"}


def test_search(client):
    response = client.get("/search/?index=test_text_index")
    assert response.status_code == 200, response.json()


def test_index(client, headers):
    # TODO: Rollback test data
    # Clean index from previous test results.
    # for i in (58, 74, 40, 97):
    #     response = client.post(
    #         "/index/",
    #         headers=headers,
    #         json={ "object": "test_text", "action": "delete", "previous": {"id": i}, "current": {}},
    #     )
    id = random.randint(0, 100)
    response = client.post("/index/", headers=headers)
    assert response.status_code == 400, response.json()
    response = client.post(
        "/index/", headers=headers, json={"object": "test_text"}
    )
    assert response.status_code == 400, response.json()

    # Create index
    response = client.post(
        "/index/",
        headers=headers,
        json={
            "object": "test_text",
            "action": "create",
            "current": {"id": id, "text": "four"},
            "previous": {},
        },
    )
    assert response.status_code == 200, response.json()

    # Check is index created
    response = client.get(
        "/search/?index=rt_test_text_index&match=four", headers=headers
    )
    assert response.status_code == 200, response.json()
    assert len(response.json()['result']) == 1

    # Check is index updated
    response = client.post(
        "/index/",
        headers=headers,
        json={
            "object": "test_text",
            "action": "update",
            "current": {"id": id, "text": "five"},
            "previous": {},
        },
    )
    assert response.status_code == 200, response.json()

    response = client.get("/search/?index=rt_test_text_index", headers=headers)
    assert response.status_code == 200, response.json()
    assert len(response.json()['result']) == 1

    response = client.get(
        "/search/?index=rt_test_text_index&match=five", headers=headers
    )
    assert response.status_code == 200, response.json()
    assert len(response.json()['result']) == 1

    response = client.get(
        "/search/?index=rt_test_text_index&match=four", headers=headers
    )
    assert response.status_code == 200, response.json()
    assert len(response.json()['result']) == 0

    # Check is index deleted
    response = client.post(
        "/index/",
        headers=headers,
        json={
            "object": "test_text",
            "action": "delete",
            "previous": {"id": id, "text": "five"},
            "current": {},
        },
    )
    assert response.status_code == 200, response.json()

    response = client.get(
        "/search/?index=rt_test_text_index&match=five", headers=headers
    )
    assert response.status_code == 200, response.json()
    assert len(response.json()['result']) == 0

    response = client.get(
        "/search/?index=rt_test_text_index&match=four", headers=headers
    )
    assert response.status_code == 200, response.json()
    assert len(response.json()['result']) == 0

    response = client.get("/search/?index=rt_test_text_index", headers=headers)
    assert response.status_code == 200, response.json()
    assert len(response.json()['result']) == 0
