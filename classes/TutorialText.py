import pygame

class TutorialText(pygame.sprite.Sprite):
    def __init__(self, text, position) -> None:
        super().__init__()
        self.font = pygame.font.Font("./fonts/PixeloidSans-Bold.ttf", 28)
        self.image = self.font.render(text, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.move_ip(position)
        self.visible = True
        self.text = text

    def update(self):
        if self.text == "Main objective completed land here":
            from classes.GameWorld import GameWorld
            if GameWorld().main_objective_completed:
                self.visible = True
            else:
                self.visible = False

    def draw(self, screen):
        if self.visible:
            screen.blit(self.image, self.rect)