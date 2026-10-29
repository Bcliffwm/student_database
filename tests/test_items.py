import os

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "sqlite://"

from app.database.database import Base, get_db
from app.main import app


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)


def override_get_db():
    with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


def test_item_crud_flow():
    Base.metadata.create_all(bind=test_engine)
    with TestClient(app) as client:
        created = client.post("/items", json={"name": "Widget", "description": "Starter item"})
        assert created.status_code == 201
        item = created.json()
        assert item["name"] == "Widget"

        fetched = client.get(f"/items/{item['id']}")
        assert fetched.status_code == 200
        assert fetched.json()["description"] == "Starter item"

        updated = client.patch(f"/items/{item['id']}", json={"name": "Updated widget"})
        assert updated.status_code == 200
        assert updated.json()["name"] == "Updated widget"

        deleted = client.delete(f"/items/{item['id']}")
        assert deleted.status_code == 204
        assert client.get(f"/items/{item['id']}").status_code == 404

    Base.metadata.drop_all(bind=test_engine)