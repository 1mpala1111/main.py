import python
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Вопросы викторины
questions = [
    {
        "question": "Какой элемент периодической таблицы обозначается символом 'O'?",
        "options": ["A) Золото", "B) Водород", "C) Кислород", "D) Углерод"],
        "answer": "C"
    },
    {
        "question": "Кто написал роман '1984'?",
        "options": ["A) Олдос Хаксли", "B) Джордж Оруэлл", "C) Фрэнсис Скотт Фицджеральд", "D) Эрнест Хемингуэй"],
        "answer": "B"
    },
    {
        "question": "Какой океан является самым большим на Земле?",
        "options": ["A) Атлантический океан", "B) Индийский океан", "C) Северный Ледовитый океан", "D) Тихий океан"],
        "answer": "D"
    }
]

user_scores = {}

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Нажмите /quiz, чтобы начать викторину.")

def quiz(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_scores[user_id] = {"score": 0, "question_index": 0}
    
    send_question(update, user_id)

def send_question(update: Update, user_id: int) -> None:
    index = user_scores[user_id]["question_index"]
    
    if index < len(questions):
        question = questions[index]
        options = question["options"]
        
        keyboard = [[InlineKeyboardButton(option, callback_data=option[0]) for option in options]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.message.reply_text(question["question"], reply_markup=reply_markup)
    else:
        score = user_scores[user_id]["score"]
        update.message.reply_text(f"Викторина окончена! Ваш результат: {score} из {len(questions)}.")
        del user_scores[user_id]

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    user_id = query.from_user.id
    index = user_scores[user_id]["question_index"]
    
    if query.data == questions[index]["answer"]:
        user_scores[user_id]["score"] += 1
    
    user_scores[user_id]["question_index"] += 1
    send_question(query, user_id)

def main() -> None:
    updater = Updater("8033851799:AAEX2TFSbH0vHD4IwfBde23n8Ownp5MzGGg")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("quiz", quiz))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
