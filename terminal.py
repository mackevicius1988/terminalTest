import datetime

from MainController import mainController


def seconds_until_midnight():
    now = datetime.datetime.now()
    tomorrow = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
    return abs(tomorrow - now).seconds


if __name__ == '__main__':
    # Init configurations, raspi_id and screen
    raspi_id = mainController.init()
    mainController.connect_terminal(raspi_id)

    while 1:
        question_data = mainController.get_and_display_question(raspi_id)
        got_question = question_data is not None and question_data['questionMapId'] != ''

        while 1:
            layout = 0
            if question_data is not None:
                layout = len(question_data['answers'])

            if got_question:
                sleep = seconds_until_midnight()
            else:
                sleep = 60

            card_id, answer_id = mainController.wait_for_nfc_input(layout, sleep)

            if got_question is False and card_id is False:
                # No question, wait for the minute
                # time.sleep(60)
                # Back to question retrieval
                break

            if card_id is False:
                continue  # wait for another input

            break

        if got_question and card_id and answer_id:
            mainController.submit_answer(question_data, raspi_id, card_id, answer_id)
