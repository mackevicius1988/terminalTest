# Class responsible for readeing nfc card
import serial
import ConfigParser, os

reverse_readers = False
serial_dev = '/dev/ttyAMA0'
serial_baud_rate = 38400

print("Reading configurations file")
config = ConfigParser.RawConfigParser()
config.read('terminal.conf')

if config.has_option('General', 'serial_dev'):
    serial_dev = config.get('General', 'serial_dev')

if config.has_option('General', 'serial_baud_rate'):
    serial_baud_rate = config.get('General', 'serial_baud_rate')
if config.get('General', 'reverse_readers') == 'True' or config.get('General', 'reverse_readers') == 1:
    reverse_readers = True
else:
    reverse_readers = False


def read_nfc(timeout=60):
    ser = serial.Serial(serial_dev, serial_baud_rate, timeout=timeout)
    # Activate NFC readers
    ser.write("\r")
    serResponse = ser.readline()[:-2]
    if serResponse:
        print("Got NFC Response: " + serResponse)
        # print("Got NFC Response: " + serResponse)
        # sys.stdout.flush()
        answer_id = serResponse[:2][1:]
        answer_id = int(answer_id) + 1
        if reverse_readers is True: answer_id = 6 - int(answer_id)
        card_id = serResponse[3:]

        if card_id == 'False': return False, False
        return card_id, answer_id
    else:
        return False, False
