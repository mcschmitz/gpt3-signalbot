import argparse
import logging
import threading

from pysignalclirestapi import SignalCliRestApi
from signalbot import Message, SignalBot

from commands import GPT3Command
from contacts.groups import get_groups

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger("apscheduler").setLevel(logging.WARNING)

lock = threading.Lock()

parser = argparse.ArgumentParser(
    prog="GPT3-Signalbot ",
    description="A Signalbot that replies to your Signal messags using the GPT-3 API",
)
parser.add_argument(
    "--service",
    type=str,
    help="IP adress of your local signal service",
    required=True,
)
parser.add_argument(
    "--phone_number",
    type=str,
    help="Your phone number",
    required=True,
)
parser.add_argument(
    "--groups",
    type=str,
    nargs="+",
    help="Names of groups you want the bot to reply to. If none are iven, the bot will replly to all messages",
    required=False,
)


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

    if args.groups:
        bot = SignalBot(config)
        groups = get_groups(
            phone_number=args.phone_number,
            service=args.service,
        )
        for group in groups:
            if group["name"] in args.groups:
                bot.listen(group["id"], group["internal_id"])

    else:
        bot = ChatyBot(config)

    bot.register(GPT3Command())

    bot.start()
