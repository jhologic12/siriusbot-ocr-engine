"""
Rate limiter en memoria para el SiriusBot OCR Engine.
"""

from math import ceil
import time

from config import (
    RATE_LIMIT_REQUESTS,
    RATE_LIMIT_WINDOW_SECONDS,
)


class RateLimiter:
    """
    Rate limiter basado en una ventana temporal fija.
    """

    def __init__(
        self,
        max_requests: int,
        window_seconds: int,
    ):
        if max_requests <= 0:
            raise ValueError("max_requests must be greater than 0")

        if window_seconds <= 0:
            raise ValueError("window_seconds must be greater than 0")

        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = {}

    def is_allowed(
        self,
        client_key: str,
    ) -> bool:
        """
        Determina si una solicitud puede continuar.
        """

        now = time.monotonic()
        window_start = now - self.window_seconds

        timestamps = self._requests.get(
            client_key,
            [],
        )

        timestamps = [timestamp for timestamp in timestamps if timestamp > window_start]

        if len(timestamps) >= self.max_requests:
            self._requests[client_key] = timestamps
            return False

        timestamps.append(now)
        self._requests[client_key] = timestamps

        return True

    def get_retry_after(
        self,
        client_key: str,
    ) -> int:
        """
        Retorna los segundos restantes de la ventana
        para el cliente indicado.
        """

        timestamps = self._requests.get(
            client_key,
            [],
        )

        if not timestamps:
            return 0

        now = time.monotonic()
        oldest_timestamp = min(timestamps)

        remaining = oldest_timestamp + self.window_seconds - now

        return max(1, ceil(remaining))

    def reset(self) -> None:
        """
        Limpia todo el estado del limiter.
        """

        self._requests.clear()


rate_limiter = RateLimiter(
    max_requests=RATE_LIMIT_REQUESTS,
    window_seconds=RATE_LIMIT_WINDOW_SECONDS,
)
