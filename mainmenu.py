
# Importing Libraries and Python Files
import pygame
import os
import sys
from button import Button


pygame.init()

# Global Constanst
SCREEN_HEIGHT = 620  # Screen Height of the game window
SCREEN_WIDTH = 1000  # Screen Width of the game window
# pygame.NOFRAME removes the task bar from the game window
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)

DinoBG = pygame.image.load(os.path.join("./Assets/Mainmenu", "DinoBG.png"))

if __name__ == "__main__":

    while True:
        SCREEN.blit(DinoBG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # EXIT_BUTTON = Button(image=pygame.image.load(
        #     os.path.join("./Assets/Titlebar", "times.png")), pos=(
        #     980, 20), text_input="", font="", base_color="#d7fcd4", hovering_color="White")

        PLAY_BUTTON = Button(image=pygame.image.load("./Assets/mainmenu/Options Rect.png"), pos=(500, 250),
                             text_input="Train Model", font="", base_color="#d7fcd4", hovering_color="Red")
        OPTIONS_BUTTON = Button(image=pygame.image.load("./Assets/mainmenu/Options Rect.png"), pos=(500, 400),
                                text_input="Test Model", font="", base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("./Assets/mainmenu/Quit Rect.png"), pos=(500, 550),
                             text_input="QUIT", font="", base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            # button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #     options()
                    pygame.quit()
                    sys.exit()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
