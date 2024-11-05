#April 2023
import pygame
from random import randint, choice
pygame.init()

FPS = 60
#start
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1150, 469))
pygame.display.set_caption("DinoGame")

label = pygame.font.Font("Symbol/Regular.ttf", 60)

bg = pygame.image.load("Background/bg4.png").convert_alpha()
icon = pygame.image.load("icon/icon.png").convert_alpha()
pygame.display.set_icon(icon)
speed = 10

#player
player_move = [
pygame.image.load("Dino/DinoRun1.png").convert_alpha(),
pygame.image.load("Dino/DinoRun2.png").convert_alpha()
]
player_duck = [
pygame.image.load("Dino/DinoDuck1.png").convert_alpha(),
pygame.image.load("Dino/DinoDuck2.png").convert_alpha()
]
player_x = 90
player_y = 340

#ptero
ptero = [
pygame.image.load("Ptero/Ptero1.png").convert_alpha(),
pygame.image.load("Ptero/Ptero2.png").convert_alpha()
] 
ptero_x = 1170
ptero_in_game = []
ptero_rand_pos = [330, 315, 295]

#cactus
cactus = [
pygame.image.load("Cactus/LargeCactus2.png").convert_alpha(),
pygame.image.load("Cactus/SmallCactus2.png").convert_alpha(),
pygame.image.load("Cactus/SmallCactus3.png").convert_alpha()
]
cactus_x = 1160
cactus_y = 350
cactus_in_game = []
cactus_ch = choice(cactus)

#counters
bg_x = 0
counter_ptero_move = 0
counter_move = 0
counter_duck = 0
counter_bg = 0
counter_speed_change = 0
counter_score = 0
counter_cactus_t = 0

#jump
is_jump = False
JUMP_RESET = 11
jump_count = JUMP_RESET
#sounds
jump_sound = pygame.mixer.Sound("Sounds/jump.wav")
game_over_sound = pygame.mixer.Sound("Sounds/gameOver.wav")
level_sound = pygame.mixer.Sound("Sounds/levelUp.wav")

#timers
delay = 3200
ptero_timer = pygame.USEREVENT + 2
pygame.time.set_timer(ptero_timer, choice([i for i in range(10000, 20000, 1000)]))
cactus_timer = pygame.USEREVENT + 1
pygame.time.set_timer(cactus_timer, delay)
timer = 0

#score_timer EightBits
score_label = pygame.font.Font("Symbol/Regular.ttf", 50)
score_t = score_label.render(f"{counter_score}", False, (115,132,148))
score = 0

#labels
label = pygame.font.Font("Symbol/Regular.ttf", 60)
lose_label = label.render("You Lose!", False, (193,196,199))
quit_label = label.render("QUIT", False, (115,132,148))
scores_label = label.render(f"Score: {counter_score}", False, (193,196,199))
restart_label = label.render("Restart", False, (115,132,148))
restart_label_rect = restart_label.get_rect(topleft=(215, 200))
quit_label_rect = restart_label.get_rect(topleft=(215, 300))


gameplay = True

run = True
while run:
	ptero_y = choice(ptero_rand_pos)
	keys = pygame.key.get_pressed()
	# adding a background and implementing its movement
	screen.blit(bg, (bg_x,0))
	screen.blit(bg,(bg_x+1150, 0))
	bg_x -= speed
	if bg_x <= -1150:
		bg_x = 0

	screen.blit(score_t, (1010, 20))
	if gameplay:

 	# appearance of cacti

		if cactus_in_game:
			
			for (i, el) in enumerate(cactus_in_game):
				counter_cactus_t += 1
				screen.blit(cactus_ch, el)
				el.x -= speed

				if el.x < -speed:
					cactus_in_game.pop(i)
					cactus_ch = choice(cactus)

				if player_rect.colliderect(el) or player_duck_rect.colliderect(el):
					game_over_sound.play()
					gameplay = False

	# appearance of a pterodactel
		if ptero_in_game:
			for (i2, el2) in enumerate(ptero_in_game):
				screen.blit(ptero[counter_ptero_move//15], el2)
				el2.x -= speed + 7
				counter_ptero_move += 1

				if counter_ptero_move > 29:
					counter_ptero_move = 0

				if el2.x < -(speed + 7):
					ptero_in_game.pop(i2)

				if player_rect.colliderect(el2) or player_duck_rect.colliderect(el2):
					game_over_sound.play()
					gameplay = False

	# Movement
		if keys[pygame.K_DOWN]:
			player_duck_rect = player_duck[0].get_rect(topleft=(player_x, player_y+17))
			player_rect = player_duck[0].get_rect(topleft=(player_x, player_y+17))
			screen.blit(player_duck[counter_duck//15], (player_x,player_y+17))
			counter_duck += 1
			if counter_duck > 29:
				counter_duck = 0
		else:
			player_rect = player_move[0].get_rect(topleft=(player_x, player_y))
			player_duck_rect = player_move[0].get_rect(topleft=(player_x, player_y))
			screen.blit(player_move[counter_move//15], (player_x,player_y))
			counter_move+=1
			if counter_move > 29:
				counter_move = 0
		
	# Jump
		if not is_jump:
			if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
				is_jump = True
				jump_sound.play()
		else:
			if jump_count >= -JUMP_RESET:
				if jump_count > 0:
					player_y -= (jump_count**2) / 2
				else:
					player_y += (jump_count**2) / 2
				jump_count -= 1
			else:
				is_jump = False
				jump_count = JUMP_RESET

	#Ending
		counter_speed_change += 1
		if counter_speed_change%300 == 0:
			speed += 1
			level_sound.play()
		
		counter_score += 1
		
		score_t = score_label.render(f"{counter_score}", True, (115,132,148))
		score_r = label.render(f"Score: {counter_score}", False, (193,196,199))

# else gameplay
	else:
		screen.fill((87,88,89))
		screen.blit(lose_label, (210, 100))
		screen.blit(restart_label, restart_label_rect)
		screen.blit(quit_label, quit_label_rect)
		screen.blit(score_r, (599, 100))
		mouse = pygame.mouse.get_pos()

		if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
			gameplay = True
			player_x = 90
			player_y = 340
			jump_count = JUMP_RESET
			speed = 8
			counter_cactus_t = 0
			counter_score = 0
			counter_speed_change = 0
			cactus_in_game.clear()
			ptero_in_game.clear()
			pygame.time.set_timer(ptero_timer, choice([i for i in range(10000, 20000, 500)]))

		if quit_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
			pygame.quit()
			run = False

# update display
	pygame.display.update()

# End Game
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			pygame.quit()
		if event.type == cactus_timer:
			cactus_in_game.append(cactus_ch.get_rect(topleft=(cactus_x,cactus_y)))
		if event.type == ptero_timer:
			ptero_in_game.append(ptero[0].get_rect(topleft=(ptero_x,ptero_y)))
	clock.tick(FPS)
