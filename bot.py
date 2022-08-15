import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext
from config import token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
) # not sure where to check the log
logger = logging.getLogger(__name__) # not sure what this line do

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def template_reader(dict = {}):
    # check for fields, list, options
    print()
    # if dict['fields'] != None:
    #     for field in dict.fields:

async def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("Template 1", callback_data='template_1')],
        [InlineKeyboardButton("Template 2", callback_data='template_2')],
        [InlineKeyboardButton("Template 3", callback_data='template_3')],
        [ InlineKeyboardButton("OK", callback_data='ok'), InlineKeyboardButton("Cancel", callback_data='cancel'),],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose a template:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    print('=== === user_data === ===')
    print(context.user_data)
    # store user option
    context.user_data['selected_template'] = query.data # flag the template
    stored_templates = {}  # dummy store for now
    # get template
    template = stored_templates.get(query.data)
    if template == None:
        # alias for await bot.answer_callback_query(update.callback_query.id, *args, **kwargs)
        await query.answer(text=f"Invalid template: {query.data}")
    else:
        await query.answer(text=f"Selected template: {query.data}") # required, even if just to register the click
    # some how query the template to find the next step
    # flag next step, template flag alone doesnt tell me which step


async def help_command(update: Update, context: CallbackContext):
    """Displays info on how to use the bot."""
    # having -> None in this function seemed to give an error?
    print('=== === user_data === ===')
    print(context.user_data)
    await update.message.reply_text("Use /start to test this bot.") # to add useful info

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main() -> None:
    """Run the bot."""
    application = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    help_handler = CommandHandler('help', help_command)
    application.add_handler(help_handler)

    button_handler = CallbackQueryHandler(button)
    application.add_handler(button_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()