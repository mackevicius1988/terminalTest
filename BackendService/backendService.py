import requests, logging
import ConfigParser, os

backend_url = "http://dev.pulsetip.com/"
backend = 'app.pulsetip.com'
protocol = 'http'

config = ConfigParser.RawConfigParser()
config.read('terminal.conf')

if config.has_option('General', 'backend'):
    backend = config.get('General', 'backend')

if config.has_option('General', 'protocol'):
    protocol = config.get('General', 'protocol')

backend_url = protocol + '://' + backend


def get_question_data(raspi_id):
    try:
        url = backend_url + '/api/v1/answers/terminal/' + raspi_id
        resp = requests.get(url)
        logging.info("Got response from backend for get_question_data: " + resp.text)
        data = resp.json();
    except Exception as e:
        logging.error("ERROR: while calling backend.", e)
        raise Exception("ERROR: while calling backend. Check network connectivity!")

    if not data['success']:
        raise Exception(data['message'])

    return data


def connect_terminal(raspi_id):
    try:
        url = backend_url + "/api/v1/terminal/{0}".format(raspi_id)
        resp = requests.get(url)
        logging.info("Got response from backend fot connect_terminal: " + resp.text)
        data = resp.json();
    except Exception as e:
        logging.error("ERROR: while calling backend.", e)  # log excption
        raise Exception("ERROR: while calling backend. Check network connectivity!")

    return data


def register_terminal(raspi_id):
    logging.debug("Register terminal to backend: " + raspi_id)
    try:
        url = backend_url + "/api/v1/terminal/register/{0}".format(raspi_id)
        data = dict(raspi_id=raspi_id)
        resp = requests.post(url, data, allow_redirects=True)
        logging.info("Got response from backend for register_terminal: " + resp.text)
        data = resp.json();
    except Exception as e:
        logging.error("ERROR: while calling backend.", e)  # log excption
        raise Exception("ERROR: while calling backend. Check network connectivity!")

    return data


def get_question_stats(question_map_id):
    try:
        url = backend_url + 'api/v1/question_day_stats/' + str(question_map_id)
        resp = requests.get(url)
        logging.info("Got response from backend for get_question_stats: " + resp.text)
        data = resp.json();
    except Exception as e:
        logging.error("ERROR: while calling backend.", e)  # log excption
        raise Exception("ERROR: while calling backend. Check network connectivity!")

    return data


def submit_answer(raspi_id, cardId, questionMapId, questionId, answerId):
    url = backend_url + "api/v1/answers/terminal/{0}/{1}/{2}/{3}/{4}".format(raspi_id, cardId, questionMapId,
                                                                             questionId, answerId)
    data = dict({'submit': 'submit'})
    try:
        resp = requests.post(url, data)
        logging.debug("Response from answer submit: " + resp.text)
        ret = resp.json();
    except Exception as e:
        logging.error("ERROR: while calling backend.", e)  # log excption
        raise Exception("ERROR: while calling backend. Check network connectivity!")

    return ret
