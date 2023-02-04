# Import and initialize the pygame library
import pygame
from time import sleep
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([1000, 700])

# Run until the user asks to quit
running = True

x = 245
y = 245
while running:

	# Did the user click the window close button?
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Fill the background with white
	screen.fill((255, 255, 255))

	# Draw line
	pygame.draw.line(screen, (0,0,0), (250,250), (650,250))

	# Draw circle 
	pygame.draw.circle(screen, (0, 0, 255), (250, 250), 20)
	# Draw circle 
	pygame.draw.circle(screen, (0, 0, 255), (650, 250), 20)

	pygame.draw.rect(screen, (255,100,100), pygame.Rect(x, y, 15, 10))
	if x<645:
		x += 10

	# Flip the display
	pygame.display.flip()

	sleep(0.1)

# Time to end the Game
pygame.quit()