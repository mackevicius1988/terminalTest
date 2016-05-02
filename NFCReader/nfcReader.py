# Class responsible for readeing nfc card
import serial

reverse_readers = True


def read_nfc(timeout=60):
    ser = serial.Serial("/dev/ttyAMA0", 38400, timeout=timeout)
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
