import telebot
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from flowers_store.apps.bot.models import Event, Bouquet, Order, Memory
from telebot import types


bot = telebot.TeleBot(settings.BOT_TOKEN)


def get_bouquets(price):
    click = Memory.objects.all().first()

    bouquets = Bouquet.objects.filter(price__lte=price, events__title=click.click_event)

    Memory.objects.all().delete()
    return bouquets



@bot.message_handler(commands=['start'])
def hear_menu(message):
    inline_markup = types.InlineKeyboardMarkup()
    inline_markup.add(types.InlineKeyboardButton(text='День рождения', callback_data='prefix:День рождения'))
    inline_markup.add(types.InlineKeyboardButton(text='Свадьба', callback_data='prefix:Свадьба'))
    inline_markup.add(types.InlineKeyboardButton(text='В школу', callback_data='prefix:В школу'))
    inline_markup.add(types.InlineKeyboardButton(text='Без повода', callback_data='prefix:Без повода'))
    bot.send_message(message.chat.id, f'Привет!\nК какому событию готовимся? Выберите один из вариантов,',
                     reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.split(":")[1] in ['День рождения', 'Свадьба', 'В школу', 'Без повода'])
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)
    inline_markup = types.InlineKeyboardMarkup()
    data_ = call.data.split(":")[1]
    Memory.objects.create(click_event=data_)
    inline_markup.add(types.InlineKeyboardButton(text='500', callback_data="prefix2:500"))
    inline_markup.add(types.InlineKeyboardButton(text='1000', callback_data="prefix2:1000"))
    inline_markup.add(types.InlineKeyboardButton(text='2000', callback_data="prefix2:2000"))
    inline_markup.add(types.InlineKeyboardButton(text='больше', callback_data="prefix2:больше"))
    inline_markup.add(types.InlineKeyboardButton(text='не важно', callback_data="prefix2:не важно"))
    inline_markup.add(types.InlineKeyboardButton(text='👈 назад 👈', callback_data="prefix2:назад"))
    bot.edit_message_text('На какую сумму рассчитываете?', call.message.chat.id, call.message.message_id,
                                  reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "prefix2")
def querry_handler2(call):
    data_ = call.data.split(":")[1]
    if data_ == "500":
        bouquets = get_bouquets(data_)
        for bouquet in bouquets:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Заказать букет', callback_data=f'prefix3:{bouquet.id}'))
            keyboard.add(types.InlineKeyboardButton(text='Заказать консультацию', callback_data="prefix3:Заказать консультацию"))
            keyboard.add(types.InlineKeyboardButton(text='Посмотреть всю коллекцию', callback_data="prefix3:Посмотреть всю коллекцию"))
            bot.send_photo(call.message.chat.id, bouquet.photo, bouquet.description, reply_markup=keyboard)

    elif data_ == "1000":
        bouquets = get_bouquets(data_)
        for bouquet in bouquets:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Заказать букет', callback_data=f'prefix3:{bouquet.id}'))
            keyboard.add(types.InlineKeyboardButton(text='Заказать консультацию', callback_data="prefix3:Заказать консультацию"))
            keyboard.add(types.InlineKeyboardButton(text='Посмотреть всю коллекцию', callback_data="prefix3:Посмотреть всю коллекцию"))
            bot.send_photo(call.message.chat.id, bouquet.photo, bouquet.description, reply_markup=keyboard)

    elif data_ == "2000":
        bouquets = get_bouquets(data_)
        for bouquet in bouquets:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Заказать букет', callback_data=f'prefix3:{bouquet.id}'))
            keyboard.add(types.InlineKeyboardButton(text='Заказать консультацию', callback_data="prefix3:Заказать консультацию"))
            keyboard.add(types.InlineKeyboardButton(text='Посмотреть всю коллекцию', callback_data="prefix3:Посмотреть всю коллекцию"))
            bot.send_photo(call.message.chat.id, bouquet.photo, bouquet.description, reply_markup=keyboard)

    elif data_ == "больше":
        click = Memory.objects.all().first()
        bouquets = Bouquet.objects.filter(price__gt='2000', events__title=click.click_event)
        for bouquet in bouquets:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Заказать букет', callback_data=f'prefix3:{bouquet.id}'))
            keyboard.add(types.InlineKeyboardButton(text='Заказать консультацию', callback_data="prefix3:Заказать консультацию"))
            keyboard.add(types.InlineKeyboardButton(text='Посмотреть всю коллекцию', callback_data="prefix3:Посмотреть всю коллекцию"))
            bot.send_photo(call.message.chat.id, bouquet.photo, bouquet.description, reply_markup=keyboard)

    elif data_ == "не важно":
        bouquets = Bouquet.objects.all()
        for bouquet in bouquets:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(text='Заказать букет', callback_data=f'prefix3:{bouquet.id}'))
            keyboard.add(types.InlineKeyboardButton(text='Заказать консультацию', callback_data="prefix3:Заказать консультацию"))
            bot.send_photo(call.message.chat.id, bouquet.photo, bouquet.description, reply_markup=keyboard)


    elif data_ == "назад":
        inline_markup = types.InlineKeyboardMarkup()
        inline_markup.add(types.InlineKeyboardButton(text='День рождения', callback_data='prefix:День рождения'))
        inline_markup.add(types.InlineKeyboardButton(text='Свадьба', callback_data='prefix:Свадьба'))
        inline_markup.add(types.InlineKeyboardButton(text='В школу', callback_data='prefix:В школу'))
        inline_markup.add(types.InlineKeyboardButton(text='Без повода', callback_data='prefix:Без повода'))
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=inline_markup)


@bot.callback_query_handler(func=lambda call: call.data.split(":")[0] == "prefix3")
def querry_handler3(call):
    data_ = call.data.split(":")[1]
    if data_.isdigit():
        bouquet = Bouquet.objects.get(id=int(data_))
        bouquet_order = Order.objects.create(bouquet=bouquet)
        bouquet_order.save()
        bot.send_message(call.message.chat.id, f'Введите ваше имя')


@bot.message_handler(content_types=['text'])
def callback_order(message):
    if message:
        bot.register_next_step_handler(message, save_username)


def get_consulting(message):
    chat_id = 1180965200
    bot.send_message(chat_id, f'номер клиента: {message.text}')


def save_username(message):
    order = Order.objects.last()
    order.client_name = message.text
    order.save()
    name = message.text
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     f'Отлично, {name}. Теперь укажите свой адрес')
    bot.register_next_step_handler(message, save_address)


def save_address(message):
    order = Order.objects.last()
    order.address = message.text
    order.save()
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     f'Отлично, Теперь укажите дату доставки')
    bot.register_next_step_handler(message, save_date)


def save_date(message):
    order = Order.objects.last()
    order.date = message.text
    chat_id = message.chat.id
    order.save()
    bot.send_message(chat_id,
                     f'Отлично, теперь укажите время доставки')
    bot.register_next_step_handler(message, save_time_send_deliver)


def save_time_send_deliver(message):
    order = Order.objects.last()
    order.time = message.text
    order.save()
    bot.send_message(message.chat.id,
                     f'Отлично, заказ сформирован')
    chat_id = 6113251330
    bot.send_message(chat_id ,f'Имя клиента: {order.client_name}\nДата заказа: {order.date}\nАдрес клиента: {order.address}\nДоставить к: {order.time}',
                     )

