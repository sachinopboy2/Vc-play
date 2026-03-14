from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN

from start import start
from help import help_cmd
from info import info


def main():

    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("info", info))

    print("""
==============================
 VCCHAT BOT STARTED
==============================
Server : VPS
Status : Running
""")

    app.run_polling()


if __name__ == "__main__":
    main()
