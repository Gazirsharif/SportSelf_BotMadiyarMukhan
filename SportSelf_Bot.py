from RandomWordGenerator import RandomWord

from flask import Flask, request
import logging
import os

from string import Template

from telebot import types
import requests
import telebot
import random


import config


bot = telebot.TeleBot(config.token)

list_beg_time = [] #???


@bot.message_handler(commands=['help'])
def MadiyarMukhan(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id,
                           "Заблудился путник? Я тебе помогу " + message.from_user.first_name + ", держи, это твои путеводители:\n /start /help /call",
                           reply_markup=markup)

@bot.message_handler(commands=['secret'])
def Secret(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    rw = RandomWord(max_word_size=5)
    send_mess = f"<b>Secret word: {rw.generate()}</b>!"
    bot.send_message(message.chat.id, send_mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['call'])
def send_welcome(message):
    # убрать клавиатуру Telegram полностью
    markup = types.ReplyKeyboardRemove(selective=False)

    msg = bot.send_message(message.chat.id,
                           "Привет " + message.from_user.first_name + ", Я бот-калькулятор калорий, чтобы узнать свою дневную норму калорий, следуйте указаниям.\nВведите cвой вес:",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, process_num1_step)


# введите первое число
def process_num1_step(message, user_result=None):
    try:
        global user_num1

        # запоминаем число
        # если только начали /start
        if user_result == None:
            user_num1 = int(message.text)
        else:
            # если был передан результат ранее
            # пишем в первое число, не спрашивая
            user_num1 = str(user_result)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('+')
        markup.add(itembtn1)

        msg = bot.send_message(message.chat.id, "Нажмите на плюс", reply_markup=markup)
        bot.register_next_step_handler(msg, process_proc1_step)
    except Exception as e:
        bot.reply_to(message, 'Это не число или что то пошло не так...')


# выберите операцию +, -, *, /
def process_proc1_step(message):
    try:
        global user_proc1

        # запоминаем операцию
        user_proc1 = message.text
        # убрать клавиатуру Telegram полностью
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(message.chat.id, "Еще один ингредиент ваш рост:", reply_markup=markup)
        bot.register_next_step_handler(msg, process_num2_step)
    except Exception as e:
        bot.reply_to(message, 'Вы ввели что то другое или что то пошло не так...')


# введите второе число
def process_num2_step(message):
    try:
        global user_num2

        # запоминаем число
        user_num2 = int(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('-')
        markup.add(itembtn1)

        msg = bot.send_message(message.chat.id, "Следующая операция минус нажмите на кнопку", reply_markup=markup)
        bot.register_next_step_handler(msg, process_proc2_step)
    except Exception as e:
        bot.reply_to(message, 'Это не число или что то пошло не так...')


# выберите операцию +, -, *, /
def process_proc2_step(message):
    try:
        global user_proc2

        # запоминаем операцию
        user_proc2 = message.text
        # убрать клавиатуру Telegram полностью
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(message.chat.id, "Сколько вам лет?", reply_markup=markup)
        bot.register_next_step_handler(msg, process_num3_step)
    except Exception as e:
        bot.reply_to(message, 'Вы ввели что то другое или что то пошло не так...')


# введите третье число
def process_num3_step(message):
    try:
        global user_num3

        # запоминаем число
        user_num3 = int(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('-')
        itembtn2 = types.KeyboardButton('+')
        markup.add(itembtn1, itembtn2)

        msg = bot.send_message(message.chat.id, "Ваш пол? Если вы Женщина то нажмите на -, если вы Мужчина то на +",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, process_proc3_step)
    except Exception as e:
        bot.reply_to(message, 'Это не число или что то пошло не так...')


# выберите операцию +, -, *, /
def process_proc3_step(message):
    try:
        global user_proc3

        # запоминаем операцию
        user_proc3 = message.text
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(message.chat.id, "Если вы Женщина то напишите 165, если вы Мужчина то 5",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, pol_step)
    except Exception as e:
        bot.reply_to(message, 'Вы ввели что то другое или что то пошло не так...')


# введите пол
def pol_step(message):
    try:
        global pol

        # запоминаем число
        pol = int(message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        itembtn1 = types.KeyboardButton('Результат')
        markup.add(itembtn1)

        msg = bot.send_message(message.chat.id, "Ваш результат!", reply_markup=markup)
        bot.register_next_step_handler(msg, process_alternative_step)
    except Exception as e:
        bot.reply_to(message, 'Это не число или что то пошло не так...')


# показать результат
def process_alternative_step(message):
    try:
        # сделать вычисление
        calc()

        # убрать клавиатуру Telegram полностью
        markup = types.ReplyKeyboardRemove(selective=False)

        if message.text.lower() == 'результат':
            bot.send_message(message.chat.id, calcResultPrint(), reply_markup=markup)
            bot.send_message(message.chat.id, calcResultPrint1(), reply_markup=markup)
            bot.send_message(message.chat.id, calcResultPrint2(), reply_markup=markup)

    except Exception as e:
        bot.reply_to(message, 'Что то пошло не так...')


# Вывод результата пользователю
def calcResultPrint():
    global user_num1, user_num2, user_num3, pol, user_proc1, user_proc2, user_proc3, user_result
    return "Результат: " + str(user_num1 * 10) + ' ' + user_proc1 + ' ' + str(
        user_num2 * 6.25) + ' ' + user_proc2 + ' ' + str(user_num3) + ' ' + user_proc3 + ' ' + str(pol) + ' = ' + str(
        user_result)


def calcResultPrint1():
    global user_num1, user_result1
    return "Сколько калорий в день нужно для быстрого похудения:" + str(user_result1)


def calcResultPrint2():
    global user_num1, user_result2
    return "Сколько калорий в день нужно для безопасного похудения:" + str(user_result2)


# Вычисление
def calc():
    global user_num1, user_num2, user_num3, pol, user_proc1, user_proc2, user_proc3, user_result, user_result1, user_result2

    user_result = 1.3 * eval(
        str(10 * user_num1) + user_proc1 + str(6.25 * user_num2) + user_proc2 + str(user_num3) + user_proc3 + str(pol))
    user_result1 = eval(str(user_num1 * 0.9 * 24))
    user_result2 = eval(str(user_num1 * 1.1 * 24))
    return user_result
    return user_result1
    return user_result2


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Здравствуйте "
                     + message.from_user.first_name
                     + ", Каким видом спорта вы хотите занятся? Для доп.инфы нужно писать /help", reply_markup=markup_menu)


# Начальные Кнопки

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn_1 = types.KeyboardButton('Бег')
btn_2 = types.KeyboardButton('Бокс')
btn_3 = types.KeyboardButton('Футбол')
btn_4 = types.KeyboardButton('Заряд для мотивации')
btn_5 = types.KeyboardButton('Калориметр')
btn_6 = types.KeyboardButton('Выход')
markup_menu.add(btn_1, btn_2, btn_3, btn_4, btn_5, btn_6)

# Бег

vmenyu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_n1 = types.KeyboardButton('Записать результаты')
btn_n2 = types.KeyboardButton('Инструкции')
btn_n3 = types.KeyboardButton('Навигатор')
btn_n4 = types.KeyboardButton('Музыка')
btn_n5 = types.KeyboardButton('На стартовое меню')
vmenyu.add(btn_n1, btn_n2, btn_n3, btn_n4, btn_n5)

#  Бокс

vmenyu1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_n11 = types.KeyboardButton('Новости')
btn_n12 = types.KeyboardButton('Советы')
btn_n13 = types.KeyboardButton('Мухаммед Али')
btn_n14 = types.KeyboardButton('Упражнении для бокса')
btn_n15 = types.KeyboardButton('На стартовое меню')
vmenyu1.add(btn_n11, btn_n12, btn_n13, btn_n14, btn_n15)

# Футбол

vmenyu2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_n21 = types.KeyboardButton('Финты - уроки')
btn_n22 = types.KeyboardButton('Дриблинги - уроки')
btn_n23 = types.KeyboardButton('Футбольные новости')
btn_n24 = types.KeyboardButton('Фрикик - уроки')
btn_n25 = types.KeyboardButton('На стартовое меню')
vmenyu2.add(btn_n21, btn_n22, btn_n23, btn_n24, btn_n25)

# Заряд для мотивации

vmenyu3 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_n31 = types.KeyboardButton('Шутка')
btn_n32 = types.KeyboardButton('Мотивационный канал')
btn_n33 = types.KeyboardButton('Получить задание')
btn_n34 = types.KeyboardButton('На стартовое меню')
vmenyu3.add(btn_n31, btn_n32, btn_n33, btn_n34, )

# Комплексная тренировка для жиросжигание

vmenyu4 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_n41 = types.KeyboardButton('Начальный')
btn_n42 = types.KeyboardButton('Средний')
btn_n43 = types.KeyboardButton('Высокий')
btn_n44 = types.KeyboardButton('На стартовое меню')
vmenyu4.add(btn_n41, btn_n42, btn_n43, btn_n44, )

# Записать результаты бега

vmenyu5 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_n51 = types.KeyboardButton('Силовая упражнения')
btn_n52 = types.KeyboardButton('Кардио упражнения')
btn_n53 = types.KeyboardButton('Упражнения для скорость')
btn_n55 = types.KeyboardButton('На стартовое меню')
vmenyu5.add(btn_n51, btn_n52, btn_n53, btn_n55)

vmenyu6 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_n61 = types.KeyboardButton('15 мин')
btn_n62 = types.KeyboardButton('30 мин')
btn_n63 = types.KeyboardButton('45 мин')
btn_n64 = types.KeyboardButton('60 мин')
btn_n65 = types.KeyboardButton('На стартовое меню')
vmenyu6.add(btn_n61, btn_n62, btn_n63, btn_n64, btn_n65)

vmenyu_back = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
btn_n_back = types.KeyboardButton('На стартовое меню')
vmenyu_back.add(btn_n_back)

user_num1 = ''
user_num2 = ''
user_num3 = ''
pol = ''
user_proc1 = ''
user_proc2 = ''
user_proc3 = ''
user_result = None
user_result1 = ''
user_result2 = ''


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Бег':
        bot.reply_to(message, "Какую опцию вы хотите?",
                     reply_markup=vmenyu)

    # 1

    if message.text == 'Записать результаты':
        bot.reply_to(message, """ 
           Запишите сюда сколько минут вы пробежали. Например: 15""",
                     reply_markup=vmenyu6)

    # 11

    if message.text == '15 мин':
        text = """https://play.google.com/store/apps/details?id=com.runtastic.android&hl=ru&gl=US"""
        bot.reply_to(message, """Отлично, если у вас вес 60 кг и бегали в темпе 6 мин/км - то вы потратили 155 ккал.
        Если хотите отслеживать свой маршрут движении, и посчитать количество шагов, то вы можете использовать приложения - фитнес трекер
        Вы можете скачивать приложения перейдя на эту ссылку:""", reply_markup=vmenyu6)
        bot.send_animation(chat_id=message.chat.id,
                           animation='https://play-lh.googleusercontent.com/VVQDP3bhier4_ju8kKjBrmKCSzWtsejX5xkfuS2OkyhiQvC777_1lZoeSY4Gi8ZCfAc=w720-h310-rw',
                           caption=text)

    if message.text == '30 мин':
        text = """https://play.google.com/store/apps/details?id=com.runtastic.android&hl=ru&gl=US"""
        bot.reply_to(message, """Отлично, если у вас вес 60 кг и бегали в темпе 6 мин/км - то вы потратили 310 ккал.
        Если хотите отслеживать свой маршрут движении, и посчитать количество шагов, то вы можете использовать приложения - фитнес трекер
        Вы можете скачивать приложения перейдя на эту ссылку:""", reply_markup=vmenyu6)
        bot.send_animation(chat_id=message.chat.id,
                           animation='https://play-lh.googleusercontent.com/VVQDP3bhier4_ju8kKjBrmKCSzWtsejX5xkfuS2OkyhiQvC777_1lZoeSY4Gi8ZCfAc=w720-h310-rw',
                           caption=text)

    if message.text == '45 мин':
        text = """https://play.google.com/store/apps/details?id=com.runtastic.android&hl=ru&gl=US"""
        bot.reply_to(message, """Отлично, если у вас вес 60 кг и бегали в темпе 6 мин/км - то вы потратили 465 ккал.
        Если хотите отслеживать свой маршрут движении, и посчитать количество шагов, то вы можете использовать приложения - фитнес трекер
        Вы можете скачивать приложения перейдя на эту ссылку:""", reply_markup=vmenyu6)
        bot.send_animation(chat_id=message.chat.id,
                           animation='https://play-lh.googleusercontent.com/VVQDP3bhier4_ju8kKjBrmKCSzWtsejX5xkfuS2OkyhiQvC777_1lZoeSY4Gi8ZCfAc=w720-h310-rw',
                           caption=text)

    if message.text == '60 мин':
        text = """https://play.google.com/store/apps/details?id=com.runtastic.android&hl=ru&gl=US"""
        bot.reply_to(message, """Отлично, если у вас вес 60 кг и бегали в темпе 6 мин/км - то вы потратили 620 ккал.
        Если хотите отслеживать свой маршрут движении, и посчитать количество шагов, то вы можете использовать приложения - фитнес трекер
        Вы можете скачивать приложения перейдя на эту ссылку:""", reply_markup=vmenyu6)
        bot.send_animation(chat_id=message.chat.id,
                           animation='https://play-lh.googleusercontent.com/VVQDP3bhier4_ju8kKjBrmKCSzWtsejX5xkfuS2OkyhiQvC777_1lZoeSY4Gi8ZCfAc=w720-h310-rw',
                           caption=text)

    # 2
    if message.text == 'Инструкции':
        text = """https://www.youtube.com/watch?v=JvhLfDsdw0E"""
        bot.reply_to(message, """
Чтобы решиться на первую пробежку, необходимо пройти минимальное обследование: измерить давление, сделать кардиограмму и провести ультразвуковое исследование сердца. 
Врачи рекомендуют такое обследование дополнить холтеровским мониторированием (функциональный метод диагностики, при котором обследуется сердечно-сосудистая система) или стресс-тестом 
(ЭКГ с нагрузкой на организм, выполняется на велоэргометре). По данным показателям кардиолог определяет степень нагрузки организма при беге. 
Если имеются хронические заболевания, то требуется индивидуальная консультация врача. Посетите канал чтобы получить полезные советы про бег:
        """, reply_markup=vmenyu)
        bot.send_photo(chat_id=message.chat.id,
                       photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQw-oh1aPqiJeZfCDNOBHu5XDeOqMJkrRDjuQ&usqp=CAU',
                       caption=text)
    # НАвигация для бега
    if message.text == 'Навигатор':
        text = """https://play.google.com/store/apps/details?id=com.runtastic.android&hl=ru&gl=US"""
        bot.reply_to(message, """Если хотите отслеживать свой маршрут движении, и посчитать количество шагов, то вы можете использовать приложения - фитнес трекер
        Вы можете скачивать приложения перейдя на эту ссылку:""", reply_markup=vmenyu_back)
        bot.send_animation(chat_id=message.chat.id,
                           animation='https://play-lh.googleusercontent.com/VVQDP3bhier4_ju8kKjBrmKCSzWtsejX5xkfuS2OkyhiQvC777_1lZoeSY4Gi8ZCfAc=w720-h310-rw',
                           caption=text)

    # Музыка

    if message.text == 'Музыка':
        text = """Давайте слушая музыку, мотивируем себя для бега"""
        bot.reply_to(message, """Бегание очень полезное для здоровья...""", reply_markup=vmenyu_back)
        bot.send_audio(chat_id=message.chat.id,
                       audio='https://oxy.sunproxy.net/file/ejdrQXRuM3EzdnFsdTNqdGpWNW5SRWJldktZOVNRZHVBM3RRNU5JTmVHVjVSelRaNmVTME5vRjlpWGFlNGN1K2JZM1NLa1BhcWp6RFliQTdxam9sK3R5UWJFZVF0N0UxNXJpMHJvcXhRcFk9/Clean_Bandit_ft._Zara_Larsson_-_Symphony_(oxy.fm).mp3',
                       caption=text)
        bot.send_audio(chat_id=message.chat.id,
                       audio='https://oxy.sunproxy.net/file/ejdrQXRuM3EzdnFsdTNqdGpWNW5SRWJldktZOVNRZHVBM3RRNU5JTmVHVjVSelRaNmVTME5vRjlpWGFlNGN1KzVVSm82TEMwR21IZXRBL013S01JcUVKbWtFZU4rY0Z5eERqMHBKelR2S2s9/Eminem_feat._Nate_Dogg_-_Till_I_Collapse_(oxy.fm).mp3',
                       caption=text)
        bot.send_audio(chat_id=message.chat.id,
                       audio='https://oxy.sunproxy.net/file/ejdrQXRuM3EzdnFsdTNqdGpWNW5SRWJldktZOVNRZHVBM3RRNU5JTmVHVjVSelRaNmVTME5vRjlpWGFlNGN1K0ZxdEhmZHM0SmRCalQwTSs5aWpCQmpwcDFDZEw4VUl5NVRPTzJkdXA4RDQ9/YARMAK_-_Gni_svoyu_liniyu_(oxy.fm).mp3',
                       caption=text)

    # назад

    if message.text == 'На стартовое меню':
        bot.reply_to(message, "ОК",
                     reply_markup=markup_menu)

    # Бокс
    if message.text == 'Бокс':
        bot.reply_to(message, "Что хотите посмотреть?", reply_markup=vmenyu1)

    # НОвости про бокс

    if message.text == 'Новости':
        text = """https://vesti.kz/boxing/"""
        bot.reply_to(message, """Все последние новости из мира бокса. Все событи в мире бокса, боксеры, 
        обзоры боксерских поединков Посетите сайт чтобы узнать новости про бокс:""", reply_markup=vmenyu1)
        bot.send_photo(chat_id=message.chat.id,
                       photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTdlaYJCQlEKtL-KfuczbE6rATP6-NnsdGj6Q&usqp=CAU',
                       caption=text)

    # Советы чтобы заниматься боксом

    if message.text == 'Советы':
        text = """https://www.expertboxing.ru/sovety-po-boksu"""
        bot.reply_to(message, ("Секция Советы по Боксу содержит несколько вещей, которые ты можешь применить, \n"
                               "        когда зайдешь в ринг в следующий раз, или короткие памятки для старых советов по боксу, о которых ты забыл \n"
                               "        Посетить канал:"), reply_markup=vmenyu1)
        bot.send_photo(chat_id=message.chat.id,
                       photo='https://manfit.ru/upload/iblock/e25/e259001d0967673ec1a0b79ecc948177.jpg',
                       caption=text)

    # Мухаммед Али

    if message.text == 'Мухаммед Али':
        text = """https://www.youtube.com/watch?v=jY3hMP0uShY"""
        bot.reply_to(message, ("""Американский боксер, чемпион Олимпийских игр 1960 года Мохаммед Али (настоящее имя — Кассиус Марцеллиус Клей) 
родился 17 января 1942 года в Луисвилле (штат Кентукки, США).
Боксом начал заниматься с раннего детства.
В 1959 году попал в Олимпийскую сборную США.
В 1960 году в Риме (Италия) Кассиус Клей под своим именем стал чемпион Олимпийских игр в полутяжелом весе. 
После этого перешел в профессионалы.
В 1963 году Кассиус Клей победил Дага Джонса. Бой получил статус "бой года" по версии журнала "Ринг"
В 1964 году Кассиус Клей получил свое первое звание чемпиона в результате боя с Сонни Листоном, победив его техническим нокаутом в седьмом раунде. 
В том же году Клей принял ислам и изменил имя на Мохаммед Али.
25 мая 1965 года состоялся повторный поединок между Мохаммедом Али и Сонни Листоном, в котором снова победил Али.
В 1966-1967 годах боксер защитил свой титул против Брайна Лондона, Карла Милденбергера, Кливленда Уильямса, Эрни Террела и Зоры Фолли.
В 1967 году во время войны с Вьетнамом Мохаммед Али был призван в армию США, но отказался участвовать в войне. 
Звание его было аннулировано, а самого боксера осудили на пять лет, за уклонение от службы. 
В это время Али было запрещено заниматься боксом. В 1970 году Верховный суд США отменил приговор, и боксер вернулся на ринг.
В марте 1971 года Мохаммед Али впервые вышел на ринг против Джо Фрейзера. Этот бой впоследствии был назван "боем года" по версии журнала "Ринг". 
В 15-м раунде Али побывал в нокдауне, а после окончания поединка судьи пришли к выводу, что бой он проиграл. 
Это было первое поражение Али в карьере.
В 1974 году состоялся второй поединок между Мохаммедом Али и Джо Фрейзером. В этом бою победил Али, выиграв его по очкам.
30 октября 1974 года состоялся бой за звание чемпиона мира между Джоржем Форменом, действующим чемпионом, и претендентом Мухаммедом Али. Этот бой специалисты считают, как "величайший и незабываемый". 
Его выиграл Али, став чемпионом.
1 октября 1975 года Али провел ещё один поединок, который тоже навсегда остался в истории мирового бокса. Им стал поединок, в котором Мохаммед Али в третий раз встречался с Джо Фрейзером и опять победил его.
В 1976 году Мохаммед Али успешно защитил титулы против Жана-Пьера Купмана, Джимми Янга и Ричарда Данна. В 1977 году победил Альфредо Евангелисту и Эрни Шейверса.
В 1978 году Мохаммед Али решил закончить карьеру боксера. Для завершающего боя был выбран олимпийский чемпион 1976 года Леон Спинкс, которому Али проиграл. 
Бой получил статус "Бой года" по версии журнала "Ринг".
Али вызвал Леона Спинкса на реванш, который прошел 15 сентября 1978 года. 
В этот раз Али выиграл единогласным решением судей. После чего ушел из бокса. 
Из-за финансовых трудностей ему вскоре снова пришлось выйти на ринг. 
Но лишь для того, чтобы проиграть два боя — один в октябре 1980 года против Ларри Холмса и второй против Тревора Бербика в декабре 1981 года. 
После чего Али окончательно ушел из бокса.
Вскоре у спортсмена была обнаружена болезнь Паркинсона.
В 1990 году Али был избран в Национальный зал славы бокса. В 1996 году он нес факел на летних Олимпийских играх в Атланте.
Мохаммед Али — чемпион Олимпийских игр 1960 года, абсолютный чемпион мира в тяжёлом весе (1964-1966, 1974-1978), чемпион мира в тяжёлом весе по версиям WBC (1974-1978), WBA (1967, 1974-1978, 1978). 
Журнал "Ринг" пять раз признавал его "Боксёром года" (1963, 1972, 1974, 1975, 1978) и, кроме того, "Боксёром десятилетия" (1970-е). 
В 1999 году Sports Illustrated и BBC назвали Али "Спортсменом века". 
Награжден президентской медалью Свободы (2005), филадельфийской медалью свободы и др. Получил звание Почетного жителя Кентукки и гражданина Кентукки столетия.
Посмотрите лушчие бои великого боксера который шокировал весь мир:"""), reply_markup=vmenyu1)
        bot.send_photo(chat_id=message.chat.id,
                       photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS_vl5EqD5viObUwLLiWtRixP-lEH12zc6wmA&usqp=CAU',
                       caption=text)

    # упр бокс

    if message.text == 'Упражнении для бокса':
        bot.reply_to(message, """Выбирайте один из них:""",
                     reply_markup=vmenyu5)

    if message.text == 'Силовые упражнения':
        text = """http://boxinglegends.ru/silovaya-trenirovka-boksyora-uprazhneniya-na-plechi-bitseps-tritseps/"""
        bot.reply_to(message, """Силовая тренировка боксёра.
        Посетить сайт:""", reply_markup=vmenyu5)
        bot.send_animation(chat_id=message.chat.id,
                           animation='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSlwMpm6zBSBVV5gK67A7SKEndpyH7Xgy_YFA&usqp=CAU',
                           caption=text)

    if message.text == 'Кардио упражнения':
        text = """https://bazaar.ru/beauty/health/dlya-teh-kto-ne-lyubit-beg-5-kardio-uprazhneniy-iz-boksa-ot-diany-arbeninoy/"""
        bot.reply_to(message, """Кардио упражнение боксёра.
        Посетить сайт:""", reply_markup=vmenyu5)
        bot.send_animation(chat_id=message.chat.id,
                           animation='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1_ESbUqTu_dTllx3BQ7MXi1A1jyulrF8oLw&usqp=CAU',
                           caption=text)

    if message.text == 'Упражнения для скорость':
        text = """https://www.youtube.com/watch?v=kg4LIQ_fgRc"""
        bot.reply_to(message, """Скорость ударов в боксе и выносливость ног — фактор, который позволит выстоять даже против превосходящего по силе противника. 
        Два простых упражнения на тренировку скорости ударов руками и внимательность помогут бить быстрее, развить тайминг и молниеносную реакцию.
        Посмотреть канал:""", reply_markup=vmenyu5)
        bot.send_animation(chat_id=message.chat.id,
                           animation='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1_ESbUqTu_dTllx3BQ7MXi1A1jyulrF8oLw&usqp=CAU',
                           caption=text)

    #     Фуутбол

    if message.text == 'Футбол':
        bot.reply_to(message, "Что хотите посмотреть?", reply_markup=vmenyu2)

    # 1

    if message.text == 'Финты - уроки':
        text = """https://www.youtube.com/watch?v=5BXdCUu1OvE&t=16s"""
        bot.reply_to(message, """Футбольный финт — это движения, вследствие которых соперника вводят в заблуждение, 
        обманный приём, исполненный футболистом. 
        Качественное исполнение финтов зависит от наличия у футболиста необходимых физических и психических качеств, 
        его интуиции и возможности импровизировать. Тут особенную роль играет: богатое воображение, скорость реакции, 
        высота центра тяжести корпуса тела, скорость и общая физическая подготовка.
        Посетите канал чтобы научиться финтить:""", reply_markup=vmenyu2)
        bot.send_photo(chat_id=message.chat.id,
                       photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSIj_Kfqy7VLB9ygQ7WQZJATwchafBWt8qxA&usqp=CAU',
                       caption=text)

    # дриблинг

    if message.text == 'Дриблинги - уроки':
        text = """https://www.youtube.com/watch?v=_P0abmeP_mQ"""
        bot.reply_to(message, """Дриблинг - навык ведения мяча в футболе, достаточно сложное умение для тренировки, 
        но роль дриблинга в футболе слишком велика, чтобы не уделять внимание обучению дриблинга.
        Посетите канал чтобы научиться как делать дриблинг:""", reply_markup=vmenyu2)
        bot.send_photo(chat_id=message.chat.id,
                       photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQhxyKXKppr3cdtFDg3qbFWeTb-_YqkpWxPOg&usqp=CAU',
                       caption=text)

    # Футбол новость

    if message.text == 'Футбольные новости':
        text = """https://news.sportbox.ru/Vidy_sporta/Futbol"""
        bot.reply_to(message, """Ежедневные новости футбола. Обзоры матчей, календарь игр чемпионата России и Еврокубков, результаты, турнирные таблицы.
        Посетите сайт чтобы узнать новости про футбол:""", reply_markup=vmenyu2)
        bot.send_photo(chat_id=message.chat.id,
                       photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQoozmtYQcflRnEkssF_t_kdZqa93_rQQkYSg&usqp=CAU',
                       caption=text)

    # Фрикик

    if message.text == 'Фрикик - уроки':
        text = """https://www.youtube.com/watch?v=-fSnxd7I60o"""
        bot.reply_to(message, """Свободный удар является способом возобновления игры в футболе . 
        Он присуждается после нарушения правил противоположной командой.
        Посетите канал чтобы научиться как сделать фрикик:""", reply_markup=vmenyu2)
        bot.send_photo(chat_id=message.chat.id,
                       photo='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTDVEZqVClV1FqgLFaFK1TjRYxsLy3Nn-WBkg&usqp=CAU',
                       caption=text)

    # ЗДМ

    if message.text == 'Заряд для мотивации':
        bot.reply_to(message, "Какую опцию вы хотите?", reply_markup=vmenyu3)

    # ЗДМ

    if message.text == 'Шутка':
        text = """Давайте мотивируем себя глядя на этот кот"""
        bot.reply_to(message, """Давайте посчитаем сколько раз котик подтянется...""", reply_markup=vmenyu3)
        bot.send_animation(chat_id=message.chat.id,
                           animation='https://cs8.pikabu.ru/post_img/2016/04/07/7/1460029941192073733.gif',
                           caption=text)

    # Мотив канал

    if message.text == 'Мотивационный канал':
        text = """https://www.youtube.com/channel/UC43V5k5_zeO8MTk3-tCB3fQ"""
        bot.reply_to(message, """Давайте мотивируем себя посмотрев ролики  на этого канала...""", reply_markup=vmenyu3)
        bot.send_animation(chat_id=message.chat.id,
                           animation='https://yt3.ggpht.com/ytc/AAUvwnjHTLyyBpwadeEybv7eKkGrzL5PNWicSu0FA2dkHg=s48-c-k-c0xffffffff-no-rj-mo',
                           caption=text)

    # 3
    if message.text == 'Получить задание':
        a = random.randint(1, 3)
        if a == 1:
            send_mess = f"<b>Движение это полезно для здоровья. Сделай отжимание вот столько раз: {str(random.randint(0, 30))}</b>!"
            bot.send_message(message.chat.id, send_mess, parse_mode='html')
        elif a == 2:
            send_mess = f"<b>Движение это полезно для здоровья. Сделай прыжок вот столько раз: {str(random.randint(60, 90))}</b>!"
            bot.send_message(message.chat.id, send_mess, parse_mode='html')
        elif a == 3:
            send_mess = f"<b>Движение это полезно для здоровья. Сделай пресс вот столько раз: {str(random.randint(30, 60))}</b>!"
            bot.send_message(message.chat.id, send_mess, parse_mode='html')

    if message.text == 'Калориметр':
        bot.reply_to(message, """Если хотите узнать ваш калория в организме то нажмите на /call """,
                     reply_markup=markup_menu)

    if message.text == 'Выход':
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Отключаюсь на подзарядк...", reply_markup=markup)


####################################################################################################################################################


async def init_app(loop):
    app = web.Application(loop=loop, middlewares=[])
    app.router.add_post('/api/v1', handler)
    return app


TOKEN = '1472085738:AAEsHXJULHZd2PXhbYph0aDzmHvuyPu1L68'
API_URL = 'https://api.telegram.org/bot%s/sendMessage' % TOKEN

...


async def handler(request):
    data = await request.json()
    headers = {
        'Content-Type': 'application/json'
    }
    message = {
        'chat_id': data['message']['chat']['id'],
        'text': data['message']['text']
    }
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.post(API_URL,
                                data=json.dumps(message),
                                headers=headers) as resp:
            try:
                assert resp.status == 200
            except:
                return web.Response(status=500)
    return web.Response(status=200)


###################################################################################################################
# Здесь пишем наши хэндлеры

# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)
if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)


    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200


    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(
            url="https://min-gallows.herokuapp.com/bot")  # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200


    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    bot.polling(none_stop=True)

bot.polling(none_stop=True)
