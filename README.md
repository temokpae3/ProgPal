# ProgPal

ProgPal is a Discord bot that allows you to conduct quizzes within Discord channels or private direct messages using interactive buttons for answering questions sourced from the QuizAPI service. 
Players can participate in quizzes based on specific categories and difficulties, or opt for random questions.

## Features
- **Interactive Quiz Interface:** Users can participate in quizzes by selecting answers through Discord's button interactions.
- **API Integration:** Fetches quiz questions dynamically from an external API (https://quizapi.io).
- **Customizable Categories and Difficulties:** Quizzes can be tailored based on specific categories (e.g., programming, history) and difficulty levels.
- **Score Tracking:** The bot tracks users' scores based on correct and incorrect answers.
- **Documentation**: Explore the comprehensive documentation on the [ProgPal Wiki](http://wiki.progpal.site/en/home) for detailed bot functionalities.

## Requirements:
- Python 3.6+
- discord.py library (`pip install discord.py`)
- requests library (`pip install requests`)
- python-dotenv library (`pip install python-dotenv`)

## Usage
### Commands:
- **`/regular <category> <difficulty>:`** Start a quiz with questions from a specific category and difficulty level.
Example: /regular Linux easy

- **`/random:`** Start a random quiz with questions from various categories and difficulties.

## Getting Started
1. **Invite ProgPal to Your Server**: Click the "Invite to Server" button on the [ProgPal Website](https://www.cs.oswego.edu/~temokpae/coursework/ProgPal/).

2. **Usage**:
   - Use slash commands `/regular <category> <difficulty>` or `/random` to initiate quizzes and the bot will present questions one by one.
   - Users can click on the buttons corresponding to their chosen answers.
   - The bot will provide instant feedback on whether the answer was correct or incorrect.

3. **Direct Messaging**: ProgPal can also be used directly in Discord's Direct Messaging feature for private quizzes.

---

&copy; 2024 ProgPal
