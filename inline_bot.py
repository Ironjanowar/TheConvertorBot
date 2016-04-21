import telebot
import os.path as path
from telebot import types
import sys

# Check if there is any token file
if not path.isfile('./convertor.token'):
    print("ERROR: Can't find token as \"convertor.token\"\nCreate the file with a Telegram bot token.")
    sys.exit()

# Create bot with its token
with open('./convertor.token', 'r') as TOKEN:
    bot = telebot.TeleBot(TOKEN.readline().strip())


# Functions
def toBin(num):
    if type(num) == int:
        return bin(num)
    else:
        return None


def isNumber(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


def toHex(num):
    if type(num) == int:
        return hex(num)
    else:
        return None


# Inline handler


@bot.inline_handler(lambda query: isNumber(query.query))
def query_fromDec(inline_query):
    try:
        number = inline_query.query
        binNum = toBin(int(number))
        hexNum = toHex(int(number))
        binSend = str(number) + " -> " + str(binNum)
        hexSend = str(number) + " -> " + str(hexNum)
        rBin = types.InlineQueryResultArticle('1', 'To Binary', types.InputTextMessageContent(binSend))
        rHex = types.InlineQueryResultArticle('2', 'To Hexadecimal', types.InputTextMessageContent(hexSend))
        bot.answer_inline_query(inline_query.id, [rBin, rHex])
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: query.query.startswith('0x') and len(query.query.split('x')) == 2)
def query_fromHex(iq):
    number = iq.query
    decNum = int(number, 16)
    toSend = str(number) + " -> " + str(decNum)
    r = types.InlineQueryResultArticle('1', 'To Decimal', types.InputTextMessageContent(toSend))
    bot.answer_inline_query(iq.id, [r])


@bot.inline_handler(lambda query: query.query.startswith('0b') and len(query.query.split('b')) == 2)
def query_fromBin(iq):
    number = iq.query
    decNum = int(number, 2)
    toSend = str(number) + " -> " + str(decNum)
    r = types.InlineQueryResultArticle('1', 'To Decimal', types.InputTextMessageContent(toSend))
    bot.answer_inline_query(iq.id, [r])

# I'm ready!
print("Running..")

# Ignore old messages
bot.skip_pending = True

# Start the bot
bot.polling()
