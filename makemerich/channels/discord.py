"""Discord channel — notifications via Discord webhooks."""

import aiohttp
from makemerich.core.logger import get_logger


class DiscordChannel:
    """Send notifications via Discord webhook."""

    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url
        self.logger = get_logger("discord")
        self._enabled = bool(webhook_url)

    async def notify(self, message: str):
        """Send a notification via Discord webhook."""
        if not self._enabled:
            return

        try:
            async with aiohttp.ClientSession() as session:
                await session.post(
                    self.webhook_url,
                    json={"content": message},
                )
        except Exception as e:
            self.logger.error("Failed to send Discord message", error=str(e))

    async def notify_trade(self, decision):
        """Send a trade notification."""
        emoji = {"BUY": "🟢", "SELL": "🔴", "HOLD": "⏸️"}.get(decision.action, "❓")
        msg = (
            f"{emoji} **{decision.action} {decision.pair}**\n"
            f"Amount: `{decision.amount}`\n"
            f"Confidence: `{decision.confidence}`\n"
            f"Reason: {decision.reasoning[:200]}"
        )
        await self.notify(msg)
