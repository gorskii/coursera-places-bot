import os
from typing import Dict, List

import telebot
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.environ["PLACES_BOT_API_TOKEN"]

bot = telebot.TeleBot(API_TOKEN)

# store user data in memory for now
db = {
    "2397820": [
        {"title": f"Shop {i}", "address": f"Shop {i} address", "photo": "url"}
        for i in range(1, 21)
    ]
}


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
    result = db.get(user_id)
    return [] if not result else result[-10:]


def add_place(user_id):
    """Add place to list."""


def reset_user_data(user_id):
    """Remove user and its data."""


if __name__ == "__main__":
    bot.infinity_polling()
