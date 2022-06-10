import typing

if typing.TYPE_CHECKING:
    from coursebot.apps.bot.utils import MailSender

SUBSCRIPTION_CHANNELS: list[tuple[str, str]] = []
MAIL_SENDER: typing.Optional["MailSender"] = None
BOT_RUNNING: bool = True
