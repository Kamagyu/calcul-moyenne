import pygame

pygame.init()
pygame.display.set_caption("Calcul de moyenne")

width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
big_font = pygame.font.Font('freesansbold.ttf', 26)
small_font = pygame.font.Font('freesansbold.ttf', 19)
color_inactive = (36, 37, 51)
color_active = (97, 0, 238)
color_invalid = (208, 72, 72)
color_text_invalid = (93, 14, 65)
color_background = (49, 54, 63)
white = (255, 255, 255)
average = 0

class Subject:
    def __init__(self, name, coeff, mark):
        self.name = name
        self.coeff = coeff
        self.mark = mark

class InputBox:
    def __init__(self, value):
        self.value = value
        self.active = False
        self.valid = True

def empty_selection():
    for subject in subjects:
        subject.coeff.active = False
        subject.mark.active = False

def is_float(val):
    try:
        num = float(val)
    except ValueError:
        return False
    return True    

subjects = [
    Subject("Français", InputBox("1"), InputBox("10")),
    Subject("Mathématiques", InputBox("1"), InputBox("10")),
    Subject("SNT", InputBox("1"), InputBox("10")),
    Subject("Anglais", InputBox("1"), InputBox("10")),
    Subject("Espagnol", InputBox("1"), InputBox("10")),
    Subject("Histoire-géo", InputBox("1"), InputBox("10")),
    Subject("EPS", InputBox("1"), InputBox("10")),
    Subject("Physique-Chimie", InputBox("1"), InputBox("10")),
    Subject("SES", InputBox("1"), InputBox("10")),
    Subject("SVT", InputBox("1"), InputBox("10")),
    Subject("EMC", InputBox("1"), InputBox("10")),
]

titles = [
    big_font.render("Matières", True, white),
    big_font.render("Coefficients", True, white),
    big_font.render("Notes", True, white),
]


running = True
while running:

    input_text = ""
    do_delete = False

    # Handle events and text input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_BACKSPACE:
                do_delete = True
            else:
                input_text += event.unicode

    # Compute average
    sum =  [0, 0]
    for s in subjects:
        if is_float(s.coeff.value) and is_float(s.mark.value):
            sum[0] += int(s.coeff.value)*int(s.mark.value)
            sum[1] += int(s.coeff.value)
    if not sum[1] == 0:
        average = sum[0] / sum[1] 


    screen.fill(color_background)

    # Draw titles
    for i in range(len(titles)):
        pygame.draw.rect(screen, color_inactive, pygame.Rect(i*width/3 + 5, 5, width/3-5, height/20))
        screen.blit(titles[i], titles[i].get_rect(center=(i*width/3 + width/6, height/40+5)))

    # Draw average
    pygame.draw.rect(screen, color_inactive, pygame.Rect(5, 26*height/30 + 5, width/3-5, height/10))
    screen.blit(big_font.render("Moyenne :", True, white), big_font.render("Moyenne", True, white).get_rect(center=(width/6 - 5, 27*height/30 + 20)))
    screen.blit(big_font.render(str(average), True, white), big_font.render(str(average), True, white).get_rect(center=(2*width/4 - 5, 27*height/30 + 20)))
    
    for i in range(len(subjects)):
        subject = subjects[i]
        subject_render = small_font.render(subject.name, True, white)
        coeff_render = small_font.render(subject.coeff.value, True, white if subject.coeff.valid else color_text_invalid)
        mark_render = small_font.render(subject.mark.value, True, white if subject.mark.valid else color_text_invalid)
        mouse_pos = pygame.mouse.get_pos()

        # Draw subjects
        pygame.draw.rect(screen, color_inactive, pygame.Rect(5, height/14*(i+1) + 5, width/3 - 5, height/15))
        screen.blit(subject_render, subject_render.get_rect(center=(width/6, height/14*(i+1) + height/30+ 5)))


        # Draw coefficients rectangle

        if not is_float(subject.coeff.value):
            subject.coeff.valid = False
        else:
            subject.coeff.valid = True
    
        coeff_rect = pygame.draw.rect(screen, color_active if subject.coeff.active else (color_invalid if not subject.coeff.valid else color_inactive), pygame.Rect(width/3 + 5, height/14*(i+1) + 5, width/3 - 5, height/15))

        # Check collision for coefficients
        if coeff_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed(3)[0]:  
            empty_selection()
            subject.coeff.active = True

        # Input text to coefficient value
        if subject.coeff.active:
            if do_delete:
                subject.coeff.value = subject.coeff.value[:-1]
            else:
                subject.coeff.value += input_text
        
        # Draw coefficient value
        screen.blit(coeff_render, coeff_render.get_rect(center=(width/2, height/14*(i+1) + height/30 + 5)))


        # Draw marks rectangle

        if not is_float(subject.mark.value):
            subject.mark.valid = False
        else:
            subject.mark.valid = True

        mark_rect = pygame.draw.rect(screen, color_active if subject.mark.active else (color_invalid if not subject.mark.valid else color_inactive), pygame.Rect(2*width/3 + 5, height/14*(i+1) + 5, width/3 - 5, height/15))

        # Check collision for marks
        if mark_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed(3)[0]:
            empty_selection()
            subject.mark.active = True

        # Input text to mark value
        if subject.mark.active:
            if do_delete:
                subject.mark.value = subject.mark.value[:-1]
            else:
                subject.mark.value += input_text
        
        # Draw mark value
        screen.blit(mark_render, mark_render.get_rect(center=(5*width/6, height/14*(i+1) + height/30 + 5)))
        

    pygame.display.flip()

pygame.quit()
exit()