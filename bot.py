import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import nmap

# Initialize nmap scanner
nm = nmap.PortScanner()

# Telegram bot token
TOKEN = '7746177940:AAEHTsKoPxma8Sm3ow4HAQ5OzwMIb1ZRcP4'

# Start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send me an IP or hostname to scan.\n\nMade by Darkboy\n========@Darkboy336")

# Scan function
def scan(target, port_range):
    result = nm.scan(target, port_range)
    open_ports = []

    for host in result['scan']:
        for proto in result['scan'][host].all_protocols():
            lport = result['scan'][host][proto].keys()
            for port in lport:
                if result['scan'][host][proto][port]['state'] == 'open':
                    open_ports.append(port)
    
    return open_ports

# Function to handle user input
def handle_message(update: Update, context: CallbackContext) -> None:
    target = update.message.text
    keyboard = [
        [InlineKeyboardButton("Common ports", callback_data=f"{target}:common")],
        [InlineKeyboardButton("All ports", callback_data=f"{target}:all")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an option:', reply_markup=reply_markup)

# Callback query handler
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    target, scan_type = query.data.split(':')

    if scan_type == 'common':
        open_ports = scan(target, '21,22,23,25,53,80,110,139,143,443,445,3389')
    else:
        open_ports = scan(target, '1-65535')

    if open_ports:
        response = f"Open ports for {target}:\n" + ", ".join(map(str, open_ports))
    else:
        response = f"No open ports found for {target}."

    query.edit_message_text(text=response + "\n\nMade by Darkboy\n========@Darkboy336")

# Main function
def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
