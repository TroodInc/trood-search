import json
import random


def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200, response.json()
    assert response.json() == {"status": "OK"}


def test_snippet_configuration(client, headers):
    response = client.get("/snippets/")
    assert response.status_code == 403
    response = client.get("/snippets/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {}
    snippet = {"tbl_index": ", snippet(text, '{match}') as __text"}
    response = client.post("/snippets/", headers=headers, json=snippet)
    assert response.status_code == 200
    assert response.json() == snippet
    response = client.delete(
        "/snippets/{snippet['tbl_index']}/", headers=headers, json=snippet,
    )
    assert response.status_code == 204
