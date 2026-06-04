import os

def test_api_docs_exists():
    assert os.path.exists("docs/api.md")
