"""
Tests Metrics
-------------
Pruebas unitarias para el sistema
de métricas del OCR Engine.
"""

from utils.metrics import (
    Metrics,
    metrics,
)


def test_global_metrics_instance():

    assert isinstance(
        metrics,
        Metrics,
    )


def test_increment_existing_metric():

    metric = Metrics()

    metric.increment("ocr_success")

    result = metric.get_metrics()

    assert result["ocr_success"] == 1


def test_increment_new_metric():

    metric = Metrics()

    metric.increment("custom_metric")

    result = metric.get_metrics()

    assert result["custom_metric"] == 1


def test_add_request_time():

    metric = Metrics()

    metric.add_request_time(2.5)

    result = metric.get_metrics()

    assert result["total_request_time"] == 2.5


def test_reset_clears_metrics():

    metric = Metrics()

    metric.increment("ocr_failed")

    metric.add_request_time(10)

    metric.reset()

    result = metric.get_metrics()

    assert result["ocr_failed"] == 0

    assert result["total_request_time"] == 0.0


def test_get_metrics_returns_copy():

    metric = Metrics()

    data = metric.get_metrics()

    data["ocr_success"] = 999

    assert metric.get_metrics()["ocr_success"] == 0


def test_add_processing_time():
    metric = Metrics()

    metric.add_processing_time(2.5)

    result = metric.get_metrics()

    assert result["total_processing_time"] == 2.5


def test_average_processing_time():
    metric = Metrics()

    metric.increment("requests_total", 2)
    metric.add_processing_time(5.0)

    result = metric.get_metrics()

    assert result["average_processing_time"] == 2.5
