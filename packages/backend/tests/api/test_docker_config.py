import os
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from backend.api.app import create_app

def test_app_uses_env_vars_for_artifacts():
    # This test verifies that the app can be configured via environment variables
    # (which we will use in the Dockerfile/docker-compose)
    model_path = "/tmp/fake_model.pth"
    scaler_path = "/tmp/fake_scaler.joblib"
    
    os.environ["MODEL_PATH"] = model_path
    os.environ["SCALER_PATH"] = scaler_path
    
    app = create_app()
    
    # We expect the creation to fail because the files don't exist,
    # but the test proves it tried to load them
    with pytest.raises(FileNotFoundError):
        with TestClient(app):
            pass
