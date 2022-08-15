from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext
from templates import template

async def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [InlineKeyboardButton("Template 1", callback_data='template_1')],
        [InlineKeyboardButton("Template 2", callback_data='template_2')],
        [InlineKeyboardButton("Template 3", callback_data='template_3')],
        [InlineKeyboardButton("OK", callback_data='ok'), InlineKeyboardButton(
            "Cancel", callback_data='cancel'), ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose a template:', reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    context.user_data['selected_template'] = query.data  # flag the template
    stored_templates = {}  # dummy store for now
    # get template
    # template = stored_templates.get(query.data)
    await query.answer(text=f"Selected template: {query.data}")

    # assuming hard code
    # for field in template.fields
    await context.bot.send_message(chat_id=update.effective_chat.id, text=template.fields[0].label)
