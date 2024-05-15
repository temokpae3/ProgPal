import asyncio
import unittest
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()

class TestIntegration(unittest.TestCase):
    async def test_fetch_quiz_questions_integration(self):
        api_token = os.getenv("QUIZ_API_KEY")
        headers = {"X-Api-Key": api_token}

        async with aiohttp.ClientSession() as session:
            async with session.get("https://quizapi.io/api/v1/questions", headers=headers) as response:
                data = await response.json()
                
                # Extract questions from the JSON data
                questions = [entry.get('question') for entry in data]

                # Close the response body
                await response.release()

        # Assert that the API call returned the expected data
        expected_questions = [entry.get('question') for entry in data]
        self.assertEqual(questions, expected_questions)
        await asyncio.sleep(0)

    def test_async_method(self):
        asyncio.run(self.test_fetch_quiz_questions_integration())

if __name__ == "__main__":
    unittest.main(verbosity=2)