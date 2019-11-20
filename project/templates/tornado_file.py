import os
 
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
 
from tornado.options import define, options

import functions as func
import datetime

answers = []
doers = []
answ = []

define("port", default=8888, help="run on the given port", type=int)
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", RootHandler),("/booking", BookingHandler), ("/guest", GuestHandler), ("/vhod", VhodHandler), ("/allguests", AllGuestsHandler), 
        ("/inguests", InGuestsHandler), ("/pay", PayHandler), ("/payment", PaymentHandler), ("/confirm", ConfirmHandler), 
        ("/confirmation", ConfirmationHandler),("/Econom",EconomHandler),("/Standart",StandartHandler),("/Komfort",KomfortHandler),
        ("/Luks",EconomHandler),("/President",PresidentHandler), ("/basic_excursion", ExcBasicHandler), ("/sred_excursion", ExcSredHandler), 
        ("/pov_excursion", ExcPovHandler), ("/excursion", ExcursionHandler),("/autoion", AutoionHandler), ("/basic_auto", AutoBasicHandler), 
        ("/sred_auto", AutoSredHandler), ("/pov_auto", AutoPovHandler),("/admin",AdminHandler), ("/statistic",StatHandler), ("/cvit", CvitHandler),
        ("/allrooms", AllRoomsHandler), ("/busyrooms", BusyRoomsHandler), ("/services", ServicesHandler), ("/dopservices", DopServicesHandler),
        ("/crash", CrashHandler), ("/crashrooms", CrashRoomsHandler), ("/crashroomstech", CrashRoomsHandler), ("/crashconfirm", CrashConfirmHandler), 
        ("/crashconfirmation", CrashConfirmationHandler), ("/pri", CrashAcceptionHandler), ("/priem", CrashAceptHandler)]
        settings = {
            "debug": True,
            "template_path": os.path.join('C:\\Users\\user\\Desktop\\project', "templates"),
            "static_path": os.path.join('C:\\Users\\user\\Desktop\\project', "static")
                
        }
        tornado.web.Application.__init__(self, handlers, **settings)

class StatHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('Statistic.html')

class AutoionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('auto.html')

    def post(self):
        info = func.get_last_booking()
        for i in range(len(info)):
            info[i] = func.yes_no(info[i])
        self.render("guest.html", info = info)

class PresidentHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('President.html')

class LuksHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('Luks.html')

class KomfortHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('Komfort.html')

class StandartHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('Standart.html')

class EconomHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('Econom.html')
        
class RootHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class BookingHandler(tornado.web.RequestHandler):
    def get(self):
        cost = func.costs()
        self.render('booking.html', occupied = " ", cost = cost)
    
    def post(self):
        date_in = self.get_argument("date_in")
        date_out = self.get_argument("date_out")
        type_room = self.get_argument("type_room")
        guest_num = self.get_argument("guest_num")
        room_num = self.get_argument("room_num")
        comm = self.get_argument("comm")
        # print(comm)
        trans_in = func.on_off(self.get_argument("trans_in"))
        trans_out = func.on_off(self.get_argument("trans_out"))
        exc = func.on_off(self.get_argument("exc"))
        food = func.on_off(self.get_argument("food"))
        fitness = func.on_off(self.get_argument("fitness"))
        bar = func.on_off(self.get_argument("bar"))
        res1 = func.rooms_req(type_room, room_num) 
        res2 = func.booking_req(type_room, room_num, date_in, date_out)
        res = [x for x in res1 if x not in res2]
        if res != []:
            num_room = res[0]
            func.booking(type_room, guest_num, room_num, date_in, date_out, trans_in, trans_out, exc, food, fitness, bar, comm, num_room)
            # info = func.get_last_booking()
            # for i in range(len(info)):
            #     info[i] = func.yes_no(info[i])
            # # self.render("guest.html", info = info)
            self.render("ekskur.html")
        else: 
            self.render('booking.html', occupied = "Все номера заняты", cost = "")

class GuestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('guest.html', info = "")
    
    def post(self):
        pass_num = self.get_argument("pass_num")
        f_name = self.get_argument("f_name")
        l_name = self.get_argument("l_name")
        o_name = self.get_argument("o_name")
        gender = self.get_argument("gender")
        phone = self.get_argument("phone")
        email = self.get_argument("email")
        res = func.guest_req(pass_num) 
        if res != []:
            func.history_add(pass_num)
        else:
            func.guest(pass_num, f_name, l_name, o_name, gender, phone, email)
        func.guest_add(pass_num)
        self.render("thankyou.html")
        # print(pass_num, f_name, l_name, o_name, phone, email)

class AdminHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('admin.html')

class VhodHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('vhod.html')

    def post(self):
        login = self.get_argument("login")
        password = self.get_argument("password")
        try:
            user = func.autorize(login, password)[0].strip()
            if user == "admin":
                self.render("admin.html")
            if user == "tech_admin":
                self.render("tech_admin.html")
        except Exception as e:
            print(e)
            self.render("error.html")

class AllGuestsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('guests.html', records = "")
    
    def post(self):
        records = func.all_guests()
        # print(records)
        try:
            self.render('guests.html', records = records)
        except Exception as e:
            print(e)
            self.render('error1.html')

class InGuestsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('guests.html', records = "")
    
    def post(self):
        records = func.in_guests()
        # print(records)
        try:
            self.render('guests.html', records = records)
        except Exception as e:
            print(e)
            self.render('error1.html')

class PayHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('pay.html')
    
    def post(self):
        # self.render('pay.html')
        contract = self.get_argument("contract")
        print("HERE")
        try:
            info = func.get_booking_for_pay(contract)
            cost = func.costs()
            # print(cost)
            print("HERE")
            for i in range(len(info)):
                info[i] = func.yes_no(info[i])
                if info[i] == None:
                    info[i] = 0
            # print(info)
            type_room = info[0]
            date_in = info[3]
            date_out = info[4]
            trans_in = info[5]
            trans_out = info[6]
            exc = info[7]
            food = info[8]
            fitness = info[9]
            bar = info[10]
            num_room = info[11]
            booking_num = info[12]
            exc_class = info[13]
            auto = info[14]
            pass_num = info[15]
            days = (date_out - date_in).days
            sum_room, pay_punkts = func.payment(pass_num, type_room, days, trans_in, trans_out, exc, food, fitness, bar, exc_class, auto)
            hist = func.history(pass_num)
            func.payment_insert(booking_num, num_room, days, pass_num, sum_room, datetime.date.today(), contract)
            self.render('payment.html', info = info, sum = sum_room, history = hist, pay = pay_punkts, cost = cost)
        except Exception as e:
            print(e)
            self.render('error.html')

class PaymentHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("thankyoupay.html")

class ConfirmationHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("confirm.html", rec = "", number = "")
    
    def post(self):
        self.redirect("/confirm?number=0")

class ConfirmHandler(tornado.web.RequestHandler):
    def get(self):
        records = func.bookings()
        number = self.get_argument('number')
        for i in range(len(records)):
            records[i] = list(records[i])
            for j in range(len(records[i])):
                records[i][j] = func.yes_no(records[i][j])
        # print(records)
        try:
            self.render("confirm.html", rec = records[int(number)], number = str(int(number) + 1))
        except Exception as e:
            print(e)
            self.render('error2.html')

    def post(self):
        records = func.bookings()
        rec = []
        answer = self.get_argument("answer")
        answers.append(answer)
        # print(answers)
        if len(answers) < len(records):
            number = self.get_argument('number')
            self.render("confirm.html", rec = records[int(number)], number = str(int(number) + 1))
        else:
            self.render("admin.html")
            func.add_status_to_booking(answers)

class ExcursionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ekskur.html")

class ExcBasicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ekskur.html")

    def post(self):
        func.excursion(1)
        self.render("auto.html")

class ExcSredHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ekskur.html")

    def post(self):
        func.excursion(2)
        self.render("auto.html")

class ExcPovHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("ekskur.html")

    def post(self):
        func.excursion(3)
        self.render("auto.html")

class AutoBasicHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("auto.html")

    def post(self):
        func.auto(1)
        info = func.get_last_booking()
        for i in range(len(info)):
            info[i] = func.yes_no(info[i])
        self.render("guest.html", info = info)

class AutoSredHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("auto.html")

    def post(self):
        func.auto(2)
        info = func.get_last_booking()
        for i in range(len(info)):
            info[i] = func.yes_no(info[i])
        self.render("guest.html", info = info)

class AutoPovHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("auto.html")

    def post(self):
        func.auto(3)
        info = func.get_last_booking()
        for i in range(len(info)):
            info[i] = func.yes_no(info[i])
        self.render("guest.html", info = info)

class CvitHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("thankyoupay.html")

    def post(self):
        contract, fio, phone, summ, day = func.cvit()
        self.render("cvit.html", contract = contract, fio = fio, phone = phone, sum = summ, day = day)

class AllRoomsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("rooms.html", records = "", status = "", len = "")

    def post(self):
        res1, res2 = func.rooms_adm()
        records = func.rooms_info(res1)
        self.render("rooms.html", records = records, status = "свободен", len = len(records))

class BusyRoomsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("rooms.html", records = "", status = "", len = "")
    
    def post(self):
        res1, res2 = func.rooms_adm()
        records = func.rooms_info(res2)
        self.render("rooms.html", records = records, status = "занят", len = len(records))

class ServicesHandler(tornado.web.RequestHandler):
    def get(self):
        cost = func.costs()
        self.render("services.html", cost = cost)

    def post(self):
        new_cost = self.get_argument("cost")
        # print(new_cost)
        service = self.get_argument("service")
        # print(service)
        func.new_cost(service, new_cost)
        cost = func.costs()
        self.render("services.html", cost = cost)

class DopServicesHandler(tornado.web.RequestHandler):
    def get(self):
        cost = func.costs()
        self.render("dopservices.html", cost = cost)

    def post(self):
        contract = self.get_argument("contract")
        trans_in = func.on_off(self.get_argument("trans_in"))
        trans_out = func.on_off(self.get_argument("trans_out"))
        exc = func.on_off(self.get_argument("exc"))
        food = func.on_off(self.get_argument("food"))
        fitness = func.on_off(self.get_argument("fitness"))
        bar = func.on_off(self.get_argument("bar"))
        func.dopservices(contract, trans_in, trans_out, exc, food, fitness, bar)
        self.render("thankyoudop.html")

class CrashHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("crash.html")

    def post(self):
        num_room = self.get_argument("num_room")
        crash_type = self.get_argument("crash_type")
        comment = self.get_argument("comment")
        # print(num_room, crash_type, comment)
        func.crash(num_room, crash_type, comment)
        self.render("admin.html")

class CrashRoomsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("crash_rooms.html", records = "", status = "", len = "")

    def post(self):
        res = func.crash_rooms()
        records = func.rooms_info(res)
        for i in records:
            stat = list(func.crash_status(i[0]))
            # print(stat)
            i.append(stat[0])
            i.append(stat[1])
            i.append(stat[2])
        self.render("crash_rooms.html", records = records, status = "c неисправностями", len = len(records))

class CrashConfirmationHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("crashconfirm.html", rec = "", number = "")
    
    def post(self):
        self.redirect("/crashconfirm?number=0")

class CrashConfirmHandler(tornado.web.RequestHandler):
    def get(self):
        records = func.get_crashes()
        number = self.get_argument('number')
        for i in range(len(records)):
            records[i] = list(records[i])
            records[i][2] = records[i][2].strip()
            records[i][3] = records[i][3].strip()
            records[i][5] = records[i][5].strip()
        # print(records)
        # print(records[int(number)+1])
        doers = func.doers()
        print(doers)
        try:
            self.render("crashconfirm.html", rec = records[int(number)], number = str(int(number) + 1), records = doers)
        except Exception as e:
            print(e)
            self.render('error3.html')

    def post(self):
        rec = func.get_crashes()
        answer = self.get_argument("answer")
        doer = self.get_argument("doer")
        doers.append(doer)
        func.add_doer_to_crash(doers)
        answ.append(answer)
        records = func.doers()
        print(doers)
        if len(answ) < len(rec):
            number = self.get_argument('number')
            self.render("crashconfirm.html", rec = rec[int(number)], number = str(int(number) + 1), records = records)
        else:
            self.render("error3.html")
            func.add_status_to_crash(answ, "Не выполнен" ,"В работе")

class CrashRoomsTechHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("crash_rooms_tech.html", records = "", status = "", len = "")

    def post(self):
        res = func.crash_rooms()
        records = func.rooms_info(res)
        for i in records:
            stat = list(func.crash_status(i[0]))
            # print(stat)
            i.append(stat[0])
            i.append(stat[1])
        self.render("crash_rooms_tech.html", records = records, status = "c неисправностями", len = len(records))

class CrashAcceptionHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("priem.html", rec = "", number = "")
    
    def post(self):
        self.redirect("/priem?number=0")

class CrashAceptHandler(tornado.web.RequestHandler):
    def get(self):
        records = func.get_inwork_crashes()
        number = self.get_argument('number')
        for i in range(len(records)):
            records[i] = list(records[i])
            records[i][2] = records[i][2].strip()
            records[i][3] = records[i][3].strip()
            records[i][5] = records[i][5].strip()
        try:
            self.render("priem.html", rec = records[int(number)], number = str(int(number) + 1))
        except Exception as e:
            print(e)
            self.render('error3.html')

    def post(self):
        rec = func.get_inwork_crashes()
        answer = self.get_argument("answer")
        answ.append(answer)
        if len(answ) < len(rec):
            number = self.get_argument('number')
            self.render("priem.html", rec = rec[int(number)], number = str(int(number) + 1))
        else:
            self.render("error3.html")
            func.add_status_to_crash(answ, "В работе","Выполнен")

def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()