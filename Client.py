from RPi.GPIO import GPIO
from MFRC522 import MFRC522
from ServerSpecs import ServerSpecs
import datetime
import signal
import time  # Ensure time is imported

# Clean up on exit
def end_program(signal, frame):
    print("\nCtrl+C captured, ending read.")
    GPIO.cleanup()
    exit()

# Set up signal handler
signal.signal(signal.SIGINT, end_program)

# Create an instance of the MFRC522 class
rfid = MFRC522.MFRC522()

server = ServerSpecs.get_xmlrpc_server_instance()

try:
    while True:
        # Scan for cards
        (status_card, tag_type) = rfid.MFRC522_Request(rfid.PICC_REQIDL)

        # If a card is found
        if status_card == rfid.MI_OK:
            current_date_time = datetime.datetime.now().isoformat()
            print("Card detected")

            # Get the ID of the card
            (status_id, uid) = rfid.MFRC522_Anticoll()

            # If we have the UID, print it
            if status_id == rfid.MI_OK:
                rfid_id = "".join([str(x) for x in uid])
                print("Card UID: " + rfid_id)

                # Send data to the XML-RPC server
                response = server.is_person_exists(rfid_id, current_date_time)

                if response != "Unknown RFID ID":
                    person_name = response
                    print(f"Name: {person_name}")
                # Optionally, prevent reading the same card multiple times
                time.sleep(1)
finally:
    GPIO.cleanup()