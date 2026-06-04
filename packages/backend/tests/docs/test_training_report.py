import os

def test_training_report_exists():
    assert os.path.exists("docs/training_report.md")
