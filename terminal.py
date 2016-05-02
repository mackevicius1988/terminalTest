import pygame, time, logging, serial

from MainController import mainController

if __name__ == '__main__':
    # Init configurations, raspi_id and screen
    raspi_id = mainController.init()
    mainController.connect_terminal(raspi_id)

    while 1:
        question_data = mainController.get_and_display_question(raspi_id)
        #if question_data['questionMapId'] is None:
         #   continue

        got_question = question_data['questionMapId'] != ''

        while 1:
            print(got_question)

            cardId, answerId = mainController.wait_for_nfc_input(got_question);

            if cardId and answerId:
                mainController.submit_answer(question_data, raspi_id, cardId, answerId)
            else:
                continue


