from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "Hacker News API": "API to fetch news from https://news.ycombinator.com/"}


def test_news():
    for page in range(10):
        response = client.get(f"/news/?page={page}")
        if page == 0:
            assert response.status_code == 400
            assert response.json() == {
                "detail": "Invalid page number. Page number must be greater than or equal to 1."}
        else:
            assert response.status_code == 200
            assert response.json()['page'] == str(page)
            assert len(response.json()['data']) == 30
