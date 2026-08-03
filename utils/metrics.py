"""
Metrics Service
---------------
Métricas internas del SiriusBot OCR Engine.
"""


from datetime import datetime, timezone
from copy import deepcopy



DEFAULT_METRICS = {
    "requests_total": 0,
    "requests_success": 0,
    "requests_error": 0,
    "ocr_success": 0,
    "ocr_failed": 0,
    "total_processing_time": 0.0,
    "started_at": None,
}



class Metrics:
    """
    Administrador de métricas.
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



    def add_processing_time(
        self,
        seconds: float,
    ):
        """
        Acumula tiempo de procesamiento.
        """

        self._metrics[
            "total_processing_time"
        ] += seconds



    def get_metrics(self):
        """
        Devuelve copia independiente.
        """

        return deepcopy(
            self._metrics
        )



    def reset(self):
        """
        Reinicia métricas conservando claves existentes.
        """

        previous_metrics = getattr(
            self,
            "_metrics",
            {}
        )


        self._metrics = deepcopy(
            DEFAULT_METRICS
        )


        for key in previous_metrics:

            if key not in self._metrics:

                self._metrics[key] = 0


            else:

                self._metrics[key] = 0


        self._metrics[
            "started_at"
        ] = datetime.now(
            timezone.utc
        ).isoformat()



metrics = Metrics()
