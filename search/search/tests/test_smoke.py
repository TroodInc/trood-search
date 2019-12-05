import json
import random


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200, response.json()
    assert response.json() == {"status": "OK"}


def test_search(client):
    response = client.get("/search/?index=test_text_index&match=understanding")
    assert response.status_code == 200, response.json()


def test_snippet_configuration(client, headers):
    response = client.get("/snippets/")
    assert response.status_code == 403
    response = client.get("/snippets/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {}
    snippet = {"test_text_index": ", snippet(text, '{match}') as __text"}
    response = client.post("/snippets/", headers=headers, json=snippet)
    assert response.status_code == 200
    assert response.json() == snippet
    response = client.delete(
        "/snippets/{snippet['test_text_index']}/",
        headers=headers,
        json=snippet,
    )
    assert response.status_code == 204


def test_index(client, headers):
    # TODO: Rollback test data
    # Clean index from previous test results.
    for i in range(1, 101):
        response = client.post(
            "/index/",
            headers=headers,
            json={
                "object": "test_text",
                "action": "delete",
                "previous": {"id": i},
                "current": {},
            },
        )
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
            "current": {
                "id": id,
                "text": "The first a user encounters when working with the system: it is important that the user interface (UI) is user-friendly, intuitive, and functional. The UI is one of the most customizable system components.\n\nTrood does not allow to create custom user interfaces without coding, as in practice it usually leads to an even longer time of development with poor UX in the result.\n\nWhat we provide is a set of unified components, integrated with Trood Core backend mechanisms, and a framework atop - React/Redux for web applications and React Native/Redux for mobile.",
            },
            "previous": {},
        },
    )
    assert response.status_code == 200, response.json()

    # Check is index created
    response = client.get(
        "/search/?index=test_text_index&match=components&select=id",
        headers=headers,
    )
    assert response.status_code == 200, response.json()
    assert len(response.json()["matches"]) == 1

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
    assert len(response.json()["matches"]) == 1

    response = client.get(
        "/search/?index=rt_test_text_index&match=five", headers=headers
    )
    assert response.status_code == 200, response.json()
    assert len(response.json()["matches"]) == 1

    response = client.get(
        "/search/?index=rt_test_text_index&match=components", headers=headers
    )
    assert response.status_code == 200, response.json()
    assert len(response.json()["matches"]) == 0

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
    assert len(response.json()["matches"]) == 0

    response = client.get(
        "/search/?index=rt_test_text_index&match=components", headers=headers
    )
    assert response.status_code == 200, response.json()
    assert len(response.json()["matches"]) == 0

    response = client.get("/search/?index=rt_test_text_index", headers=headers)
    assert response.status_code == 200, response.json()
    assert len(response.json()["matches"]) == 0
