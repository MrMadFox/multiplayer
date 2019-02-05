import pygame,textinput
def name(display_text):
    screen = pygame.display.set_mode((700, 400))
    clock = pygame.time.Clock()
    pygame.init()
    text=textinput.TextInput(initial_string=display_text)
    while True:
        screen.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type==pygame.KEYDOWN:
                if event.key == 13:
                    return(text.input_string)

        # Feed it with events every frame
        text.update(events)
        # Blit its surface onto the screen
        screen.blit(text.get_surface(), (10, 10))
        pygame.display.update()
        clock.tick(30)