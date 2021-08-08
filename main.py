import telebot
import time
import os

def get_price_per_g(quantity_per_package, price_per_package):
    quantity_per_package = float(quantity_per_package)
    price_per_package = float(price_per_package)
    price_per_hundred = ( 100 * price_per_package ) / quantity_per_package
    return price_per_hundred

def get_price_per_hundred_protein(protein_per_hundred_package, price_per_hundred_package):
    protein_per_hundred_package = float(protein_per_hundred_package)
    price_per_hundred_package = float(price_per_hundred_package)
    price_per_hundred_protein = ( price_per_hundred_package * 100 ) / protein_per_hundred_package
    return price_per_hundred_protein

bot_token = os.environ.get('BotToken')
bot = telebot.TeleBot(bot_token)



if __name__ == "__main__":
    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.reply_to(message, 'Food Protein Calculator - To use this bot, send it a /start command')

    @bot.message_handler(commands=['start'])
    def start(message):
        try:
            msg = bot.reply_to(message, 'Please enter product name:')
            bot.register_next_step_handler(msg, name_step)
        except Exception as e:
            bot.reply_to(message, e)

    def name_step(message):
        try:
            global name
            name = message.text
            msg = bot.reply_to(message, 'Please enter the total package quantity in grams:')
            bot.register_next_step_handler(msg, process_price_step)
        except Exception as e:
            bot.reply_to(message, e)

    def process_price_step(message):
        try:
            global quantity_per_package
            quantity_per_package = message.text
            try:
                n = float(quantity_per_package)
            except Exception as e:
                msg = bot.reply_to(message, 'Quantity should be a number! Type again:')
                bot.register_next_step_handler(msg, process_price_step)
                return
            msg = bot.reply_to(message, 'Now please enter the price for the total package:')
            bot.register_next_step_handler(msg, process_protein_step)
        except Exception as e:
            bot.reply_to(message, e)
    
    def process_protein_step(message):
        try:
            global price_per_package
            price_per_package = message.text
            try:
                n = float(price_per_package)
            except Exception as e:
                msg = bot.reply_to(message, 'Price should be a number! Type again:')
                bot.register_next_step_handler(msg, process_protein_step)
                return
            global price_per_hundred_package
            price_per_hundred_package = get_price_per_g(quantity_per_package = quantity_per_package, price_per_package = price_per_package)
            msg = ( "The price per 100 grams is: £{:0.2f}".format(price_per_hundred_package) )
            bot.reply_to(message, msg)
            msg = bot.reply_to(message, "Now enter the amout of protein per 100g of the product:")
            bot.register_next_step_handler(msg, process_calc_step)
        except Exception as e:
            bot.reply_to(message, e)

    def process_calc_step(message):
        try:
            protein_per_hundred_grams = message.text
            try:
                n = float(protein_per_hundred_grams)
            except Exception as e:    
                msg = bot.reply_to(message, 'Amount of protein should be a number! Type again:')
                bot.register_next_step_handler(msg, process_calc_step)
                return
            price_per_hundred_protein = get_price_per_hundred_protein(price_per_hundred_package = price_per_hundred_package, protein_per_hundred_package = protein_per_hundred_grams)
            msg = ('The price per 100 grams of {} protein is: £{:0.2f}'.format(name, price_per_hundred_protein))
            bot.reply_to(message, msg)
        except Exception as e:
            bot.reply_to(message, e)

    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    while True:
        try:
            print("Connecting")
            bot.polling()
        except Exception:
            time.sleep(15)

