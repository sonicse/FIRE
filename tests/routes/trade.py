import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_list_empty(
    app: FastAPI, client: TestClient, valid_auth_token: str
) -> None:
    url = app.url_path_for('dataset:list')
    response = await client.get(
        url,
        headers={
            'Authorization': valid_auth_token,
        },
    )
    assert response.status_code == 200
    assert response.json() == {'count': 0, 'items': []}
