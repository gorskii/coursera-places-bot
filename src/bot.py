from typing import Dict, List

import telebot

from app import config
from app.storage import RedisStorage

bot = telebot.TeleBot(config.API_TOKEN)

db = RedisStorage(config.REDIS_URL)


@bot.message_handler(commands=["list"])
def handle_list_command(message):
    places = get_places(str(message.chat.id))

    if not places:
        bot.send_message(
            message.chat.id,
            text="No recent places. Please add a place using /add command",
        )
    else:
        for item in places:
            bot.send_message(message.chat.id, text="\n".join(item.values()))


def get_places(user_id: str) -> List[Dict[str, str]]:
    """Return 10 recent places for a user."""
    return db.get(user_id, start=0, end=9)


def add_place(user_id):
    """Add place to list."""


def reset_user_data(user_id):
    """Remove user and its data."""


if __name__ == "__main__":
    bot.infinity_polling()
