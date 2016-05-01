import pygame, logging

totalWidth = 0;
totalHeight = 0;
margin = 10;
screen = None;
answersColors = {0: (255, 204, 128),
                 1: (255, 245, 157),
                 2: (230, 238, 156),
                 3: (174, 213, 129),
                 4: (102, 187, 106)}

answersPositionsMap = {1: [2],
                       2: [1, 3],
                       3: [0, 2, 4],
                       4: [0, 1, 3, 4],
                       5: [0, 1, 2, 3, 4]}


def init():
    global totalWidth, totalHeight, screen
    pygame.init()
    pygame.mouse.set_visible(False)
    info_object = pygame.display.Info()
    totalWidth = info_object.current_w
    totalHeight = info_object.current_h

    #totalWidth = 1024
    #totalHeight = 900

    screen = pygame.display.set_mode((totalWidth, totalHeight))
    print("Pygame initiated in " + str(totalWidth) + "x" + str(totalHeight))


def draw_question(question_data):
    # Init local variables
    global totalHeight, totalWidth, screen
    question_text = question_data['question']
    answers = question_data['answers']

    # Init background
    bg = pygame.image.load("pt-terminal-bg.png")
    screen.blit(pygame.transform.scale(bg, (totalWidth, totalHeight)), (0, 0));
    pygame.display.update()

    question_font_size = totalWidth // 30;
    questionBlock = pygame.Rect((margin, margin, totalWidth - margin * 2, totalHeight * 0.7))
    questionFont = pygame.font.Font("fonts/OpenSans-Light.ttf", question_font_size)

    # 50 symbols is equal 1 line, REFACTOR IT
    question_text = prefix_question_text(question_text)
    question_rendered = render_text_rect(question_text, questionFont, questionBlock, (216, 216, 216), False, 1);
    screen.blit(question_rendered, questionBlock.topleft)
    pygame.display.update()

    layout = len(answers);
    if layout != 0:
        position_indexes = answersPositionsMap[layout]
        for index in range(len(answers)):
            answer = answers[index]
            answer_text = answers[index]
            position = position_indexes[index]
            block_width = round(totalWidth * 0.2);  # 20 percents horizontaly of the screen
            block_height = totalHeight * 0.3;  # 30 percents verticaly of the screen
            answer_block = pygame.Rect((block_width * position, totalHeight - block_height, block_width, block_height))
            answer_font_size = int(totalWidth // 60 - (float(len(answer_text)) / 100 + 1))

            answer_font = pygame.font.Font("fonts/OpenSans-Light.ttf", answer_font_size)
            answer_text = prefix_answer_text(answer_text)
            answer_rendered = render_text_rect(answer_text, answer_font, answer_block, (0, 0, 0),
                                               answersColors[position], 1)
            screen.blit(answer_rendered, answer_block.topleft)

    pygame.display.update()


def show_message(message):
    message = prefix_question_text(str(message))
    bg = pygame.image.load("pt-terminal-bg.png")
    screen.blit(pygame.transform.scale(bg, (totalWidth, totalHeight)), (0, 0));
    font = pygame.font.Font("fonts/OpenSans-Light.ttf", totalWidth // 30)
    text_block = pygame.Rect((margin, margin, totalWidth - margin * 2, totalHeight * 0.7))
    text_rendered = render_text_rect(message, font, text_block, (255, 255, 255), False, 1)
    #text_rendered = drawText(message, font, text_block, (255, 255, 255), False, 1)
    screen.blit(text_rendered, text_block.topleft)
    pygame.display.update()


def say_thanks():
    show_message("Thank you!")


def show_error_message(exception):
    show_message(str(exception))


def display_question_stats(department, question_text, answers):
    bg = pygame.image.load("pt-terminal-bg.png")
    screen.blit(pygame.transform.scale(bg, (totalWidth, totalHeight)), (0, 0));

    top_block_height = int(round(totalHeight * 0.21))
    top_block = pygame.Surface((totalWidth, top_block_height), pygame.SRCALPHA, 32)

    company_logo = pygame.image.load("company_logo.svg")
    company_logo = pygame.transform.scale(company_logo, (30, 30))
    top_block.blit(company_logo, (totalWidth * 0.02, top_block_height * 0.3))

    department_label_font = pygame.font.Font("fonts/OpenSans-Light.ttf", totalWidth // 60)
    department_label = department_label_font.render(department, 1, (255, 255, 255))
    top_block.blit(department_label, (totalWidth * 0.02 + company_logo.get_rect().size[0] + 5, top_block_height * 0.3))

    question_label_font = pygame.font.Font("fonts/OpenSans-Light.ttf", totalWidth // 60)
    # question_label = question_label_font.render(question_text, 1, (255, 255, 255))

    question_label = render_text_rect(question_text, question_label_font, top_block.get_rect(), (255, 255, 255), False,
                                      0)
    screen.blit(question_label, (totalWidth * 0.02, top_block_height * 0.7))

    screen.blit(top_block, (0, 0))

    answer_block_height = totalHeight * 0.7;

    accumulated_x = 0
    layout = len(answers);
    if layout != 0:
        position_indexes = answersPositionsMap[layout]
        for index in range(len(answers)):
            print(index)
            answer = answers[index]
            percent = answer['percent']
            position = position_indexes[index]

            answer_block_width = totalWidth / 100 * int(percent)
            answer_block = pygame.Surface((round(answer_block_width), round(totalHeight * 0.7)))
            answer_block.fill(answersColors[position])

            percent_text_font_size = int(round(totalHeight * 0.06))
            percent_text_font = pygame.font.Font("fonts/OpenSans-Light.ttf", percent_text_font_size)
            percent_text_block = percent_text_font.render(str(percent) + "%", True, (51, 51, 51))
            midpoint = answer_block_width / 2 - percent_text_block.get_width() / 2;
            answer_block.blit(percent_text_block, (midpoint, 20))

            if answer['answer'] is not None:
                answer_text = answer['answer']
            else:
                answer_text = ""

            if len(answer_text) > 55:
                answer_text = answer_text[:52] + "..."

            answer_text_font_size = int(totalWidth // 60 - (float(len(answer_text)) / 100 + 1))
            # answer_text_font_size = int(round(totalHeight * 0.06))
            answer_text_font = pygame.font.Font("fonts/OpenSans-Light.ttf", answer_text_font_size)
            answer_text_block = answer_text_font.render(answer_text, True, (51, 51, 51))
            answer_text_block = pygame.transform.rotate(answer_text_block, 90)

            answer_rect = answer_block.get_rect()
            answer_text_block_y = answer_rect.bottom - answer_text_block.get_height() - 30;
            answer_block.blit(answer_text_block, (answer_rect.left, answer_text_block_y))

            screen.blit(answer_block, (accumulated_x, totalHeight * 0.3))
            accumulated_x += answer_block_width

    pygame.display.update()


def prefix_answer_text(text):
    text = '\n' + text if text else ''
    return text


def prefix_question_text(text):
    size = 51
    if len(text) < size:
        text = "\n\n\n\n\n" + text
    elif len(text) in range(size, size * 2):
        text = "\n\n\n\n" + text
    elif len(text) in range(size * 2 + 1, size * 3):
        text = "\n\n\n" + text
    elif len(text) in range(size * 3 + 1, size * 4):
        text = "\n\n" + text
    return text


class text_rectException:
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message
# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text

def render_text_rect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a text_rectException if the text won't fit onto the surface.
    """

    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise (text_rectException, "The word " + word + " is too long to fit in the rect passed.")
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size, pygame.SRCALPHA, 32)
    surface.convert_alpha()

    if background_color is not False: surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise (text_rectException, "Once word-wrapped, the text string was too tall to fit in the rect.")
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise (text_rectException, "Invalid justification argument: " + str(justification))
        accumulated_height += font.size(line)[1]

    return surface
