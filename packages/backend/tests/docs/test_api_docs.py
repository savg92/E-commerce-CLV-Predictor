def test_api_docs_contains_predict_endpoints():
    with open("docs/api.md", "r") as f:
        content = f.read()
    assert "### 1. `/predict` (POST)" in content
    assert "### 2. `/predict/batch` (POST)" in content

