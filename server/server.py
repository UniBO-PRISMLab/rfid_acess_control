import threading
import logging
from flask import Flask, request
import telebot
import configuration

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s - %(message)s')

bot = telebot.TeleBot(configuration.TELEGRAM_API_KEY)
api = Flask(__name__)

pending_job = None
timer = None

@bot.message_handler(commands=['newkey'])
def key_handler(message):
    global pending_job, timer

    if pending_job is not None:
        bot.send_message(message.chat.id, "A key registration is already pending. Please wait.")
        logging.warning("New key request received while another job is pending.")
        return

    try:
        pending_job = message.chat.id
        text = "Please pass the card in the reader within 30 seconds."
        bot.send_message(pending_job, text, parse_mode='Markdown')

        timer = threading.Timer(30.0, landing)
        timer.start()
        logging.info(f"Started a 30-second timer for chat ID {pending_job}.")
    except Exception as e:
        logging.error(f"Error in key_handler: {e}")

def landing():
    global pending_job

    if pending_job is not None:
        try:
            bot.send_message(pending_job, "Time expired! Please try again.")
            logging.info(f"Timer expired for chat ID {pending_job}.")
        except Exception as e:
            logging.error(f"Error sending timeout message: {e}")
        finally:
            pending_job = None

@api.route('/iskeyvalid', methods=['GET'])
def get_iskeyvalid():
    global pending_job, timer

    try:
        key_id = request.args.get('id')
        logging.info(f"Received key validation request: {key_id}")

        if pending_job is not None:
            configuration.known_keys.append(key_id)
            bot.send_message(pending_job, f"Key `{key_id}` was added!", parse_mode='Markdown')
            logging.info(f"Added new key {key_id} for chat ID {pending_job}.")

            pending_job = None
            if timer:
                timer.cancel()

            return 'a'  # Key added

        if key_id in configuration.known_keys:
            return 'g'  # Key is known
        else:
            return 'r'  # Key is unknown

    except Exception as e:
        logging.error(f"Error in /iskeyvalid endpoint: {e}")
        return 'e', 500

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    try:
        bot.reply_to(message,
            """
            Welcome to the RFID Sample Bot!
            Here's what I can do:
            /newkey => adds a new key to the volatile database
            Developed by *stradivarius*
            """, parse_mode='Markdown'
        )
    except Exception as e:
        logging.error(f"Error replying to message: {e}")

def run_bot():
    try:
        bot.infinity_polling()
    except Exception as e:
        logging.critical(f"Bot polling crashed: {e}")

def run_flask():
    try:
        api.run(host="0.0.0.0", port=5000)
    except Exception as e:
        logging.critical(f"Flask server crashed: {e}")

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Event().wait()
