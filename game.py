import pygame
import sys
import time
import random

class Plate(pygame.sprite.Sprite):

	def __init__(self, loc, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(loc)
		self.image = pygame.transform.scale(self.image, (85, 50))
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, x_change, y_change):
		self.rect.x = x_change
		self.rect.y = y_change

	def draw(self, screen):
		screen.blit(self.image, (self.x, self.y))
		screen.blit(self.image, (self.x + 600, self.y))


class Food(pygame.sprite.Sprite):
	def __init__(self, x, img, iscorrect):

		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(img)
		self.image = pygame.transform.scale(self.image, (100, 100))
		self.rect = self.image.get_rect()
		self.ypos = [-300]
		self.xpos = [65, 190, 315]

		self.rect.x = x
		self.rect.y = random.choice(self.ypos)

		self.isCorrect = iscorrect

	def update(self):
		global speed
		self.rect.y += speed


	def delete(self):
		self.kill()

	def changeimg(self):
		self.image = pygame.image.load("clear.png")

	def haspassed(self):
		if self.rect.y > 600:
			return True
		else:
			return False

	def isoff(self):
		if self.rect.y > 600:
			self.delete()
			return True
		else:
			return False


display_width = 480
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
blue = (0, 0, 200)
bright_blue = (0, 0, 255)

end = False

lline = 65 
mline = 190
rline = 315

# 125 
xposopts = [[lline, mline], [mline, rline], [lline, rline]]


pygame.init()
gameDisplay = pygame.display.set_mode((display_width, display_height))

inidialogue = ["I need some ", "Find me ", "I'm looking for "]

clock = pygame.time.Clock()


pics = {"fruit" : ["banana.png", "apple.png", "orange.png"], "vegetables" : ["carrot.png", "broccoli.png", "potato.png"], "grain" : ["rice.png", "wheat.png"], "protein" : ["chicken.png", "egg.png"], "dairy" : ["milk.png","yogurt.png"]}
calories = 0 
s = ["fruit", "vegetables", "grain", "protein", "dairy"]

caloriedict = {"banana.png" : 100 , "apple.png" : 100,  "orange.png" : 50,  "carrot.png" : 75,  "broccoli.png" : 50,  "potato.png" : 100,  "rice.png" : 150,  "wheat.png" : 100,  "chicken.png" : 200,  "egg.png" : 75,  "milk.png" : 75,  "yogurt.png" : 100}



typedict = {"fruit" : 0, "vegetables" : 1, "grain" : 2, "protein"  : 3, "dairy" : 4}
typedictinv = {0 : "fruit", 1 : "vegetables", 2 : "grain", 3  : "protein", 4 : "dairy" }

smin = [1, 2, 4, 3, 2]
smax = [2, 3, 6, 5, 3]





def gameexit():
	pygame.quit()
	quit()

def button(msg, x, y, w, h, ic, ac, tsize, screen, action=None):
	global end

	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x + w > mouse[0] > x and y + h > mouse[1] > y:
		pygame.draw.rect(screen, ac, (x, y, w, h))

		if click[0] == 1 and action is not None:
			if action == "reset":
				end = True
			if action == "restart":
				main()
			if action == "quit":
				gameexit()

			if action == "start":
				infomenu()
				
	else:
		pygame.draw.rect(screen, ic, (x, y, w, h))

	message_display('Consolas', tsize, msg, x + (w / 2), y + (h / 2), screen)


def crash(gameDisplay, servings, didWin):
	if didWin == False:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameexit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						main()



			gameDisplay.fill(white)
			message_display('Consolas', 20, "Oh no! You chose", 230, 150, gameDisplay)
			message_display('Consolas', 20, "the wrong food!", 230, 170, gameDisplay)


			message_display('Consolas', 15, "Fruit   Vegetables   Grain   Protein    Dairy",  230, 240, gameDisplay)
			message_display('Consolas', 15, "%s         %s         %s        %s        %s" % (servings["fruit"], servings["vegetables"], servings["grain"], servings["protein"], servings["dairy"]) ,  230, 260, gameDisplay)


			button("Restart", 175, 400, 120, 55, green, bright_green, 29, gameDisplay, "restart")
			button("Quit", 175, 480, 120, 55, red, bright_red, 29, gameDisplay, "quit")

			pygame.display.update()

	else:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameexit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						main()



			gameDisplay.fill(white)

			message_display('Consolas', 20, "Congratulations", 240, 150, gameDisplay)
			message_display('Consolas', 20, "You chose the right food!", 220, 170, gameDisplay)


			message_display('Consolas', 15, "Fruit   Vegetables   Grain   Protein    Dairy",  230, 240, gameDisplay)
			message_display('Consolas', 15, "%s         %s         %s        %s        %s" % (servings["fruit"], servings["vegetables"], servings["grain"], servings["protein"], servings["dairy"]) ,  230, 260, gameDisplay)


			button("Restart", 175, 400, 120, 55, green, bright_green, 25, gameDisplay, "restart")
			button("Quit", 175, 480, 120, 55, red, bright_red, 25, gameDisplay, "quit")

			pygame.display.update()



def text_objects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()


def message_display(font, size, text, width, height, screen):
	DisText = pygame.font.SysFont(font, size)
	TextSurf, TextRect = text_objects(text, DisText)
	TextRect.center = (width, height)
	screen.blit(TextSurf, TextRect)


counter = 0
xcomb = random.choice(xposopts)

def passcheck(obstacle_group, all_sprites, perthingeach):
	global speed
	global counter
	global xcomb
	global imgchoice

	passed = False
	candel = False

	speed = speed + 0.0001

	if obstacle_group.sprites()[0].haspassed():

		candel = True

	if candel:
		obstacle_group.sprites()[0].delete()
		obstacle_group.sprites()[0].delete()
		candel == False
		passed = True

	if passed:
		xcomb = random.choice(xposopts)


		tlist = list(s)
		tlist.remove(perthingeach[currentround])



		templist = random.sample(tlist , 2)



		for a in range(2):
			obstacle_group.add(Food(xcomb[a], random.choice(pics[templist[a]]), False))


		imgchoice = random.choice(pics[perthingeach[currentround]])
		obstacle_group.add(Food(list(set([lline, mline, rline]) - set(xcomb))[0], imgchoice, True))

	all_sprites.remove(obstacle_group)
	all_sprites.add(obstacle_group)
	


def startscreen():
	startscreen = pygame.image.load("title.png")
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					infomenu()

		pygame.display.set_caption("FoodRunner")
		gameDisplay.fill(white)
		gameDisplay.blit(startscreen,  (-12, 0))
		button("Start!", 189, 500, 100, 60, green, bright_green, 30, gameDisplay, "start")

		pygame.display.update()

def infomenu():
	gameDisplay.fill(white)
	selectscreen = pygame.image.load("select.png")

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				break

		pygame.display.set_caption("FoodRunner")
		gameDisplay.blit(selectscreen,  (-15, 0))

		button("Start", 185, 500, 100, 50, green, bright_green, 30, gameDisplay, "restart")


		pygame.display.update()
	


def drawseq(gameDisplay, clock, background, bgx, bgy, whattodo):
	global calories
	pygame.display.set_caption("Food Runner | FPS: " + str(int(clock.get_fps())))

	gameDisplay.blit(background, (bgx, bgy))
	gameDisplay.blit(background, (bgx, bgy - 600))

	message_display('Consolas', 23, whattodo, 300, 550, gameDisplay)

	message_display('Consolas', 23, "Calories: " + str(calories), 100, 50, gameDisplay)





speed = 5



def setup():
	t = 0
	perthing = []
	askstatements = []
	perthingeach = []

	counter = 0

	for x in range(5):
		y = random.randint(smin[x], smax[x])
		t += y
		perthing.append(y)
		for q in range(y):
			perthingeach.append(typedictinv[x])




	for thing in perthing:
		for x in range(thing):
			askstatements.append(random.choice(inidialogue) + typedictinv[counter])
		counter += 1


	return t, perthing, askstatements, perthingeach


servings = {"fruit" : 0, "vegetables" : 0, "grain" : 0, "protein"  : 0, "dairy" : 0}

currentround = 0 

def shufflelist(*ls):
	l = list(zip(*ls))

	random.shuffle(l)
	return zip(*l)

imgchoice = ""
def main():

	global speed
	global servings
	global currentround
	global calories
	global imgchoice

	servings = {"fruit" : 0, "vegetables" : 0, "grain" : 0, "protein"  : 0, "dairy" : 0}
	calories = 0


	end = False

	player_x = 80
	player_y = 400


	bgx = 0
	bgy = 0

	rounds, perthing, askstatements, perthingeach = setup()

	askstatements, perthingeach = shufflelist(askstatements, perthingeach)

	all_sprites = pygame.sprite.Group()
	obstacle_group = pygame.sprite.Group()
	player_group = pygame.sprite.Group()

	player = Plate("bowl.png", player_x, player_y)
	player_group.add(player)

	background = pygame.image.load("road.png")

	xcomb = random.choice(xposopts)

	tlist = list(s)
	tlist.remove(perthingeach[currentround])


	templist = random.sample(tlist , 2)



	for a in range(2):
		obstacle_group.add(Food(xcomb[a], random.choice(pics[templist[a]]), False))


	imgchoice = random.choice(pics[perthingeach[currentround]])
	obstacle_group.add(Food(list(set([lline, mline, rline]) - set(xcomb))[0], imgchoice, True))



	all_sprites.add(player_group)
	all_sprites.add(obstacle_group)


	while not end:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				end = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					player_x  += -120

				if event.key == pygame.K_RIGHT:
					player_x += 120

					 



		if player_x < 80:
			player_x = 80

		if player_x > 320:
			player_x = 320

		bgy = bgy + speed
		if bgy >= 600:
			bgy = 0


		drawseq(gameDisplay, clock, background, bgx, bgy, askstatements[currentround])

		passcheck(obstacle_group, all_sprites, perthingeach)

		player_group.update(player_x, player_y)

		obstacle_group.update()
		all_sprites.draw(gameDisplay)

		
		hits = pygame.sprite.spritecollide(player, obstacle_group, False)
		


		if hits == []:
			pass

		else:

			if hits[0].isCorrect == False:
				end = True
				player.kill() 
				crash(gameDisplay, servings, False)
				break
				
			else:
				hits[0].delete()
				servings[perthingeach[currentround]] += 1
				calories += caloriedict[imgchoice]
				print caloriedict[imgchoice]
				print imgchoice
				currentround += 1

		if currentround == rounds:
			crash(gameDisplay, servings, True)



		clock.tick(60)
		pygame.display.update()

	gameexit()


if __name__ == "__main__":
	startscreen()
	main()
