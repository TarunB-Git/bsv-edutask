import os
import pytest
import pymongo
from dotenv import dotenv_values
from src.util.dao import DAO
TEST_DB_NAME = "edutask_test"
TEST_USER_VALIDATOR = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["firstName", "lastName", "email"],
        "properties": {
            "firstName": {"bsonType": "string"},
            "lastName": {"bsonType": "string"},
            "email": {"bsonType": "string"},
        },
    },
}
@pytest.fixture(scope="session")
def mongo_url():
    local_mongo_url = dotenv_values('.env').get('MONGO_URL')
    return os.environ.get('MONGO_URL', local_mongo_url) or 'mongodb://localhost:27017'


@pytest.fixture(scope="session")
def test_mongo_client(mongo_url):
    client = pymongo.MongoClient(mongo_url)
    yield client
    client.close()


@pytest.fixture(scope="session")
def test_db(test_mongo_client):
    db = test_mongo_client[TEST_DB_NAME]
    db.drop_collection("user")
    db.create_collection("user", validator=TEST_USER_VALIDATOR)
    db["user"].create_index("email", unique=True)
    
    yield db  
    # Cleanup: drop entire test database after all tests
    test_mongo_client.drop_database(TEST_DB_NAME)

@pytest.fixture
def clear_collections(test_db):
    test_db["user"].delete_many({})
    yield

    test_db["user"].delete_many({})

@pytest.fixture
def user_dao(test_db, clear_collections):
    dao = DAO.__new__(DAO)
    dao.collection = test_db['user']
    return dao
