import argparse
import logging
import threading

from pysignalclirestapi import SignalCliRestApi
from signalbot import Message, SignalBot

from commands import GPT3Command

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

lock = threading.Lock()

parser = argparse.ArgumentParser(
    prog="GPT3-Signalbot ",
    description="A Signalbot that replies to your Signal messags using the GPT-3 API",
)
parser.add_argument("--service", type=str)
parser.add_argument("--phone_number", type=str)


class ChatyBot(SignalBot):
    def _should_react(self, message: Message) -> bool:
        return True


if __name__ == "__main__":
    args = parser.parse_args()

    signal_api = SignalCliRestApi(
        f"http://{args.service}",
        number=args.phone_number,
    )

    config = {
        "signal_service": args.service,
        "phone_number": args.phone_number,
        "storage": None,
    }
    bot = ChatyBot(config)

    bot.register(GPT3Command())

    bot.start()
