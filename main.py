import pymysql

class OfficeBooking:
    def __init__(self, host, user, password, db):
        self.conn = pymysql.connect(db='Rooms_db', user='root', password='12345678', host='127.0.0.1', cursorclass=pymysql.cursors.DictCursor)

    def check_availability(self, office_number, start_time, end_time):
        """Проверяеи доступна ли бронь в выбранный период времени"""
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM OfficeBooking b WHERE  b.office_number = %s AND (start_time > %s AND end_time < %s)', (office_number, start_time, end_time))
        return cur.rowcount

    def book_office(self, person_id, office_number, start_time, end_time, occupier_name, occupier_email, occupier_phone):
        """Бронируем комнату и отправляем бронирующему письмо"""
        cur = self.conn.cursor()
        cur.execute('INSERT INTO OfficeBooking (person_id, office_number, start_time, end_time, occupied_name, occupied_email, occupied_phone) VALUES (%s, %s, %s, %s, %s, %s, %s)', (person_id, office_number, start_time, end_time, occupier_name, occupier_email, occupier_phone))
        self.conn.commit()

        self.send_notification(occupier_email, occupier_phone, office_number, start_time, end_time)

    def get_occupant(self, office_number, start_time, end_time):
        """Получаем информацию про заброннированную сессию."""
        cur = self.conn.cursor()
        cur.execute('SELECT * FROM OfficeBooking WHERE office_number = %s AND (start_time <= %s AND end_time >= %s)', (office_number, start_time, end_time))
        return cur.fetchone()

    def send_notification(self, occupier_name, occupier_phone, office_number, start_time, end_time):
        """Отправляем письмо на почту и телефон бронирующему"""
        # Необходимо реализовать функцию, используя API электронной почты или API обмена сообщениями. 
        # Оставил простой print().
        # Но если требуется и это, могу добавить.
        print(f"Комната {office_number} зарезервированна за {occupier_name}, с {start_time} до {end_time}")

    def do_all(self, person_id, office_number, start_time, end_time, occupier_name, occupier_email, occupier_phone):

        availability = self.check_availability(office_number, start_time, end_time)
        if availability != 0:
            self.get_occupant(office_number, start_time, end_time)
            self.send_notification(occupier_email, occupier_phone, office_number, start_time, end_time)
        else:
            self.book_office(person_id, office_number, start_time, end_time, occupier_name, occupier_email, occupier_phone)
