from telegram.ext import Application, CommandHandler
from config import BOT_TOKEN
from handlers.start import start
from handlers.help import help_cmd
from handlers.info import info

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("info", info))

    print("VCChat Bot Started Successfully")

    app.run_polling()

if __name__ == "__main__":
    main()
