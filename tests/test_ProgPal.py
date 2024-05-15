import unittest
from unittest.mock import AsyncMock, patch, ANY
import asyncio
import sys
import os
from discord.ext.commands import Bot
from discord import Intents
sys.path.append("..")
from ProgPal import fetch_quiz_questions, QuizQuestion, ButtonView, bot, begin, random
from dotenv import load_dotenv

load_dotenv()

# Define the main bot token and test bot token from environment variables
bot_token = os.getenv("bot_token")

class TestBot(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Create the Bot instance for unit tests
        intents = Intents.default()
        intents.typing = False
        self.bot = Bot(command_prefix="/", intents=intents)

        # Add commands to the bot for testing
        self.bot.add_command(begin)
        self.bot.add_command(random)

        # Start the bot for unit testing
        await self.bot.start(bot_token)

    async def asyncTearDown(self):
        # Clean up after the unit tests
        await self.bot.close()
    
    async def test_fetch_quiz_questions(self):
        # Mock the API response
        mock_response = AsyncMock()
        mock_response.text = '[{"question": "Sample question", "answers": {}, "correct_answers": {}}]'
        
        with patch('ProgPal.requests.get', return_value=mock_response):
            # Call the fetch_quiz_questions function
            questions = await fetch_quiz_questions("category", "difficulty")

            # Assert that the returned data is as expected
            self.assertIsInstance(questions, list)
            self.assertTrue(all(isinstance(q, QuizQuestion) for q in questions))
            self.assertTrue(all(q.question for q in questions))

    async def test_button_view_initialization(self):
        # Create a sample QuizQuestion
        question_data = {
            "question": "Sample question",
            "answers": {"answer_a": "A", "answer_b": "B"},
            "correct_answers": {
                "answer_a_correct": "true",
                "answer_b_correct": "false"
            }
        }
        question = QuizQuestion(question_data)

        # Create a ButtonView instance
        view = ButtonView([question])

        # Assert the view attributes are initialized correctly
        self.assertEqual(view.questions, [question])
        self.assertEqual(view.index, 0)
        self.assertEqual(view.user_responses, [])

    async def test_button_view_next_question(self):
        # Create a sample QuizQuestion
        question_data = {
            "question": "Sample question",
            "answers": {"answer_a": "A", "answer_b": "B"},
            "correct_answers": {
                "answer_a_correct": "true",
                "answer_b_correct": "false"
            }
        }
        question = QuizQuestion(question_data)

        # Create a ButtonView instance
        view = ButtonView([question])

        # Mock interaction data for button callback
        mock_interaction = AsyncMock()
        mock_interaction.data = {'custom_id': 'answer_a'}

        # Call button_callback with mocked interaction
        await view.button_callback(mock_interaction)
        
        # Assert the expected behavior based on button callback
        mock_interaction.response.send_message.assert_called_once()

    async def test_random_command(self):
        # Mock the interaction
        interaction = AsyncMock()

        # Mocked command context
        mocked_response = "Mocked response"

        # Configure the behavior of interaction.response.send_message
        interaction.response.send_message.return_value = mocked_response

        # Simulate command invocation
        await bot.tree.get_command("random").callback(interaction)

        # Assert the awaited call to send_message with expected objects
        interaction.response.send_message.assert_awaited_with(
            embed=ANY,
            view=ANY
        )

    async def test_begin_command(self):
        # Mock the interaction
        interaction = AsyncMock()

        # Mocked command context
        mocked_response = "Mocked response"

        # Configure the behavior of interaction.response.send_message
        interaction.response.send_message.return_value = mocked_response

        # Simulate command invocation
        await bot.tree.get_command("begin").callback(interaction, category="category", difficulty="difficulty")

        # Assert the awaited call to send_message with expected embed and view (using ANY)
        interaction.response.send_message.assert_awaited_with(
            embed=ANY,
            view=ANY
        )

if __name__ == '__main__':
    asyncio.run(unittest.main())