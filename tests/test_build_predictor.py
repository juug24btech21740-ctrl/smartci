from src.build_predictor import predict_build_failure


def test_build_success():
    data = {"error_count": 0}
    assert predict_build_failure(data) == "Success"


def test_build_failure():
    data = {"error_count": 3}
    assert predict_build_failure(data) == "Failure"


def test_build_failure_one_error():
    data = {"error_count": 1}
    assert predict_build_failure(data) == "Failure"