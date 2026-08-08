"""
Métricas internas del SiriusBot OCR Engine.
"""

from copy import deepcopy
from datetime import datetime, timezone

DEFAULT_METRICS = {
    "requests_total": 0,
    "requests_success": 0,
    "requests_failed": 0,
    "ocr_success": 0,
    "ocr_failed": 0,
    "total_request_time": 0.0,
    "total_processing_time": 0.0,
    "started_at": None,
}


class Metrics:
    """
    Administrador de métricas del OCR Engine.
    """

    def __init__(self):
        self.reset()

    def increment(
        self,
        name: str,
        value: int = 1,
    ):
        """
        Incrementa una métrica.
        """

        if name not in self._metrics:
            self._metrics[name] = 0

        self._metrics[name] += value

    def add_request_time(
        self,
        seconds: float,
    ):
        """
        Acumula el tiempo total de las peticiones.
        """

        self._metrics["total_request_time"] += seconds

    def add_processing_time(
        self,
        seconds: float,
    ):
        """
        Acumula el tiempo total de procesamiento OCR.
        """

        self._metrics["total_processing_time"] += seconds

    def get_metrics(self):
        """
        Devuelve una copia independiente de las métricas
        junto con métricas calculadas.
        """

        result = deepcopy(self._metrics)

        started_at = datetime.fromisoformat(result["started_at"])

        result["uptime_seconds"] = round(
            (datetime.now(timezone.utc) - started_at).total_seconds(),
            2,
        )

        if result["requests_total"] > 0:
            result["average_processing_time"] = round(
                result["total_processing_time"] / result["requests_total"],
                4,
            )
        else:
            result["average_processing_time"] = 0

        return result

    def reset(self):
        """
        Reinicia las métricas conservando
        las métricas personalizadas existentes.
        """

        previous_metrics = getattr(
            self,
            "_metrics",
            {},
        )

        self._metrics = deepcopy(DEFAULT_METRICS)

        for key in previous_metrics:
            if key not in self._metrics:
                self._metrics[key] = 0

        self._metrics["started_at"] = datetime.now(timezone.utc).isoformat()


metrics = Metrics()
