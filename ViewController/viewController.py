import pygame

totalWidth = 0;
totalHeight = 0;
margin = 10;
screen = None;
answersColors={0:(255,204,128),
               1:(255, 245, 157),
               2:(230,238,156),
               3:(174, 213, 129),
               4:(102,187,106)}


def init():
    global totalWidth, totalHeight, screen
    pygame.init()
    pygame.mouse.set_visible(False)
    info_object = pygame.display.Info()
    totalWidth = info_object.current_w
    totalHeight = info_object.current_h

    totalWidth = 1440
    totalHeight = 700
    screen = pygame.display.set_mode((totalWidth, totalHeight))

    # Init background
    bg = pygame.image.load("pt-terminal-bg.png")
    screen.blit(pygame.transform.scale(bg, (totalWidth, totalHeight)), (0, 0));
    pygame.display.update()
    print("Pygame initiated in " + str(totalWidth) + "x" + str(totalHeight))

def drawQuestion(question_text):
    global totalHeight, totalWidth, screen
    questionFontSize = totalWidth // 30;
    questionBlock = pygame.Rect((margin, margin, totalWidth - margin * 2,  totalHeight * 0.7))
    questionFont = pygame.font.Font("fonts/OpenSans-Light.ttf", questionFontSize)

    # 50 symbols is equal 1 line, REFACTOR IT
    question_text = prefix_question_text(question_text)

    question_rendered = render_text_rect(question_text, questionFont, questionBlock, (216, 216, 216), False, 1);
    screen.blit(question_rendered, questionBlock.topleft)
    pygame.display.update()

    # Show answers section
    words = []  # MOCK DATA
    words.append("Life")
    words.append("is")
    words.append("beatiful")
    words.append("with")
    words.append("PulseTip")

    for index in range(len(words)):
        block_width = totalWidth // 5;
        block_height = totalHeight * 0.3 - 3 * margin;
        answer_block = pygame.Rect(
            (block_width * index, totalHeight - block_height, block_width, block_height))
        answer_font = pygame.font.Font("fonts/OpenSans-Light.ttf", totalWidth // 45)
        print(index)
        answer_text = prefix_answer_text(words[index])
        answer_rendered = render_text_rect(answer_text, answer_font, answer_block, (0, 0, 0), answersColors[index], 1)
        screen.blit(answer_rendered, answer_block.topleft)

    pygame.display.update()


def prefix_answer_text(text):
    text = '\n' + text if text else ''
    return text


def prefix_question_text(text):
    size = 51
    if len(text) < size:
        question_text = "\n\n\n\n" + text
    elif len(text) in range(size, size * 2):
        text = "\n\n\n" + text
    elif len(text) in range(size * 2 + 1, size * 3):
        question_text = "\n\n" + text
    elif len(text) in range(size * 3 + 1, size * 4):
        question_text = "\n" + text
    return text


class text_rectException:
    def __init__(self, message=None):
        self.message = message
    def __str__(self):
        return self.message

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
                    raise(text_rectException, "The word " + word + " is too long to fit in the rect passed.")
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
                raise(text_rectException, "Invalid justification argument: " + str(justification))
        accumulated_height += font.size(line)[1]

    return surface