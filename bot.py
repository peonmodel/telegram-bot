from cgitb import reset
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, CallbackContext
import json 
from config import token
from templates import stored_templates
import time
from generate_pdf import generate_pdf
from send_email import send_email
# year, month, day, hour, min = time.localtime()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with 2 inline buttons attached to select templates"""
    keyboard = [
        [InlineKeyboardButton("Simple Sample Template", callback_data='simple_template')],
        [InlineKeyboardButton("Toolbox Meeting Template", callback_data='toolbox_template')],
        [InlineKeyboardButton("OK", callback_data='ok'), InlineKeyboardButton(
            "Cancel", callback_data='cancel'), ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose a template:', reply_markup=reply_markup)

async def button(update: Update, context: CallbackContext) -> None:
    """callback function for when button is clicked"""
    query = update.callback_query
    if query.data in ['ok', 'cancel']:
        # to just cancel
        await reset_state(update, context)
        return
    context.user_data['selected_template'] = query.data  # flag the template
    # let user know which template is selected by them
    await query.answer(text=f"Selected template: {query.data}")
    # initialise record by generate a list of qna
    tracked = initialise_template(stored_templates[query.data])
    # store record in context.user_data
    context.user_data['form'] = tracked
    # run the first question
    first_fn = tracked['questions'].pop()
    await first_fn(update, context)

def initialise_template(template: dict):
    """initialise record based on template"""
    questions = []
    expects = []
    for field in template['fields']:
        if field['type'] in ['group', 'list']:
            continue
        question_fn, expect_fn = generate_question(field, questions, expects, template['fields'])
        questions.append(question_fn)
        expects.append(expect_fn)
    questions = list(reversed(questions))
    expects = list(reversed(expects))
    store = {
        'template': template,
        'questions': questions, # simple function to print query out for user to answer
        'expects': expects, # callback function to accept user input
        'record': [] # where input is stored
    }
    return store

def get_related_fields(field, fields):
    """get questions that belongs in the same fieldgroup
        e.g. zzz.aaa & zzz.bbb & zzz.ccc are together zzz={aaa:'',bbb:'',ccc:''}
    """
    arr = field['key'].split('.')
    arr.pop()
    path = '.'.join(arr)
    results = []
    for ele in fields:
        if ele['key'].startswith(path) and not ele['key'] == path:
            results.append(ele)
    return results

def generate_append_question(field, fields, index: int = 0):
    """for array-like items, append the group of questions that are together as a fieldgroup"""
    # first find the group of questions from fields
    async def add_more_q(update, context):
        """ask to add to array"""
        # should be button, YES/NO, but skipping for now
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Add More? Y/N')

    async def add_more_e(update, context):
        """expect whether to add to array"""
        reply = update.message.text
        if reply not in ['Y', 'y', 'yes', 'Yes', 'YES']:
            return
        else:
            # add question group to repeat
            group = get_related_fields(field, fields)
            questions = context.user_data['form']['questions']
            expects = context.user_data['form']['expects']
            for item in list(reversed(group)):
                q, e = generate_question(item, questions, expects, fields, index + 1)
                questions.append(q)
                expects.append(e)
        
    return add_more_q, add_more_e

def find_last_index(arr: list, cb):
    return len(arr) - 1 - next(e for e in enumerate(reversed(arr)) if cb(e[1]))[0]

def update_array_index(key: str, index: int = 0):
    arr = key.split('.')
    last_digit = find_last_index(arr, lambda x: str(x).startswith('['))
    arr[last_digit] = str(index)
    return '.'.join(arr)

def generate_question(field, questions: list, expects: list, fields: list, index: int = 0):
    """generates a question & expects pair"""
    async def question(update, context):
        """just print text to user asking for info"""
        await context.bot.send_message(chat_id=update.effective_chat.id, text=field['label'])

    async def expect(update, context):
        """callback for user input to the question"""
        reply = update.message.text
        record = context.user_data['form']['record']
        key = field['key']
        # part of the problem with flattening the nested dict is that relationship can be hard to navigate
        # to find which questions are "siblings" i.e. belonging to the same field group, need to scan them
        # via the key
        # a easier but dritier solution is to just add a isItem field to template
        # less elegant but since template is defined by us, its okay
        if 'isItem' in field and field['isItem']:
            key = update_array_index(key, index)
        record.append({ 'key': key, 'value': reply })

        if 'isLastItem' in field and field['isLastItem']:
            # insert `Add More?` question
            q, e = generate_append_question(field, fields, index)
            context.user_data['form']['questions'].append(q)
            context.user_data['form']['expects'].append(e)

    if field['type'] == 'image':
        async def expectImage(update, context):
            record = context.user_data['form']['record']
            file = await update.message.photo[-1].get_file()
            await file.download('./telegram input/'+file.file_id+'.jpg')
            await context.bot.send_message(chat_id=update.effective_chat.id, text='image received')
            key = field['key']
            if 'isItem' in field and field['isItem']:
                key = update_array_index(key, index)
            record.append({ 'key': key, 'value': file.file_id+'.jpg' })

            if 'isLastItem' in field and field['isLastItem']:
                # insert `Add More?` question
                q, e = generate_append_question(field, fields, index)
                context.user_data['form']['questions'].append(q)
                context.user_data['form']['expects'].append(e)
        return question, expectImage
    else:
        return question, expect

async def reset_state(update, context):
    """reset program in case of error
    """
    context.user_data.clear()
    text = "error encountered, program reset, /start to begin anew"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text)

async def wild(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """it accepts all callbacks, i.e. wild"""
    # a dirty try/except to catch every error
    try:
        tracked = context.user_data['form']
        # next chat
        # print('start', len(tracked['questions']))
        if len(tracked['expects']) == 0:
            # not expecting input
            # should throw some message informing user & reset state
            # treat that as out of scope for now, just return
            return
        expect_fn = tracked['expects'].pop()
        await expect_fn(update, context)
        # print('end', len(tracked['questions']))
        
        if len(tracked['questions']) == 0:
            year, month, day, hour, min, *_ = time.localtime()
            tracked['record'].append({
                'key': 'submittedBy', 'value': update.effective_user.username
            })
            tracked['record'].append({
                'key': 'submittedAt', 'value': '{}-{}-{}T{}:{}'.format(year, month, day, hour, min)
            })
            json_result = json.dumps(tracked['record'])
            await context.bot.send_message(chat_id=update.effective_chat.id, text=json_result)
            if tracked['template']['template_name'] == "simple_template_001":
                not_available = '{} not available for pdf generation, please select the other template'.format(tracked['template']['document_title'])
                await context.bot.send_message(chat_id=update.effective_chat.id, text=not_available)
                await reset_state(update, context)
                return
            await context.bot.send_message(chat_id=update.effective_chat.id, text="generating pdf")
            filename = await generate_pdf(tracked['template'], tracked['record'])
            await context.bot.send_message(chat_id=update.effective_chat.id, text="pdf generated")
            # should be a 2 step process, first ask whether to send email (Y/N), then ask for email address
            email_address = next(filter(lambda x: x['key']=='email', tracked['record']))['value']
            await context.bot.send_message(chat_id=update.effective_chat.id, text="sending to " + email_address)
            await send_email(email_address, tracked['record'], tracked['template'], filename)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="email sent")
            # reset state by clearing data, then inform user, tell them to /start again
            await context.bot.send_message(chat_id=update.effective_chat.id, text="to restart, send /start")
            context.user_data['form'] = None
            return
        next_fn = tracked['questions'].pop()
        await next_fn(update, context)
    except Exception as err:
        print(err)
        # always reset if anything wrong
        await reset_state(update, context)

def main() -> None:
    """Run the bot."""
    application = ApplicationBuilder().token(token).build()
    
    any_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), wild)
    application.add_handler(any_handler)

    sendImage_handler = MessageHandler(filters.PHOTO, wild)
    application.add_handler(sendImage_handler)

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    button_handler = CallbackQueryHandler(button)
    application.add_handler(button_handler)
    
    application.run_polling()

if __name__ == '__main__':
    main()
