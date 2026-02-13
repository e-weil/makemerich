"""Telegram channel — notifications and commands via Telegram bot."""

import asyncio
from makemerich.core.logger import get_logger


class TelegramChannel:
    """Send notifications and receive commands via Telegram."""

    def __init__(self, config):
        self.config = config
        self.logger = get_logger("telegram")
        self.bot = None
        self._enabled = bool(config.telegram_bot_token and config.telegram_chat_id)

    async def start(self):
        """Start the Telegram bot."""
        if not self._enabled:
            self.logger.info("Telegram not configured, skipping")
            return

        try:
            from telegram import Bot
            self.bot = Bot(token=self.config.telegram_bot_token)
            self.logger.info("Telegram bot connected")
        except Exception as e:
            self.logger.error("Failed to start Telegram bot", error=str(e))

    async def notify(self, message: str):
        """Send a notification message."""
        if not self._enabled or not self.bot:
            return

        try:
            await self.bot.send_message(
                chat_id=self.config.telegram_chat_id,
                text=message,
                parse_mode="Markdown",
            )
        except Exception as e:
            self.logger.error("Failed to send Telegram message", error=str(e))

    async def notify_trade(self, decision):
        """Send a trade notification."""
        emoji = {"BUY": "🟢", "SELL": "🔴", "HOLD": "⏸️"}.get(decision.action, "❓")
        msg = (
            f"{emoji} *{decision.action} {decision.pair}*\n"
            f"Amount: `{decision.amount}`\n"
            f"Confidence: `{decision.confidence}`\n"
            f"Reason: {decision.reasoning[:200]}"
        )
        await self.notify(msg)

    async def notify_error(self, error: str):
        """Send an error notification."""
        await self.notify(f"⚠️ *Error*\n```{error}```")
