import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ТОКЕН ТВОЕГО БОТА (уже вставлен)
BOT_TOKEN = "8489055225:AAHfRkvxr3jIBKdQ0JIU0aqaMhqa6MQiP0Y"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    
    # Создаём кнопки
    keyboard = [
        [InlineKeyboardButton("💰 Создать ордер", callback_data='create_order')],
        [InlineKeyboardButton("📋 Активные ордера", callback_data='active_orders')],
        [InlineKeyboardButton("👤 Мой профиль", callback_data='my_profile')],
        [InlineKeyboardButton("ℹ️ Помощь", callback_data='help_info')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Отправляем сообщение с кнопками
    await update.message.reply_text(
        f"🎉 Привет, {user.first_name}!\n\n"
        "Я — P2P-бот для обмена USDT/RUB\n\n"
        "✅ Создавай ордера\n"
        "✅ Находи контрагентов\n"
        "✅ Обменивай безопасно\n\n"
        "Выбери действие:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий кнопок"""
    query = update.callback_query
    await query.answer()  # Ответим на запрос
    
    if query.data == 'create_order':
        # Показываем выбор типа ордера
        keyboard = [
            [InlineKeyboardButton("💵 КУПИТЬ USDT", callback_data='buy_usdt')],
            [InlineKeyboardButton("💸 ПРОДАТЬ USDT", callback_data='sell_usdt')],
            [InlineKeyboardButton("🔙 Назад", callback_data='back_main')]
        ]
        await query.edit_message_text(
            "Выбери тип ордера:\n\n"
            "💵 **Купить USDT** — ты получаешь USDT, отдаёшь RUB\n"
            "💸 **Продать USDT** — ты отдаёшь USDT, получаешь RUB",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )
    
    elif query.data == 'active_orders':
        await query.edit_message_text(
            "📋 **Активные ордера:**\n\n"
            "1. 💵 Купить 1000 USDT за 90₽/шт\n"
            "2. 💸 Продать 500 USDT за 92₽/шт\n"
            "3. 💵 Купить 2000 USDT за 89₽/шт\n\n"
            "Чтобы подключиться — напиши номер ордера",
            parse_mode='Markdown'
        )
    
    elif query.data == 'my_profile':
        await query.edit_message_text(
            "👤 **Твой профиль:**\n\n"
            "📍 Москва\n"
            "⭐ Рейтинг: 5.0\n"
            "💼 Сделок: 0\n"
            "💰 Баланс: 0 USDT\n\n"
            "🚀 Начинай первую сделку!",
            parse_mode='Markdown'
        )
    
    elif query.data == 'help_info':
        await query.edit_message_text(
            "ℹ️ **Помощь по боту:**\n\n"
            "1. **Создать ордер** — размести заявку на покупку/продажу\n"
            "2. **Активные ордера** — просмотр всех доступных сделок\n"
            "3. **Мой профиль** — твоя статистика и баланс\n\n"
            "📞 Поддержка: @support\n"
            "💎 Безопасность: все сделки защищены",
            parse_mode='Markdown'
        )
    
    elif query.data == 'back_main':
        # Возврат в главное меню
        await start(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /help"""
    await update.message.reply_text(
        "📚 **Доступные команды:**\n\n"
        "/start — запуск бота\n"
        "/help — эта справка\n\n"
        "Используй кнопки для навигации!",
        parse_mode='Markdown'
    )

def main():
    """Запуск бота"""
    # Создаём приложение
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Запускаем
    print("=" * 50)
    print("🤖 P2P БОТ ЗАПУЩЕН!")
    print(f"📍 Токен: {BOT_TOKEN[:15]}...")
    print("📍 Напиши /start в Telegram")
    print("=" * 50)
    
    # Запускаем polling (для Railway)
    application.run_polling()

if __name__ == "__main__":
    main()
