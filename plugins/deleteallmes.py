import logging
from telegram import Update
from info import BOT_TOKEN ,ADMINS
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with the actual API token of your bot.
bot_token = BOT_TOKEN

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Command handler to handle the /alldelete command
def all_delete(update: Update, _: CallbackContext) -> None:
    user = update.effective_user
    if user is not None:
        # Check if the user is the bot's owner or authorized to use the command (optional)
        if user.id in ADMINS:
            for message in update.effective_message.bot.get_updates():
                try:
                    message.effective_message.delete()
                except Exception as e:
                    logger.error(f"Error deleting message: {e}")
        else:
            update.message.reply_text("You are not authorized to use this command.")
    else:
        update.message.reply_text("You need to send this command in a group.")

def main() -> None:
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    # Handler to handle the /alldelete command
    dispatcher.add_handler(CommandHandler("alldelete", all_delete))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process is interrupted
    updater.idle()

if __name__ == 'main':
    main()
