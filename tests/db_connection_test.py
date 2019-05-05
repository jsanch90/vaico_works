import pytest
import pymongo

@pytest.fixture()
def test_connection():
    client = pymongo.MongoClient("mongodb+srv://vaico:7iBcC3Pqk3RuNnYK@vaicorockets-05ijn.mongodb.net/test?retryWrites=true")
    return (type(client.server_info()) is dict)

@pytest.fixture()
def test_bad_connection():
    try:
        pymongo.MongoClient("mongodb+srv://vaico:7iBC3Pqk3RuNnYK@vaicorockets-0jn.mongodb.net/test?retryWrites=true")
    except:
        return False

def test_answer(test_connection, test_bad_connection):
    res = test_connection
    res2 = test_bad_connection
    assert res == True
    assert res2 == False