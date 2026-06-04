def test_api_docs_contains_predict_endpoint():
    with open("docs/api.md", "r") as f:
        content = f.read()
    assert "## /predict (POST)" in content
