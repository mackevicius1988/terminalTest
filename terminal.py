print("Reading configuration file")

# Read configurationsss
import pygame


from ViewController import viewController

if __name__ == '__main__':
    # Init display START
    viewController.init()



    while 1:
        # Connect to backend for refgistartion
        # GetQuestion and retrieve itfd
        # Retrieve the question and drawit
        viewController.drawQuestion("Bla bla bla bla?")

        #wait for the answer question

        # Draw stats
        event = pygame.event.wait()
        if event.type == 2:
            raise SystemExit





