import pygame, time, logging, serial

from MainController import mainController

if __name__ == '__main__':
    # Init configurations, raspi_id and screen
    raspi_id = mainController.init()
    mainController.connect_terminal(raspi_id)

    while 1:
        question_data = mainController.get_and_display_question(raspi_id)
        got_question = question_data['questionMapId'] != ''

        if got_question is False:
            # No question, wait for the minute
            time.sleep(600)
            # Back to question retrieval
            continue
        layout = len(question_data['answers'])
        while 1:
            card_id, answer_id = mainController.wait_for_nfc_input(layout, 60)
            if card_id is False:
                continue # wait for another input

            break

        if card_id and answer_id:
            mainController.submit_answer(question_data, raspi_id, card_id, answer_id)
