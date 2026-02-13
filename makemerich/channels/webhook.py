"""Generic webhook channel — send notifications to any HTTP endpoint."""

import aiohttp
from datetime import datetime
from makemerich.core.logger import get_logger


class WebhookChannel:
    """Send notifications to a generic webhook endpoint."""

    def __init__(self, url: str = None, headers: dict = None):
        self.url = url
        self.headers = headers or {"Content-Type": "application/json"}
        self.logger = get_logger("webhook")
        self._enabled = bool(url)

    async def notify(self, event: str, data: dict):
        """Send a webhook notification."""
        if not self._enabled:
            return

        payload = {
            "event": event,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }

        try:
            async with aiohttp.ClientSession() as session:
                await session.post(
                    self.url,
                    json=payload,
                    headers=self.headers,
                )
        except Exception as e:
            self.logger.error("Webhook failed", url=self.url, error=str(e))
