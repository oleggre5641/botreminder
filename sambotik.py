import telebot
import time
import sqlite3
import threading
from datetime import datetime
from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE
from telebot.types import ReplyKeyboardRemove, CallbackQuery

f = open('project.conf')
for token in f:
    print(token)

API_TOKEN = token
print(API_TOKEN)
bot = telebot.TeleBot(token=API_TOKEN)

def czif(a):
    tru = 0
    if len(a) > 5:
        return False
    elif len(a) < 5:
        return False
    if a[0].isnumeric() == True:
        if int(a[0]+a[1]) <= 31 and int(a[0]+a[1]) != 0:
            tru += 1
    if a[1].isnumeric() == True:
        tru += 1
    if a[2] == ".":
        tru += 1
    if a[3].isnumeric() == True:
        if int(a[3] + a[4]) <= 12 and int(a[3] + a[4]) != 0:
            tru += 1
    if a[4].isnumeric() == True:
        tru += 1
    if tru == 5:
        return True
    return False

def czif(a):
    tru = 0
    if len(a) > 5:
        return False
    elif len(a) < 5:
        return False
    if a[0].isnumeric() == True:
        if int(a[0]+a[1]) <= 31 and int(a[0]+a[1]) != 0:
            tru += 1
    if a[1].isnumeric() == True:
        tru += 1
    if a[2] == ".":
        tru += 1
    if a[3].isnumeric() == True:
        if int(a[3] + a[4]) <= 12 and int(a[3] + a[4]) != 0:
            tru += 1
    if a[4].isnumeric() == True:
        tru += 1
    if tru == 5:
        return True
    return False

def chTime(a):
    tru = 0
    if len(a) > 5:
        return False
    elif len(a) < 5:
        return False
    if a[0].isnumeric() == True:
        if int(a[0]+a[1]) < 24:
            tru += 1
    if a[1].isnumeric() == True:
        tru += 1
    if a[2] == ".":
        tru += 1
    if a[3].isnumeric() == True:
        if int(a[3] + a[4]) <= 59:
            tru += 1
    if a[4].isnumeric() == True:
        tru += 1
    if tru == 5:
        return True
    return False



def remember(a):
    while(True):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        now = datetime.now()
        today = datetime.today()
        todayD = today.strftime("%d.%m")
        current_time = now.strftime("%H.%M")
        cur.execute(f"SELECT id,id_telegram,remindtext FROM users WHERE activeornot='TRUE' AND datetext='{todayD}' AND timetext='{current_time}';")
        one_result = cur.fetchall()
        if len(one_result) > 0:
            print(one_result)
            bot.send_message(one_result[0][1], one_result[0][2])
            sql_delete_query = (f"""DELETE from users WHERE id = {one_result[0][0]}""")
            cur.execute(sql_delete_query)
            conn.commit()

            # print(f"SELECT id_telegram,remindtext FROM users WHERE activeornot='TRUE' AND datetext={todayD} AND timetext={current_time};")
        time.sleep(1)

# datetext={todayD} and timetext={current_time} and

t1 = threading.Thread(target=remember, args=(1,))
t1.start()




conn = sqlite3.connect('users.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   id_telegram TEXT, 
   remindtext TEXT,
   datetext TEXT,
   timetext TEXT,
   activeornot TEXT
   );
""")
conn.commit()
# time.sleep(33333)


calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")


def getRem(id_telegram):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute(f"SELECT id,remindtext,datetext,timetext FROM users WHERE id_telegram = {id_telegram};")
    one_result = cur.fetchall()
    return one_result

def knpInput(message):
    if message.text == "Создать напоминание":
        msg = bot.send_message(message.from_user.id,text="О чём вам напомнить?")
        bot.register_next_step_handler(msg,kbInput)
    if message.text == "Мои напоминания":
        one_result = getRem(message.from_user.id)
        if len(one_result) != 0:
            result = ""
            for i in range(len(one_result)):
                result += "\n"
                result += str(f"{i + 1} : {one_result[i][1]} -- {one_result[i][2]} -- {one_result[i][3]}")

            bot.send_message(message.from_user.id,result)
            menu(message.from_user.id)
        else:
            bot.send_message(message.from_user.id,text="У вас нет напоминаний",)
            menu(message.from_user.id)
    if message.text == "Удалить напоминание":
        one_result = getRem(message.from_user.id)
        if len(one_result) > 0:
            keyboard_menu = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
            result = ""
            for i in range(len(one_result)):
                keyboard_menu.row(f" {i + 1} \n")
                result += "\n"
                result += str(f"{i + 1} : {one_result[i][1]} -- {one_result[i][2]} -- {one_result[i][3]}")
            delremaa = bot.send_message(message.from_user.id, text=f"Выберите напоминание которое вы собираетесь удалить:\n {result}",reply_markup=keyboard_menu)
            bot.register_next_step_handler(delremaa ,delRem)
        else:
            bot.send_message(message.from_user.id, text="У вас нет напоминаний", )
            menu(message.from_user.id)

    if message.text == "О нас":
        bot.send_message(message.from_user.id,text="Писать сюда:\n@shyuii\nКидать сюда:\n2200700153064489")
        menu(message.from_user.id)

def delRem(message):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    one_result = getRem(message.from_user.id)
    idfordel = message.text
    idj = one_result[int(idfordel) - 1][0]
    sql_delete_query = (f"""DELETE from users where id = {idj}""")
    cur.execute(sql_delete_query)
    conn.commit()
    bot.send_message(message.from_user.id,"Напоминание удалено!")
    menu(message.from_user.id)

def kbInput(message):
    reminde = message.text
    now = datetime.now()  # Get the current date
    bot.send_message(
        message.chat.id,
        "Выберите Дату",
        reply_markup=calendar.create_calendar(
            name=calendar_1_callback.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )

    @bot.callback_query_handler(
        func=lambda call: call.data.startswith(calendar_1_callback.prefix)
    )
    def callback_inline(call: CallbackQuery):
        # At this point, we are sure that this calendar is ours. So we cut the line by the separator of our calendar
        name, action, year, month, day = call.data.split(calendar_1_callback.sep)
        # Processing the calendar. Get either the date or None if the buttons are of a different type
        date = calendar.calendar_query_handler(
            bot=bot, call=call, name=name, action=action, year=year, month=month, day=day
        )
        # There are additional steps. Let's say if the date DAY is selected, you can execute your code. I sent a message.
        if action == "DAY":
            bot.send_message(
                chat_id=call.from_user.id,
                text=f"Вы выбрали дату: {date.strftime('%d.%m.%Y')}",
                reply_markup=ReplyKeyboardRemove(),
            )
        daterem = date.strftime("%d.%m")
        print(daterem)
        idd = message.from_user.id
        tmImput(daterem,idd,reminde)

def tmImput(daterem,idd,reminde):
    msg = bot.send_message(idd, text="Напишите время(МСК)\nПример : 12.00")
    bot.register_next_step_handler(msg,aprInput,daterem,reminde)


def aprInput(message,daterem,reminde):
    timerem = message.text
    if chTime(timerem) == True:
        keyboard_menu = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
        keyboard_menu.row('Да')
        keyboard_menu.row('Нет')
        msg = bot.send_message(message.from_user.id, text=f"Всё правильно?(Да,Нет)\n\n{reminde}\n{daterem}\n{timerem}",reply_markup=keyboard_menu)
        bot.register_next_step_handler(msg,lastInput, timerem,daterem,reminde)
    else:
        msg = bot.send_message(message.from_user.id,text="Вы допустили ошибку в написанни времени,введите её заново\nПример : 12.00")
        bot.register_next_step_handler(msg, aprInput, daterem,reminde)


def lastInput(message,timerem,daterem,reminde):
    proverka = message.text
    if proverka == "Да":
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        bot.send_message(message.from_user.id, text="Обязательно напомню")
        cur.execute(f"""INSERT INTO users(id_telegram,remindtext,datetext,timetext,activeornot)
            VALUES("{message.from_user.id}","{reminde}","{daterem}","{timerem}","TRUE");""")
        conn.commit()
        menu(message.from_user.id)
        print(message)
    else:
        msg = bot.send_message(message.from_user.id, text="О чём вам напомнить?")
        bot.register_next_step_handler(msg, kbInput)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard_menu = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
    keyboard_menu.row('Создать напоминание')
    keyboard_menu.row('Мои напоминания')
    keyboard_menu.row('Удалить напоминание')
    keyboard_menu.row('О нас')
    msg = bot.send_message(message.from_user.id,text="Привет!" ,reply_markup=keyboard_menu)
    bot.register_next_step_handler(msg,knpInput)

def menu(userid):
    keyboard_menu = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
    keyboard_menu.row('Создать напоминание')
    keyboard_menu.row('Мои напоминания')
    keyboard_menu.row('Удалить напоминание')
    keyboard_menu.row('О нас')
    msg = bot.send_message(userid,text="Выберите действие:" ,reply_markup=keyboard_menu)
    bot.register_next_step_handler(msg,knpInput)






bot.polling(none_stop=True, interval=0)


# апрель	июнь
# Количество дней
# Календарные	30	30