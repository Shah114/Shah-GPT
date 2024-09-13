# Importing Modules
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext
from easygoogletranslate import EasyGoogleTranslate
import google.generativeai as gen_ai
import config

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Configure Google Gemini-Pro AI model
gen_ai.configure(api_key=config.api_key)
model = gen_ai.GenerativeModel('gemini-pro')

# Translator instance
translator = EasyGoogleTranslate()

# Conversation state
WAITING_FOR_RESPONSE = 1

# Function to initialize chat session
def start_chat_session():
    return model.start_chat(history=[])

# Async function to handle the /start command
async def start(update: Update, context: CallbackContext) -> None:
    context.user_data["language"] = "en"
    await update.message.reply_text(
        "Hi! I'm Shah GPT. You can ask me anything. Type /aze to switch to Azerbaijani, /eng to switch back to English. Type /cancel to stop the conversation.")

# Async function to handle the /cancel command
async def cancel(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Conversation canceled. Type /start to begin again.")
    return ConversationHandler.END

# Async function to switch to Azerbaijani
async def switch_to_aze(update: Update, context: CallbackContext) -> None:
    context.user_data["language"] = "az"
    await update.message.reply_text("Switched to Azerbaijani. You can now send messages in Azerbaijani.")

# Async function to switch to English
async def switch_to_eng(update: Update, context: CallbackContext) -> None:
    context.user_data["language"] = "en"
    await update.message.reply_text("Switched to English. You can now send messages in English.")

# Async function to handle translation
async def translate_message(text: str, src_lang: str, target_lang: str) -> str:
    if src_lang == target_lang:
        return text
    
    try:
        # Translate text from src_lang to target_lang
        if src_lang == "az":
            translation = translator.translate(text, "en")  # Translating Azerbaijani to English
        elif src_lang == "en" and target_lang == "az":
            translation = translator.translate(text, "az")  # Translating English to Azerbaijani
        else:
            return text
        return translation
    except Exception as e:
        logging.error(f"Translation error: {e}")
        return text

# Async function to handle user messages
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    user_language = context.user_data.get("language", "en")  # Default to English if not set

    # Translate user input to English if necessary
    if user_language == "az":
        translated_input = await translate_message(user_input, "az", "en")
    else:
        translated_input = user_input

    # Send the (possibly translated) text to Gemini-Pro model
    chat_session = start_chat_session()
    gemini_response = chat_session.send_message(translated_input)

    # Translate response to user's language if necessary
    if user_language == "az":
        translated_response = await translate_message(gemini_response.text, "en", "az")
    else:
        translated_response = gemini_response.text

    await update.message.reply_text(translated_response)

    return WAITING_FOR_RESPONSE

# Command to handle errors
async def error(update: Update, context: CallbackContext) -> None:
    logging.error(f'Update {update} caused error {context.error}')

# Main function to run the bot
if __name__ == '__main__':
    # Create the Application instance
    application = ApplicationBuilder().token(config.bot_token).build()

    # Define ConversationHandler for cancelable conversations
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        states={
            WAITING_FOR_RESPONSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cancel", cancel))
    application.add_handler(CommandHandler("aze", switch_to_aze))
    application.add_handler(CommandHandler("eng", switch_to_eng))
    application.add_handler(conv_handler)
    application.add_error_handler(error)

    # Start the bot and run it
    print("Starting Bot...")
    application.run_polling()