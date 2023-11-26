import random
import telebot
import random
import pickle


rating_dict = {} # ratind_dict(user) = how many problems have solved
rates = [] # how peole rate my bot
last_messages = dict() # dict of last messages of bot to users

def load_data():
    try:
        rating_dict = pickle.load(open('rating_dict.pickle', 'rb'))
        rates = pickle.load(open('rates.pickle', 'rb'))
        last_messages = pickle.load(open('last_messages.pickle', 'rb'))
    except Exception:
        rating_dict = dict()
        rates = []
        last_messages = dict()

load_data() #TODO

key = "6503445568:AAG6bIW_bRMvjHl4WEvWXaOA-euG12RZ60Y" # telebram-bot api-key

bot = telebot.TeleBot(key)


def create_quadratic_problem():
    '''
    return list of coefficents and answer
    '''
    candidate_1 = random.randint(-15, 15)
    candidate_2 = random.randint(-15, 15)
    candidate_3 = random.randint(-15, -1)
    candidate_4 = random.randint(1, 15)
    if candidate_1 != 0:
        x1 = candidate_1
    else:
        x1 = candidate_3

    if candidate_2 != 0:
        x2 = candidate_2
    else:
        x2 = candidate_4

    c = x1 * x2
    b = x1 + x2
    a = random.choice([1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 4, 5])
    tmp = max(x1, x2)
    tmp_2 = min(x1, x2)
    return [a, -b * a, c * a, tmp, tmp_2]


def create_plus_problem():
    '''
    return list of conditions and answer: +
    '''
    x1 = random.randint(10, 200)
    x2 = random.randint(10, 200)
    ans = x1 + x2
    return [x1, x2, ans]


def create_minus_problem():
    '''
    return list of conditions and answer: -
    '''
    x1 = random.randint(10, 200)
    x2 = random.randint(10, 200)
    ans = x1 - x2
    return [x1, x2, ans]


def create_multi_problem():
    '''
    return list of conditions and answer: *
    '''
    x1 = random.randint(5, 20)
    x2 = random.randint(5, 20)
    ans = x1 * x2
    return [x1, x2, ans]

# Handle the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the High Arithmetic Bot! Type /problem to get a math problem.")
    rating_dict[message.from_user.id] = 0

# Handle the /problem command
@bot.message_handler(commands=['problem'])
def send_problem(message):
    problem_type = random.choice(['quadratic', 'plus', 'minus', 'multi'])
    if problem_type == 'quadratic':
        problem = create_quadratic_problem()
        last_messages[message.from_user.id] = [problem[3], problem[4]]
        bot.reply_to(message, f"Solve the quadratic equation: {problem[0]}x^2 + {problem[1]}x + {problem[2]} = 0")
        bot.send_message(message.from_user.id, 'В ответе укажите корни в порядке неубывания.')

    elif problem_type == 'plus':
        problem = create_plus_problem()
        last_messages[message.from_user.id] = [problem[2]]
        bot.reply_to(message, f"What is the sum of {problem[0]} and {problem[1]}?")

    elif problem_type == 'minus':
        problem = create_minus_problem()
        last_messages[message.from_user.id] = [problem[2]]
        bot.reply_to(message, f"What is the difference between {problem[0]} and {problem[1]}?")

    elif problem_type == 'multi':
        problem = create_multi_problem()
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