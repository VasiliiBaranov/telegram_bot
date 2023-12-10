import random
import os
import telebot
import random
import pickle
from dotenv import load_dotenv

import generate_task


rating_dict = dict() # ratind_dict(user) = how many problems have solved
rates = [] # how peole rate my bot
last_messages = dict() # dict of last messages of bot to users


def load_data():
    global rating_dict, rates, last_messages
    try:
        rating_dict = pickle.load(open('rating_dict.pickle', 'rb'))
        rates = pickle.load(open('rates.pickle', 'rb'))
        last_messages = pickle.load(open('last_messages.pickle', 'rb'))
        print('aboba')
    except Exception:
        rating_dict = dict()
        rates = []
        last_messages = dict()

def open_data():
    load_data()
    load_dotenv(".env")
    key = str(os.getenv("key")) # telebram-bot api-key
    bot = telebot.TeleBot(key)

open_data()
# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the High Arithmetic Bot! Type /problem to get a math problem.")
    if (message.from_user.id not in rating_dict.keys()):
        rating_dict[message.from_user.id] = 0

# Handle the /problem command
@bot.message_handler(commands=['problem'])
def send_problem(message):
    problem_type = random.choice(['quadratic', 'plus', 'minus', 'multi'])
    if problem_type == 'quadratic':
        problem = generate_task.create_quadratic_problem()
        last_messages[message.from_user.id] = [problem[3], problem[4]]
        bot.reply_to(message, f"Solve the quadratic equation: {problem[0]}x^2 + {problem[1]}x + {problem[2]} = 0")
        bot.send_message(message.from_user.id, 'В ответе укажите корни в порядке неубывания.')

    elif problem_type == 'plus':
        problem = generate_task.create_plus_problem()
        last_messages[message.from_user.id] = [problem[2]]
        bot.reply_to(message, f"What is the sum of {problem[0]} and {problem[1]}?")

    elif problem_type == 'minus':
        problem = generate_task.create_minus_problem()
        last_messages[message.from_user.id] = [problem[2]]
        bot.reply_to(message, f"What is the difference between {problem[0]} and {problem[1]}?")

    elif problem_type == 'multi':
        problem = generate_task.create_multi_problem()
        last_messages[message.from_user.id] = [problem[2]]
        bot.reply_to(message, f"What is the product of {problem[0]} and {problem[1]}?")


# Handle /help command
@bot.message_handler(commands=['help'])
def send_help(message):
    text = '''
    Type /start to start bot.
    This bot will give you a math problem to solve it. Type /problem to get it.
    Type /answer to get the answer to the problem.
    Type /statistic to get your statistics.
    Type /rating to get the rating of the bot.
    Type /rate to rate the bot.
    Else type answer to the problem.
    '''
    bot.reply_to(message, text)


# Handle /statistic command
@bot.message_handler(commands=['statistic'])
def get_statistic(message):
    print('statistic')
    try:
        bot.reply_to(message, str(f'Congratulations!!! You have solved {rating_dict[message.from_user.id]} problems!!!'))
    except Exception:
        bot.reply_to(message, 'You should start the bot first, type /start')
    

# Handle /rating command
@bot.message_handler(commands=['rating'])
def get_rating(message):
    print('rating')
    progresses = []
    for i in rating_dict.keys():
        progresses.append(rating_dict[i])
    progresses.sort(reverse= True)
    try:
        number_of_problems = rating_dict[message.from_user.id]
        for i in range(len(rating_dict)):
            if progresses[i] == number_of_problems:
                bot.reply_to(message, str(f'Your rating is {i + 1}'))
                return 0
    except Exception:
        bot.reply_to(message, 'You should start the bot first, type /start')


# Handle /rate problem
@bot.message_handler(commands=['rate'])
def rate_bot(message):
    print('rate')
    try:
        rates.append(message.text.split()[1])
        bot.reply_to(message, 'Thank you for your rate!!!')
        print(rates[-1])
    except Exception:
        bot.reply_to(message, 'You should write your rate after /rate command')
    return 0


# Handle user answers
@bot.message_handler(func=lambda message: True)
def check_answer(message):
    print("aboba")
    try:
        last_message = last_messages[message.from_user.id]
        if last_message == -100000:
            bot.reply_to(message, 'You are very clever, that\'s good, type /problem')
            return 0
        answer = message.text.split()
        print(answer)
        print(last_message)
        if len(answer) == len(last_message) and all(str(i).isdigit() for i in answer):
            for i in range(len(answer)):
                if float(answer[i]) != float(last_message[i]):
                    bot.reply_to(message, 'Wrong answer!!!')
                    return 0
            bot.reply_to(message, 'Congratulations!!!')
            bot.send_message(message.from_user.id, 'Type /problem to get another one problem.')
            rating_dict[message.from_user.id] += 1
            last_messages[message.from_user.id] = -100000
            return 0
        else:
            bot.reply_to(message, 'You have subtimmed some cringe!!!')
            return 0
    except Exception:
        bot.reply_to(message, 'You should request at least 1 problem to the bot first, type /start, then /problem')
        return 0

        
# Start the bot
bot.polling(none_stop=True, interval=0)


#save data:
with open('rating_dict.pickle', 'wb') as f:
    pickle.dump(rating_dict, f)

with open('rates.pickle', 'wb') as f:
    pickle.dump(rates, f)

with open('last_messages.pickle', 'wb') as f:
    pickle.dump(last_messages, f)