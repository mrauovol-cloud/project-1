import pygame

pygame.init()
display = pygame.display.set_mode((800, 800))
image = pygame.image.load('images/player1.png')
image_rect = image.get_rect()
run = True
while run:
    display.blit(image, image_rect)
    for event in pygame.event.get():
        print(event.type, pygame.QUIT)
        if event.type == pygame.QUIT:
            run  = False
    if image_rect.colliderect(30, 1,10,20):
        print("hello")
    pygame.display.update()

pygame.quit()