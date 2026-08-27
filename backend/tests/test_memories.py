import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_memory(client: AsyncClient, auth_headers):
    response = await client.post(
        "/api/memories/",
        json={"content": "This is a test memory about AI."},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert "AI" in data["content"]
    assert "id" in data
    assert "vector_id" in data

@pytest.mark.asyncio
async def test_list_memories(client: AsyncClient, auth_headers):
    await client.post(
        "/api/memories/",
        json={"content": "Another memory for listing."},
        headers=auth_headers
    )
    
    response = await client.get("/api/memories/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

@pytest.mark.asyncio
async def test_get_memory(client: AsyncClient, auth_headers):
    create_res = await client.post(
        "/api/memories/",
        json={"content": "Memory to retrieve."},
        headers=auth_headers
    )
    memory_id = create_res.json()["id"]
    
    response = await client.get(f"/api/memories/{memory_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["id"] == memory_id

@pytest.mark.asyncio
async def test_update_memory(client: AsyncClient, auth_headers):
    create_res = await client.post(
        "/api/memories/",
        json={"content": "Original content."},
        headers=auth_headers
    )
    memory_id = create_res.json()["id"]
    
    response = await client.put(
        f"/api/memories/{memory_id}",
        json={"content": "Updated content about AI."},
        headers=auth_headers
    )
    assert response.status_code == 200
    assert "Updated" in response.json()["content"]

@pytest.mark.asyncio
async def test_delete_memory(client: AsyncClient, auth_headers):
    create_res = await client.post(
        "/api/memories/",
        json={"content": "Memory to delete."},
        headers=auth_headers
    )
    memory_id = create_res.json()["id"]
    
    response = await client.delete(f"/api/memories/{memory_id}", headers=auth_headers)
    assert response.status_code == 204
    
    get_res = await client.get(f"/api/memories/{memory_id}", headers=auth_headers)
    assert get_res.status_code == 404

@pytest.mark.asyncio
async def test_search_memories(client: AsyncClient, auth_headers):
    await client.post(
        "/api/memories/",
        json={"content": "The capital of France is Paris."},
        headers=auth_headers
    )
    
    response = await client.post(
        "/api/memories/search",
        json={"query": "Where is the Eiffel Tower?", "limit": 5},
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)