import json
import os
import discord
from discord.ext import commands
from discord.ui import Button
import requests
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.tree.sync()

class QuizQuestion:
    def __init__(self, data):
        self.question = data.get("question")
        self.answers = {
            "a": data["answers"].get("answer_a"),
            "b": data["answers"].get("answer_b"),
            "c": data["answers"].get("answer_c"),
            "d": data["answers"].get("answer_d"),
            "e": data["answers"].get("answer_e"),
            "f": data["answers"].get("answer_f"),
        }
        self.correct_answers = {
            "a": data["correct_answers"].get("answer_a_correct"),
            "b": data["correct_answers"].get("answer_b_correct"),
            "c": data["correct_answers"].get("answer_c_correct"),
            "d": data["correct_answers"].get("answer_d_correct"),
            "e": data["correct_answers"].get("answer_e_correct"),
            "f": data["correct_answers"].get("answer_f_correct"),
        }

class ButtonView(discord.ui.View):
    def __init__(self, questions):
        super().__init__()
        self.questions = questions
        self.index = 0
        self.user_response = []

    async def button_callback(self, interaction: discord.Interaction):
        self.index += 1

        if self.index < len(self.questions):
            await self.show_next_question(interaction)
        else:
            await self.end_quiz(interaction)

        custom_id = interaction.data['custom_id']
        key = custom_id.split('_')[1]

        current_question = self.questions[self.index - 1]
        correct_answers = current_question.correct_answers

        if key in current_question.answers:
            # Check if the correct answer is marked as 'true'
            if correct_answers.get(key, "").lower() == "true":
                # Award a point for a correct answer
                self.user_response.append(1)
                await interaction.followup.send(content=f"Correct! The answer was: {current_question.answers[key]}.")
            else:
                self.user_response.append(0)
                await interaction.followup.send(content=f"Incorrect! The correct answer is: {self.get_correct_answer(current_question)}.")
        else:
            self.user_response.append(0)
            await interaction.followup.send(content=f"Incorrect! The correct answer is: {self.get_correct_answer(current_question)}.")

    async def show_next_question(self, interaction):
        question = self.questions[self.index]

        em = discord.Embed(
            title="Quiz", description=f"Question {self.index + 1}:", color=discord.Color.blue()
        )
        em.add_field(name="", value=question.question, inline=False)
        em.add_field(
            name="Options",
            value="\n".join(
                [f"{key.upper()}: {value}" for key, value in question.answers.items() if value]
            ),
            inline=False,
        )

        self.clear_items()

        for key, value in question.answers.items():
            if value is not None:
                button = Button(style=discord.ButtonStyle.primary, label=key.upper())
                button.custom_id = f"answer_{key.lower()}"
                self.add_item(button)
                button.callback = self.button_callback
            else:
                self.add_item(Button(style=discord.ButtonStyle.primary, label=key.upper(), disabled=True))

        await interaction.response.send_message(embed=em, view=self)

    async def end_quiz(self, interaction):
        total_questions = len(self.questions)
        correct_answers = sum(self.user_response)
        wrong_answers = total_questions - correct_answers
        score_percentage = (correct_answers / total_questions) * 100

        await interaction.response.send_message(
            content=f"Quiz ended! Correct answers: {correct_answers}, Wrong answers: {wrong_answers}, Score: {score_percentage:.2f}%."
        )

    def get_correct_answer(self, question):
        for key, value in question.correct_answers.items():
            if value.lower() == "true":
                return question.answers[key]

async def fetch_quiz_questions(category, difficulty):
    apiKey = os.getenv("QUIZ_API_KEY")
    url = "https://quizapi.io/api/v1/questions"
    headers = {"X-Api-Key": apiKey}

    response = requests.get(url, headers=headers)
    quiz_json = json.loads(response.text)

    filtered_questions = []

    for question_data in quiz_json:
        tags = question_data.get("tags", [])
        # Check if the question has the specified tag and matches the difficulty
        if any(tag.get("name") == category for tag in tags) and question_data.get("difficulty") == difficulty:
            filtered_questions.append(QuizQuestion(question_data))
        
    return filtered_questions


@bot.tree.command(name="regular", description="Start a regular quiz!")
async def regular(interaction: discord.Interaction, category: str, difficulty: str):
    questions = await fetch_quiz_questions(category, difficulty)
    if not questions:
        await interaction.response.send_message(content="No questions found for the specified category and difficulty.")
        return

    view = ButtonView(questions)
    await view.show_next_question(interaction)


@bot.tree.command(name="random", description="Start a random quiz")
async def random(interaction: discord.Interaction):
    apiKey = os.getenv("QUIZ_API_KEY")
    url = "https://quizapi.io/api/v1/questions"
    headers = {"X-Api-Key": apiKey}
    
    quiz_data = requests.get(url, headers=headers)
    quiz_json = json.loads(quiz_data.text)

    max_questions = 10
    selected_questions = []

    # Process the first 10 questions
    for question_data in quiz_json:
        if len(selected_questions) >= max_questions:
            break
        
        # Parse question data into a QuizQuestion object
        question = QuizQuestion(question_data)
        selected_questions.append(question)

    # Create a ButtonView with the selected questions
    view = ButtonView(selected_questions)
    await view.show_next_question(interaction)

# Run the bot
bot.run(os.getenv("bot_token"))
