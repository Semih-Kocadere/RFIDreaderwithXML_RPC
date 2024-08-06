import xmlrpc.client
import RPi.GPIO as GPIO
import MFRC522
import signal
import spidev
import time
from datetime import datetime

url = 'urlForOdooServer'
db = 'db_name'
username = 'ik'
password = "1234"

redled_pin = 11
greenled_pin = 33
buzzer_pin = 13

continue_reading = True
GPIO.setmode(GPIO.BOARD)
GPIO.setup(redled_pin, GPIO.OUT)
GPIO.setup(greenled_pin, GPIO.OUT)
GPIO.setup(buzzer_pin, GPIO.OUT)


def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False


def buzzer(pin):
    GPIO.output(pin, GPIO.HIGH)
    print("Buzzer is working...")
    time.sleep(0.5)
    GPIO.output(pin, GPIO.LOW)


def redled(pin):
    GPIO.output(pin, GPIO.HIGH)
    print("Red led is working...")
    time.sleep(0.5)
    GPIO.output(pin, GPIO.LOW)


def greenled(pin):
    GPIO.output(pin, GPIO.HIGH)
    print("Green led is working...")
    time.sleep(0.5)
    GPIO.output(pin, GPIO.LOW)


# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print("Welcome to the MFRC522 data read example")
print("Press Ctrl-C to stop.")

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print("Card detected")

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        # Print UID
        rfid_id = "".join([str(x) for x in uid])
        # Connect to Odoo server

        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        common.version()
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        print(f"RFID ıd : {rfid_id}")
        # Check access rights

        models.execute_kw(db, uid, password, 'hr.attendance', 'check_access_rights', ['read'],
                          {'raise_exception': False})
        models.execute_kw(db, uid, password, 'hr.attendance', 'check_access_rights', ['create'],
                          {'raise_exception': False})
        models.execute_kw(db, uid, password, 'hr.attendance', 'check_access_rights', ['write'],
                          {'raise_exception': False})
        models.execute_kw(db, uid, password, 'hr.employee', 'check_access_rights', ['read'], {'raise_exception': False})

        employee_id = models.execute_kw(db, uid, password, 'hr.employee', 'search', [[['pin', '=', rfid_id]]])
        # if empleyee exist, check attendance
        if employee_id:
            check_attendance = models.execute_kw(db, uid, password, 'hr.attendance', 'search', [
                [["employee_id", "=", employee_id], ["check_in", "!=", False], ["check_out", "=", False]]],
                                                 {"limit": 1})
            # if check attendance exist, write check_out, else create attendance
            if check_attendance:
                write_attendance = models.execute_kw(db, uid, password, 'hr.attendance', 'write', [[check_attendance], {
                    "check_out": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}])
            else:
                create_attendance = models.execute_kw(db, uid, password, 'hr.attendance', 'create', [
                    {"employee_id": employee_id[0], "check_in": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}])

            print(b)
            greenled(greenled_pin)
        else:
            print("Undefined card.")
            redled(redled_pin)
            buzzer(buzzer_pin)
            time.sleep(1)