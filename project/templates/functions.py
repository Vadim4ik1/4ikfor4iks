import psycopg2
from typing import Tuple
import datetime

conn = psycopg2.connect(dbname='HotelV', user='postgres')
cursor = conn.cursor()

def word_strip(words):
    result = []
    for i in range(len(words)):
        if type(words[i]) == str:
            result.append(words[i].strip())
        else:
            result.append(words[i])
    return tuple(result)

def on_off(condition):
    if condition == "Да":
        condition = 'YES'
        return condition
    else:
        condition = 'NO'
        return condition

def yes_no(condition):
    # if condition == None:
    #     condition = 'Нет'
    #     return condition
    if type(condition) == bool:
        if condition == True:
            condition = 'Да'
            return condition
        if condition == False:
            condition = 'Нет'
            return condition
    else:
        return condition

def return_list(tup):
    listt = []
    for i in tup:
        listt.append(i[0])
    return listt

def rooms_req(type_room, room_num):
    """Вытаскивает комнаты из бд"""
    cursor.execute('SELECT "num_room" FROM "room" WHERE ("type_room" = '+"'"+str(type_room)+"' AND " + '"room_num" = ' +"'"+str(room_num)+"'"+")")
    # cursor.execute('SELECT * FROM "Room" WHERE ("Rooms" = '+"'"+str(rooms)+"'"+")")
    records = cursor.fetchall()
    records = return_list(records)
    return records

def guest_req(pass_num):
    """Вытаскивает гостя из бд"""
    cursor.execute('SELECT * FROM "guest" WHERE ("pass_num" = '+"'"+str(pass_num)+"'"+")")
    records = cursor.fetchall()
    return records

def booking_req(type_room, room_num, date_in, date_out):
    """Вытаскивает занятые комнаты из бд"""
    cursor.execute('SELECT "num_room" FROM "booking" WHERE ("type_room" = '+ "'" + str(type_room) + "'" +' AND "room_num" = '+ "'"+ str(room_num)+ "'"+ ' AND "date_in" = ' + "'" + str(date_in) + "'" + 'AND "date_out" = '+ "'" + str(date_out)+ "'" + ')')
    records = cursor.fetchall()
    records = return_list(records)
    return records

def booking(type_room, guest_num, room_num, date_in, date_out, trans_in, trans_out, exc, food, fitness, bar, comm, num_room):
    cursor.execute('INSERT INTO "booking" ("type_room", "guest_num", "room_num", "date_in", "date_out", "trans_in", "trans_out", "exc", "food", "fitness", "bar", "comm", "num_room", "status") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (type_room, guest_num, room_num, date_in, date_out, trans_in, trans_out, exc, food, fitness, bar, comm, num_room, "Не подтвержден"))
    conn.commit()
    # print("success")

def history_add(pass_num):
    cursor.execute('SELECT "history" FROM "guest" WHERE ("pass_num" = '+"'"+str(pass_num)+"'"+")")
    records = cursor.fetchone()
    # print(records)
    history = records[0]
    # cursor.execute('UPDATE "guest" SET "history"=(%s) WHERE ("pass_num" = '+"'"+str(pass_num)+"'"+")", str(history+1))
    cursor.execute('UPDATE "guest" SET "history" =(%s) WHERE "pass_num" = (%s)', (str(history+1),str(pass_num)))
    conn.commit()

def guest(pass_num, f_name, l_name, o_name, gender, phone, email):
    cursor.execute('INSERT INTO "guest" ("pass_num", "f_name", "l_name", "o_name", "gender", "phone", "email", "history") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (pass_num, f_name, l_name, o_name, gender, phone, email, str(1)))
    conn.commit()

def guest_add(pass_num):
    cursor.execute('SELECT "booking_num" FROM "booking" WHERE ("booking_num" = (SELECT MAX("booking_num") FROM "booking"))')
    records = cursor.fetchone()[0]
    # print(records)
    cursor.execute('UPDATE "booking" SET "pass_num"= (%s) WHERE ("booking_num" = (%s))', (str(pass_num), str(records)))
    conn.commit()

def get_last_booking():
    cursor.execute('SELECT type_room, guest_num, room_num, date_in, date_out, trans_in, trans_out, exc, food, fitness, bar, exc_class, auto FROM "booking" WHERE ("booking_num" = (SELECT MAX("booking_num") FROM "booking"))')
    records = cursor.fetchone()
    records = word_strip(records)
    listt = []
    for i in range(len(records)):
        listt.append(records[i])
    return listt

def autorize(login, password):
    cursor.execute('SELECT "role" FROM roles WHERE (login = '+"'"+login+"' AND password = "+"'"+password+"'"+')')
    records = cursor.fetchone()
    return records
    
def all_guests():
    cursor.execute('SELECT pass_num, f_name, l_name, o_name, gender, phone, email, history FROM "guest"')
    records = cursor.fetchall()
    # print(records)
    for r in range(len(records)):
        records[r] = word_strip(records[r])
    return records

def in_guests():
    today = datetime.date.today()
    # print(today)
    cursor.execute('SELECT pass_num FROM "booking" WHERE "date_in" <=' + "'" +str(today)+ "'" +'AND "date_out" >='+"'"+ str(today) +"'")
    records = cursor.fetchall()
    # print(records)
    for r in range(len(records)):
        records[r] = word_strip(records[r])
    records = return_list(records)
    records = set(records)
    results = []
    for pass_num in records:
        cursor.execute('SELECT pass_num, f_name, l_name, o_name, gender, phone, email, history  FROM "guest" WHERE ("pass_num" = '+"'"+ str(pass_num)+"'"+ ')')
        rec = cursor.fetchone()
        results.append(rec)
    for r in range(len(results)):
        results[r] = word_strip(results[r])
    return results

def get_booking_for_pay(contract):
    cursor.execute('SELECT type_room, guest_num, room_num, date_in, date_out, trans_in, trans_out, exc, food, fitness, bar, num_room, booking_num, exc_class, auto, pass_num FROM "booking" WHERE ("contract" = ' +"'"+str(contract)+"'"+")")
    records = cursor.fetchone()
    records = word_strip(records)
    listt = []
    for i in range(len(records)):
        listt.append(records[i])
    return listt

def payment(pass_num, type_room, days, trans_in, trans_out, exc, food, fitness, bar, exc_class, auto):
    pay_punkts = []
    cost = costs()
    # print(cost)
    if type_room == "Эконом":
        room = cost[0][1]
        pay_punkts.append("Эконом +")
    if type_room == "Стандарт":
        room = cost[1][1]
        pay_punkts.append("Стандарт +")
    if type_room == "Комфорт":
        room = cost[2][1]
        pay_punkts.append("Комфорт +")
    if type_room == "Люкс":
        room = cost[3][1]
        pay_punkts.append("Люкс +")
    if type_room == "Президентский":
        room = cost[4][1]
        pay_punkts.append("Президентский +")
    sum_room = room*days

    if trans_in == "Да":
        sum_room += cost[5][1]
        pay_punkts.append("Трансфер от аэропорта до отеля + ")
    if trans_out == "Да":
        sum_room += cost[6][1]
        pay_punkts.append("Трансфер от отеля до аэропорта + ")
    if exc == "Да":
        sum_room += cost[7][1]
        pay_punkts.append("Бассейн + ")
    if food == "Да":
        sum_room += cost[8][1]*days
        pay_punkts.append("Питание + ")
    if fitness == "Да":
        sum_room += cost[9][1]*days
        pay_punkts.append("Фитнес + ")
    if bar == "Да":
        sum_room += cost[10][1]*days
        pay_punkts.append("Бар + ")

    if int(exc_class) == 1:
        sum_room += 2000
        pay_punkts.append("Экскурсия базовая + ")
    if int(exc_class) == 2:
        sum_room += 3500
        pay_punkts.append("Экскурсия средняя + ")
    if exc_class == "Нет":
        sum_room += 0
    if int(exc_class) == 3:
        sum_room += 5000
        pay_punkts.append("Экскурсия повышенная + ")
    if int(auto) == 1:
        sum_room += 1500*days
        pay_punkts.append("Автомобиль Ford + ")
    if int(auto) == 2:
        sum_room += 3000*days
        pay_punkts.append("Автомобиль BMW + ")
    if int(auto) == 3:
        sum_room += 4000*days
        pay_punkts.append("Автомобиль Cadillac + ")
    if auto == "Нет":
        sum_room += 0
    hist = history(pass_num)
    if int(hist) == 2:
        sum_room *= 0.97
        pay_punkts.append("Скидка 3%")
    if int(hist) == 3:
        sum_room *= 0.95
        pay_punkts.append("Скидка 5%")
    if int(hist) > 3 and int(hist) < 10:
        sum_room *= 0.93
        pay_punkts.append("Скидка 7%")
    if int(hist) > 10:
        sum_room *= 0.9
        pay_punkts.append("Скидка 10%")
    pay_punkts = " ".join(pay_punkts)
    return sum_room, pay_punkts

def costs():
    cursor.execute('SELECT "service_name", "service_cost" FROM "services"')
    records = list(cursor.fetchall())
    for i in range(len(records)):
        records[i] = word_strip(records[i])
    return records 

def history(pass_num):
    """Вытаскивает гостя из бд"""
    cursor.execute('SELECT "history" FROM "guest" WHERE ("pass_num" = '+"'"+str(pass_num)+"'"+")")
    records = cursor.fetchone()[0]
    return records 

def payment_insert(booking_num, num_room, days, pass_num, sum_room, paydate, contract):
    cursor.execute('INSERT INTO "payment" (booking_num, num_room, days, pass_num, sum, pay_date, contract) VALUES (%s, %s, %s, %s, %s, %s, %s)', (booking_num, num_room, days, pass_num, sum_room, paydate, contract))
    conn.commit()

def bookings():
    guests = []
    cursor.execute('SELECT pass_num, type_room, guest_num, room_num, date_in, date_out, status, trans_in, trans_out, exc, food, fitness, bar FROM "booking" WHERE ("status" = '+ "'" + "Не подтвержден" + "'" + ')')
    records = cursor.fetchall()
    for r in range(len(records)):
        records[r] = word_strip(records[r])
        cursor.execute('SELECT "f_name", "l_name", "o_name", "phone", "email" FROM "guest" WHERE ("pass_num" = '+"'"+str(records[r][0])+"'"+")")
        guest = cursor.fetchone()
        guests.append(guest)
    # print(records)
    # print(guests)
    for g in range(len(guests)):
        guests[g] = word_strip(guests[g])
    for r in range(len(records)):
        records[r] += guests[r]
    # print(records)
    return records

def add_status_to_booking(answers):
    cursor.execute('SELECT pass_num, date_in, date_out FROM "booking" WHERE ("status" = '+ "'" + "Не подтвержден" + "'" + ')')
    pass_num = cursor.fetchall()
    for i in range(len(answers)):
        if answers[i] == "Да":
            cursor.execute('UPDATE "booking" SET "status" = (%s) WHERE "pass_num" = (%s)', ("Подтвержден",str(pass_num[i][0])))
            conn.commit()
        if answers[i] == "Нет":
            cursor.execute('DELETE from "booking" WHERE "pass_num" = ' + "'"+str(pass_num[i][0])+ "'" + ' AND date_in = '+ "'"+str(pass_num[i][1])+"'"+ ' AND date_out = '+ "'"+str(pass_num[i][2])+"'")
            conn.commit()

def excursion(number):
    cursor.execute('SELECT "booking_num" FROM "booking" WHERE ("booking_num" = (SELECT MAX("booking_num") FROM "booking"))')
    records = cursor.fetchone()[0]
    if number == 1:
        cursor.execute('UPDATE "booking" SET "exc_class"= (%s) WHERE ("booking_num" = (%s))', (str(1), str(records)))
        conn.commit()
    if number == 2:
        cursor.execute('UPDATE "booking" SET "exc_class"= (%s) WHERE ("booking_num" = (%s))', (str(2), str(records)))
        conn.commit()
    if number == 3:
        cursor.execute('UPDATE "booking" SET "exc_class"= (%s) WHERE ("booking_num" = (%s))', (str(3), str(records)))
        conn.commit()

def auto(number):
    cursor.execute('SELECT "booking_num" FROM "booking" WHERE ("booking_num" = (SELECT MAX("booking_num") FROM "booking"))')
    records = cursor.fetchone()[0]
    if number == 1:
        cursor.execute('UPDATE "booking" SET "auto"= (%s) WHERE ("booking_num" = (%s))', (str(1), str(records)))
        conn.commit()
    if number == 2:
        cursor.execute('UPDATE "booking" SET "auto"= (%s) WHERE ("booking_num" = (%s))', (str(2), str(records)))
        conn.commit()
    if number == 3:
        cursor.execute('UPDATE "booking" SET "auto"= (%s) WHERE ("booking_num" = (%s))', (str(3), str(records)))
        conn.commit()

def cvit():
    cursor.execute('SELECT * FROM "payment" WHERE ("booking_num" = (SELECT MAX("booking_num") FROM "booking"))')
    records = list(cursor.fetchone())
    pass_num = records[3].strip()
    summ = records[4]
    day = datetime.date.today()
    day = day.strftime("%d %B %Y")
    contract = records[6]
    cursor.execute('SELECT f_name, l_name, o_name, phone FROM "guest" WHERE ("pass_num" = '+"'"+ str(pass_num)+"'"+ ')')
    guest = list(word_strip(cursor.fetchone()))
    fio = guest[0]+" "+guest[1]+" "+guest[2]
    phone = guest[3]
    # print(pass_num, sum, day, contract)
    # print(fio)
    # print(phone)
    return contract, fio, phone, summ, day

def rooms_adm():
    cursor.execute('SELECT "num_room" FROM "room"')
    all_rooms = cursor.fetchall()
    all_rooms = return_list(all_rooms)
    cursor.execute('SELECT num_room FROM "booking" WHERE "date_in" <=' + "'" +str(datetime.date.today())+ "'" +'AND "date_out" >='+"'"+ str(datetime.date.today()) +"'")
    busy_rooms = cursor.fetchall()
    busy_rooms = return_list(busy_rooms)
    res1 = [x for x in all_rooms if x not in busy_rooms]
    res2 = [x for x in all_rooms if x in busy_rooms]
    return res1, res2

def rooms_info(res):
    info = []
    for num in res:
        cursor.execute('SELECT * FROM "room" WHERE ("num_room" = '+"'"+ str(num)+"'"+ ')')
        room = list(word_strip(cursor.fetchone()))
        info.append(room)
    return info

def new_cost(service, cost):
    cursor.execute('UPDATE "services" SET "service_cost" =(%s) WHERE "service_name" = (%s)', (str(cost),str(service)))
    conn.commit()

def dopservices(contract, trans_in, trans_out, exc, food, fitness, bar):
    cursor.execute('UPDATE "booking" SET "trans_in"= (%s), "trans_out"= (%s), "exc"= (%s), "food"= (%s), "fitness"= (%s), "bar"= (%s) WHERE ("contract" = (%s))', (trans_in, trans_out, exc, food, fitness, bar, str(contract)))
    conn.commit()

def crash(num_room, crash_type, comment):
    cursor.execute('INSERT INTO "crash" (num_room, crash_type, comm, date, status) VALUES (%s, %s, %s, %s, %s)', (num_room, crash_type, comment, datetime.date.today(), "Не выполнен"))
    conn.commit()

def crash_rooms():
    cursor.execute('SELECT "num_room" FROM "room"')
    all_rooms = cursor.fetchall()
    all_rooms = return_list(all_rooms)
    cursor.execute('SELECT num_room FROM "crash" WHERE "status" =' + "'" +str("Не выполнен")+ "'" + ' OR "status" =' + "'" +str("В работе")+ "'")
    crash_rooms = cursor.fetchall()
    crash_rooms = return_list(crash_rooms)
    res = [x for x in all_rooms if x in crash_rooms]
    return res

def crash_status(num_room):
    cursor.execute('SELECT status, date, doer FROM "crash" WHERE ("num_room" = '+"'"+ str(num_room)+"'"+ ')')
    rec = cursor.fetchone()
    return rec

def get_crashes():
    cursor.execute('SELECT * FROM "crash" WHERE ("status" = '+"'"+str("Не выполнен")+"'"+")")
    records = cursor.fetchall()
    return records

def get_inwork_crashes():
    cursor.execute('SELECT * FROM "crash" WHERE ("status" = '+"'"+str("В работе")+"'"+")")
    records = cursor.fetchall()
    return records

def add_status_to_crash(answers, status1, status2):
    cursor.execute('SELECT * FROM "crash" WHERE ("status" = '+"'"+str(status1)+"'"+")")
    crash_num = cursor.fetchall()
    for i in range(len(answers)):
        if answers[i] == "Да":
            cursor.execute('UPDATE "crash" SET "status" = (%s) WHERE "crash_num" = (%s)', (status2, str(crash_num[i][0])))
            conn.commit()
        if answers[i] == "Нет":
            cursor.execute('DELETE from "crash" WHERE "crash_num" = ' + "'"+str(crash_num[i][0])+ "'")
            conn.commit()

def add_doer_to_crash(doers):
    cursor.execute('SELECT * FROM "crash" WHERE ("status" = '+"'"+str("Не выполнен")+"'"+")")
    crash_num = cursor.fetchall()
    print(crash_num)
    for i in range(len(crash_num)):
            cursor.execute('UPDATE "crash" SET "doer" = (%s) WHERE "crash_num" = (%s)', (doers[-1],str(crash_num[i][0])))
            conn.commit()

def doers():
    cursor.execute('SELECT "staff_name" FROM "staff"')
    records = cursor.fetchall()
    for i in records:
        i = list(i)
    return records

# add_doer_to_crash(['Федосеев Агафон Кимович', 'Горбунов Игнат Игоревич'])
# new_cost("Бар", 250)
# print(costs())
# res1, res2 = rooms_adm()
# print(rooms_info(res2))
# cvit()
# res = rooms_req("Эконом","1")
# for i in range(len(res)):
#     res[i] = word_strip(res[i])
# print(res)

# res = word_strip(guest_req(str(9218))[0])
# print(res)

# print(booking_req("Эконом", 1, "2019-06-11", "2019-06-18"))
# booking("Эконом", 1, 1, "2019-06-11", "2019-06-18", trans_in, trans_out, exc, food, fitness, bar, comm, num_room, booking_num, status, contract)
# print(in_guests())

# print(get_booking_for_pay(9218, 1))
# print(history(9218))
# print(bookings())
# info = [True, False]
# for i in range(len(info)):
#     info[i] = yes_no(info[i])
# print(info)