import pygame, time, logging, snowflake
import ConfigParser, os
from ViewController import viewController
from BackendService import backendService
from NFCReader import nfcReader

logging.basicConfig(format='%(asctime)s %(message)s', filename='terminal.log', level=logging.DEBUG)

stats_timeout = 5
admin_cards = ["", ""]


def read_configurations():
    global stats_timeout, admin_cards
    print("Reading configurations file")
    config = ConfigParser.RawConfigParser()
    config.read('terminal.conf')

    if config.has_option('General', 'serial_dev'):
        serial_dev = config.get('General', 'serial_dev')

    if config.has_option('General', 'serial_baud_rate'):
        serial_baud_rate = config.get('General', 'serial_baud_rate')

    if config.has_option('General', 'stats_timeout'):
        stats_timeout = config.get('General', 'stats_timeout')

    if not config.has_option('General', 'admin_card1'):
        print("Admin cards not set. \nRegister primary admin card by touching any reader")
        card_id = nfcReader.read_nfc(9999)
        config.set('General', 'admin_card1', card_id[0])
        with open('terminal.conf', 'wb') as configfile:
            config.write(configfile)
        print("Primary admin card registered")
    admin_card1 = config.get('General', 'admin_card1')

    time.sleep(3)

    if not config.has_option('General', 'admin_card2'):
        print("Secondary admin cards is not set. \nRegister secondary admin card by touching any reader")
        card_id = nfcReader.read_nfc(9999)
        config.set('General', 'admin_card2', card_id[0])
        with open('terminal.conf', 'wb') as configfile:
            config.write(configfile)
        print("Secondary admin card registered")
    admin_card2 = config.get('General', 'admin_card2')

    admin_cards = (admin_card1, admin_card2)


def get_or_generate_raspi_id():
    if not snowflake.snowflake(snowflake_file='.raspi_id'):
        print("RASPI ID not found. Looks like it's a new install. Generating RASPI ID...")
        try:
            snowflake.make_snowflake(snowflake_file='.raspi_id')
        except Exception as e:
            raise ("Failed to create raspi_id. Check if you have write permission on filesystem")
    return snowflake.snowflake(snowflake_file='.raspi_id')


def init():
    # Read configurations
    read_configurations()
    # Init screen
    viewController.init()
    # Register terminal to backend
    raspi_id = get_or_generate_raspi_id()  # 69 -> 2
    print(raspi_id)
    return raspi_id


def connect_terminal(raspi_id):
    trials_count = 0
    connection_data = None
    while not connection_data:
        try:
            connection_data = backendService.connect_terminal(raspi_id)
        except Exception as e:
            viewController.show_message(
                'Warning \n\nConnection to backend failed. Retrying... {0}'.format(trials_count))
            print("connect_terminal to backend: ")
            time.sleep(10)
            trials_count += 1
            if trials_count == 5:
                logging.error("ERROR: Can't connect to backend after 5 tries. Giving up...")
                viewController.show_message('ERROR\n\nCan\'t connect to backend after 5 tries. Giving up...')
                time.sleep(5)
                raise SystemExit

    if connection_data['success'] == 'false':
        if connection_data['error'] == 'unregistered':
            viewController.show_message(
                'Unregistered\nTerminal is not registered to backend. \n\nREGISTERING...!')
            time.sleep(5)
            registration_data = backendService.register_terminal(raspi_id)
            if registration_data == 1:
                message = 'Terminal successfully registered.\n\n Terminal ID: {0}\n\nPlace any card to restart terminal'.format(
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
        viewController.say_thanks()
        submit_data = backendService.submit_answer(raspi_id, cardId, question_map_id, question_id, answerId)
    except Exception as e:
        viewController.show_error_message(e)

    if submit_data is not None:
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
            get_and_show_question_stats(question_map_id, question_text, company_name, departament_name)


def wait_for_nfc_input(layout, timeout):
    card_id, answer_id = nfcReader.read_nfc(timeout)

    if card_id in admin_cards:
        viewController.show_message("Shutting down PulseTip terminal...")
        time.sleep(2)
        pygame.quit()
        raise SystemExit

    else:
        if layout == 4:
            if answer_id == 3:
                return False, False
        elif layout == 3:
            if answer_id in (2, 4):
                return False, False
        elif layout == 2:
            if answer_id in (2, 3, 4):
                return False, False

    return card_id, answer_id
