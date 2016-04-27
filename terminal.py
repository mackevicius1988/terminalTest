import pygame, time, requests
from ViewController import viewController






def get_question_data():
    #raspId
    resp = requests.get('http://dev.pulsetip.com/api/v1/answers/terminal/13212')
    data = resp.json();
    return data['questionId'], data['questionMapId'], data['question'], data['answers'], data['departmentName'], data[
        'companyName']


if __name__ == '__main__':
    viewController.init()
    while 1:
        # Connect to backend for refgistartion
        # GetQuestion and retrieve itfd
        # Retrieve the question and drawit
        questionId, questionMapId, questionText, answers, departmentName, companyName = get_question_data()
        viewController.draw_question(questionText, answers)

        #wait for the answer question

        # Draw stats


        event = pygame.event.wait()
        if event.type == 2:
            viewController.say_thanks()
            time.sleep(float(1))
            response = requests.get('http://dev.pulsetip.com/api/v1/question_day_stats/1231')
            answers = response.json();
            # add questionMapId
            viewController.display_question_stats(companyName + '(' + departmentName + ')', questionText, answers)
            time.sleep(float(5))






