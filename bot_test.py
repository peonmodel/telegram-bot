from unittest import IsolatedAsyncioTestCase
import asyncio
from bot import wild, initialise_template
from templates import template

# this file is for unittests for the bot
# py -m unittest .\bot.py

# stub classes
class Bot():
    async def send_message(*p1, **p2):
        pass
class Context():
    bot = Bot()
    def __init__(self, user_data):
        self.user_data = user_data
class Message():
    id = 0
    def __init__(self, text):
        self.text = text

class Update():
    effective_chat = Message(0)
    def __init__(self, text):
        self.message = Message(text)

class TestBot(IsolatedAsyncioTestCase):
    async def test_async(self):
        await asyncio.sleep(0.1)
        self.assertEqual(True, True)

    async def test_initialise_template(self):
        test_obj = initialise_template(template)
        self.assertEqual(test_obj['template'], template)
        self.assertEqual(len(test_obj['questions']), 13)
        # self.assertEqual(test_obj['expects'], [])
        # self.assertEqual(test_obj['record'], {})

    async def test_wild(self):
        test_obj = initialise_template(template)
        fake_context = Context({ 'form': test_obj })
        test_obj['questions'].pop()  # just pop it, dont have to run
        self.assertEqual(len(test_obj['questions']), 12)
        self.assertEqual(len(test_obj['expects']), 13)
        await wild(Update('aaa1'), fake_context)  # fill in project
        self.assertEqual(test_obj['record']['project'], 'aaa1')
        self.assertEqual(len(test_obj['questions']), 11)
        self.assertEqual(len(test_obj['expects']), 12)
        # print(test_obj['record'])
        await wild(Update('aaa2'), fake_context)  # fill in first attendee name
        self.assertEqual(test_obj['record']['attendees'], 'aaa2') # << supposed to fail!
        print(test_obj['record'])
