# Install instructions

## Install Telegram Python Library and others

```
py.exe -m pip install python-telegram-bot -U --pre
py.exe -m pip install python-docx
py.exe -m pip install docx2pdf
```
https://github.com/python-telegram-bot/python-telegram-bot/wiki/Introduction-to-the-API

note that we are using the pre-release version v20.x, which requires the `-U --pre` flag

## Register Telegram

follow the botfather instructions: https://core.telegram.org/bots#6-botfather

In the Telegram app, search contact for `BotFather`, be sure to add the verified one & start conversation with it
run `\newbot` and give a name for the bot
for purpose of this course, let call it ~~~`scb203xxx_bot`~~~ (use the name of the bot registered with the BotFather)
a Telegram bot token will be generated, i.e. `0000000000:AAA1a-aaaaaaaaaaaaaaaaaa_aaaaaaa_aa`
### Security
For security reasons, telegram tokens are **NOT SHARED** and therefore need to be created for each user intending to use the code
create a file `config.py` to store the token and other sensitive information

A email account & its associated password should also be stored in config
```py
token = '0000000000:AAA1a-aaaaaaaaaaaaaaaaaa_aaaaaaa_aa'
gmail_password = "abcde"
email_address = "et@example.com"
```

## Run Python Script
in `bot.py`, import the token
```py
from config import token
```
then run the script `bot.py` via the cmd prompt in the folder where the file is saved
```
py .\bot.py
```
the code is based on: https://github.com/python-telegram-bot/python-telegram-bot/wiki/Extensions-%E2%80%93-Your-first-Bot

for other example, run the respective scripts, e.g.
```
py .\inlinekey.py
```
currently ignore helper.py & testsuites

# Design
- `/start` -> show options, MCQ for different templates
- flag internal variable for chat/user id -> selected template
- - flags / other user data can be stored in `context.user_data`
- - https://github.com/python-telegram-bot/python-telegram-bot/wiki/Storing-bot%2C-user-and-chat-related-data
- - python pickle is a file type, similar to JSON
- - https://github.com/python-telegram-bot/python-telegram-bot/wiki/Making-your-bot-persistent
- - https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples#persistentconversationbotpy
- - there should be an id for chat / message / user
- - ### Update
- - `update_id` (should be unique to every message)
- - `message`
- - ### CallbackContext
- - `application` (not sure if useful)
- - `chat_id` (note that there maybe more than 1 user per chat)
- - `user_id` (in case the user open a different chat)
- - https://docs.python-telegram-bot.org/en/v20.0a2/telegram.update.html?highlight=Update
- ask basic questions, e.g. project, comments, etc, flag questions asked accordingly
- `/undo` -> undo previous qn, rollback and ask again
- ~~`/end` -> for multi-line reply requested~~
- ask if want add new entry or end document
- ask if send draft for review by user (default) or email out / etc
- ## Template design
- - pickled, dictionary
- - Python Zen, `flat is better than nested`
- - using nested dict would require recursive function to transverse, which is a pain to write
- - strictly, there is no need for nested structure, the input by user is linear, the output document is also linearly presented
- - as such, a flat array with `keys` indicating relations will do that can be transversed with a simple `for` loop
- - a drawback is that values cannot be accessed with `dict[key]`, have to search in array with
```py
next(filter(lambda x: x['key']=='b', array))
```

reference for MCQ-ish: https://github.com/python-telegram-bot/python-telegram-bot/blob/67e7468366098f79cd2aa4f88b40e6e47d93ae5a/examples/conversationbot2.py

```py
# this is example data from CallbackQueryHandler
{
  'callback_query': {
    'message': {
      'reply_markup': {'inline_keyboard': [ [{'callback_data': 'template_1', 'text': 'Template 1'}], [{'callback_data': 'template_2', 'text': 'Template 2'}], [{'callback_data': 'template_3', 'text': 'Template 3'}], [{'callback_data': 'ok', 'text': 'OK'},{'callback_data': 'cancel', 'text': 'Cancel'}]]}, 
      'chat': {'id': 1355630254, 'type': <ChatType.PRIVATE>, 'first_name': 'courtyard', 'username': 'freelancecourt'}, 
      'text': 'Please choose a template:', 'group_chat_created': False, 'entities': [], 'new_chat_members': [], 'new_chat_photo': [], 'message_id': 49, 'delete_chat_photo': False, 'caption_entities': [], 'date': 1659778320, 'supergroup_chat_created': False, 'photo': [], 'channel_chat_created': False, 'from': {'is_bot': True, 'username': 'scb203bot001_bot', 'first_name': 'scb203bot001', 'id': 5410937306}
    }, 
    'chat_instance': '-5982173596949554534', 'id': '5822387606759324393', 'data': 'cancel', # chat instance is unique to chat, id is unique to update
    'from': <ditto>
  }, 
  'update_id': 698592125
}

# this is example data from MessageHandler / CommandHandler
{
  'update_id': 698592126, # running order, includes both to & fro
  'message': {
    'chat': {'id': 1355630254, 'type': <ChatType.PRIVATE>, 'first_name': 'courtyard', 'username': 'freelancecourt'}, 
    'text': 'ech', 
    'text': '/help', # CommandHandler
    'group_chat_created': False, 
    'entities': [], # MessageHandler
    'entities': [{'length': 5, 'type': <MessageEntityType.BOT_COMMAND>, 'offset': 0}], # CommandHandler
    'new_chat_members': [], 'new_chat_photo': [], 
    'message_id': 50, 'delete_chat_photo': False, 'caption_entities': [], 
    'date': 1659793330, 'supergroup_chat_created': False, 'photo': [], 'channel_chat_created': False, 
    'from': {'is_bot': False, 'username': 'freelancecourt', 'first_name': 'courtyard', 'id': 1355630254, 'language_code': 'en'}
  }
}
```

# Todo / To Check
- a way to know the picture is for what
- i.e. cannot just accept random pictures sent
- images sent need to be in response to query
- bot will ask for specific images first
- image sent
- ask for confirmation Yes / Cancel / Resend
- ask for remarks / captions / description
- (voice transcription)

there is no `telegram` way of doing this, just use flags

https://stackoverflow.com/questions/31912730/telegram-bot-keep-questions-and-

- need to change to webhooks / push activation instead of polling for efficiency
https://grammy.dev/guide/deployment-types.html#how-to-use-long-polling

# To Learn
- what is deeplinking / webhook
https://towardsdatascience.com/bring-your-telegram-chatbot-to-the-next-level-c771ec7d31e4

### Basic notes of Telegram Python script
#### Commands
the bot will respond to commands `\<command_name>` in the chat, e.g. `\do_stuff`
to add new commands that can be responded to, handlers are added
```py
async def do_stuffstuff():
  stuff() # python function definition of name do_stuffstuff
# ... other stuff
doStuff_handler = CommandHandler('command_name', do_stuffstuff) # 'do_stuff', this creates a handler
application.add_handler(doStuff_handler) # this register the handler to the bot
```
#### User Input (Text)
for the purpose of the bot, `context.args` is essentially `input("")`, i.e. a text string user input
```py
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper() # <<<<>>>>
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
```
#### User Input (Image)
```py
async def sendImage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # update.message.photo is a list of the 
    # same image with different size, last item biggest/original
    file = await update.message.photo[-1].get_file()
    await file.download('./'+file.file_id+'.jpg')
    await context.bot.send_message(chat_id=update.effective_chat.id, text='received')
```
