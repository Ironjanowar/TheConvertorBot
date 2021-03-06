import telebot
import os.path as path
import sys

# Check if there is any token file
if not path.isfile('./convertor.token'):
    print("ERROR: Can't find token as \"convertor.token\"\nCreate the file with a Telegram bot token.")
    sys.exit()

# Create bot with its token
with open('./convertor.token', 'r') as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())

# Variables
commands = {
    'start': 'Starts the bot!',
    'help': 'Show commands abailables',
    'todec': 'Takes an hexadecimal or binary number and returns its decimal equivalent',
    'tohex': 'Takes a decimal number and returns its hexadecimal equivalent',
    'tobin': 'Takes a decimal number and returns its binary equivalent'
}

# Functions


def listener(messages):
    # When new messages arrive TeleBot will call this function.
    for m in messages:
        if m.content_type == 'text':
            # Prints the sent message to the console
            if m.chat.type == 'private':
                print("Chat -> " + str(m.chat.first_name) +
                      "(@" + m.from_user.username + ")" + " [" + str(m.chat.id) + "]: " + m.text)
        else:
            print("Group -> " + str(m.chat.title) +
                  " [" + str(m.chat.id) + "]: " + m.text)

# Handlers


@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Hi!\nThis is a simple bot for rebasing a number\n\nSource code here: https://github.com/Ironjanowar/TheConvertorBot")


@bot.message_handler(commands=['help'])
def help(m):
    helpMessage = "Commands:\n\n"
    for key in commands:
        helpMessage += "- /" + key + " ::\n  "
        helpMessage += commands[key] + "\n"
    bot.send_message(m.chat.id, helpMessage)


@bot.message_handler(commands=['tohex'])
def tohex(m):
    if len(m.text.split(' ')) == 1:
        bot.send_message(m.chat.id,
                         "Try:\n /tohex [number]\n\nExample:\n /tohex 10")
    else:
        try:
            if '.' in m.text.split()[1]:
                bot.reply_to(m, "Ups!\nThat's not a decimal number.")
            else:
                number = int(m.text.split()[1])
                hexNumber = hex(number)
                bot.reply_to(m, hexNumber)
        except ValueError:
            bot.reply_to(m, "Ups!\nThat's not a decimal number.")


@bot.message_handler(commands=['todec'])
def todec(m):
    if len(m.text.split(' ')) == 1:
        bot.send_message(m.chat.id,
                         "Try:\n /todec [number]\n\nExample:\n /todec 0xa")
    else:
        number = m.text.split()[1]
        if number.startswith('0x'):
            try:
                num = int(number, 16)
                bot.reply_to(m, str(num))
            except ValueError:
                bot.reply_to(m, "Ups!\nThat's not a hexadecimal number.")
        elif number.startswith('0b'):
            try:
                num = int(number, 2)
                bot.reply_to(m, str(num))
            except ValueError:
                bot.reply_to(m, "Ups!\nThat's not a binary number.")
        else:
            bot.reply_to(m,
                         "Ups\nThat's neither a binary or hexadecimal number")


@bot.message_handler(commands=['tobin'])
def tobin(m):
    if len(m.text.split(' ')) == 1:
        bot.send_message(m.chat.id,
                         "Try:\n /tobin [number]\n\nExample:\n /tobin 10")
    else:
        try:
            if '.' in m.text.split()[1]:
                bot.reply_to(m, "Ups!\nThat's not a decimal number.")
            else:
                number = int(m.text.split()[1])
                binNumber = bin(number)
                bot.reply_to(m, binNumber)
        except ValueError:
            bot.reply_to(m, "Ups!\nThat's not a decimal number.")

# Ignore older messages
bot.skip_pending = True

# Initializing listener
bot.set_update_listener(listener)

# Starting the bot
print("Running..")
bot.polling()
