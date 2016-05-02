import pygame, time, logging, serial

from ViewController import viewController
from BackendService import backendService
from NFCReader import nfcReader

logging.basicConfig(format='%(asctime)s %(message)s', filename='terminal.log', level=logging.DEBUG)

admin_cards = ["A1C43745", "E65C3745"]

def init():
    # TODO Read configuration
    # TODO Init snowflake
    # Init screen
    viewController.init()
    # Register terminal to backend
    raspi_id = "a5846b9b-9deb-4e5c-95bb-fe902d404212"  # 69 -> 2
    return raspi_id


def connect_terminal(raspi_id):
    trials_count = 0
    connection_data = None
    while not connection_data:
        try:
            connection_data = backendService.connect_terminal(raspi_id)
        except Exception as e:
            viewController.show_message(
                '\n\n\n Warning \n\nConnection to backend failed. Retrying... {0}'.format(trials_count))
            print("connect_terminal to backend: ")
            time.sleep(10)
            trials_count += 1
            if trials_count == 5:
                logging.error("ERROR: Can't connect to backend after 5 tries. Giving up...")
                viewController.show_message('\n\n\nERROR\n\nCan\'t connect to backend after 5 tries. Giving up...')
                time.sleep(5)
                raise SystemExit

    if connection_data['success'] == 'false':
        if connection_data['error'] == 'unregistered':
            viewController.show_message(
                '\n\n\n Unregistered\nTerminal is not registered to backend. \n\nREGISTERING...!')
            time.sleep(5)
            registration_data = backendService.register_terminal(raspi_id)
            if registration_data == 1:
                message = '\n\n\n\n Terminal successfully registered.\n\n Terminal ID: {0}\n\nPlace any card to restart terminal'.format(
                    raspi_id)
                viewController.show_message(message)
                time.sleep(10)

                #
                #  read_nfc(99999)


def get_and_display_question(raspi_id):
    question_data = None
    try:
        question_data = backendService.get_question_data(raspi_id)
    except Exception as e:
        viewController.show_error_message(e)

    if question_data is not None:
        viewController.draw_question(question_data)

    return question_data


def get_question_stats(question_map_id):
    stats_data = None
    try:
        stats_data = backendService.get_question_stats(question_map_id)
    except Exception as e:
        viewController.show_error_message(e)

    return stats_data


def get_and_show_question_stats(question_map_id, question_text, company_name, departament_name):
    question_stats = get_question_stats(question_map_id)
    if question_stats is not None:
        viewController.display_question_stats(company_name + '(' + departament_name + ')',
                                              question_text,
                                              question_stats)
    time.sleep(5)


def submit_answer(question_data, raspi_id, cardId, answerId):
    question_text = question_data['question']
    question_map_id = question_data['questionMapId']
    question_id = question_data['questionId']
    company_name = question_data['companyName']
    departament_name = question_data['departmentName']

    try:
        submit_data = backendService.submit_answer(raspi_id, cardId, question_map_id, question_id, answerId)
    except Exception as e:
        viewController.show_error_message(e)

    response_code = submit_data['code']

    if response_code == 400:
        # Say thanks for a while and show the stats
        viewController.show_message("You already answered")
        get_and_show_question_stats(question_map_id, question_text, company_name, departament_name)
    elif submit_data['code'] == 401:
        error_message = submit_data['message']
        viewController.show_message(error_message)
    else:
        # Just show the stats
        viewController.say_thanks()
        get_and_show_question_stats(question_map_id, question_text, company_name, departament_name)


def wait_for_nfc_input(timeout):
    card_id, answer_id = nfcReader.read_nfc(timeout)
    if card_id in admin_cards:
        viewController.show_message("Shutting down PulseTip terminal...")
        time.sleep(2)
        pygame.quit()
        raise SystemExit
    #elif got_question is False and card_id not in admin_cards:
     #   return False, False
    else:
        return card_id, answer_id