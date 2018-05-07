import pygame

# implement Background class
class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

def main():

    # set display size == background image size
    width = 750
    height = 500

    # set background image
    background = Background('./images/background.jpeg', [0,0])

    # set color palette
    yellow = (237,170,13)
    
    # set initial flags for image blitting
    has_sushi = False
    has_brush = False
    has_chase = False
    win_time = 10000
    
    # set initial moving image locations
    sushi_location_x = -200
    sushi_location_y = -200
    brush_location_x = -200
    brush_location_y = -200
    
    # initiate pygame
    pygame.init()

    # set up screen, clock, fonts, caption
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pretty Kitty")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 25)
    big_font = pygame.font.Font(None, 100)

    # load cat images and store in a list 
    devil_cat = pygame.image.load("./images/devil_cat.png").convert_alpha()
    gazing_sweetly = pygame.image.load("./images/gazing_sweetly.png").convert_alpha()
    reaching = pygame.image.load("./images/reaching.png").convert_alpha()
    sitting_calmly = pygame.image.load("./images/sitting_calmly.png").convert_alpha()
    whats_upstairs = pygame.image.load("./images/whats_upstairs.png").convert_alpha()
    
    cat_images = [gazing_sweetly, reaching, sitting_calmly, whats_upstairs]

    # load moving images
    sushi = pygame.image.load("./images/sushi.png").convert_alpha()
    brush = pygame.image.load("./images/brush.png").convert_alpha()

    # load sounds
    meow = pygame.mixer.Sound("./sounds/meow.wav")
    purr = pygame.mixer.Sound("./sounds/purr.wav")
    chew = pygame.mixer.Sound("./sounds/chew.wav")
    scream = pygame.mixer.Sound("./sounds/scream.wav")

    # selectively play sounds
    # more can be added later 
    def play_sound(number):
        if number == 0:
            meow.play()

    # function to react to mouse click on interactive buttons
    def respond_to_click(key, all_prompts, active_prompts):
        points = active_prompts[key]["points"] + 1
        active_prompts[key].update({"points": points})
        all_prompts[key + "_points"].update({"points": str(points)})

        if key == "feed":
            chew.play()
        elif key == "pet":
            purr.play()
        elif key == "chase":
            scream.play()

    # check whether moving image falls within givin x,y coordinates
    def on_screen(x, y):
        return (-200 <= x <= width) and (-200 <= y <= height)

    # initialize multiple dictionaries for storing game variables
    points_dict = {
        "fun_points": 0,
        "bad_points": 0,
        "meal_points": 0,
    }

    active_prompts = {
        "pet": {
            "prompts": (445, 550, 75, 100),
            "points": 0,
            "end": "Good Kitty!"
        },
        "feed": {
            "prompts": (445, 560, 105, 130),
            "points": 0,
            "end": "Full Kitty!"
        },
        "chase": {
            "prompts": (445, 570, 135, 160),
            "points": 0,
            "end": "Bad              Kitty!"
        }
    }

    all_prompts = {
        "question": {
            "label": "What do you want to do?",
            "location": (425,50),
            "rectangle": (150,450,100,50),
            "color": None
        },
        "pet": {
            "label": "Pet the cat.",
            "location": (450,80),
            "rectangle": ((445,75),(105,25)),
            "color": yellow
        },
        "feed": {
            "label": "Feed the cat.",
            "location": (450,110),
            "rectangle": ((445,105),(115,25)),
            "color": yellow
        },
        "chase": {
            "label": "Chase the cat.",
            "location": (450,140),
            "rectangle": ((445,135),(125,25)),
            "color": yellow
        },
        "pet_points": {
            "label": "Fun points: ",
            "points": str(active_prompts["pet"]["points"]),
            "location": (550,400),
            "rectangle": (150,450,100,50),
            "color": None
        },
        "chase_points": {
            "label": "Bad kitty demerits: ",
            "points": str(active_prompts["chase"]["points"]),
            "location": (550,425),
            "rectangle": (150,450,100,50),
            "color": None
        },
        "feed_points": {
            "label": "Meals fed: ",
            "points": str(active_prompts["feed"]["points"]),
            "location": (550,450),
            "rectangle": (150,450,100,50),
            "color": None
        },
    }

    # set configuration for controlling game behavior
    done = False
    did_win = False
    first_point = True
    show_devil = False
    time_devil = 10000
    MAX_NUM = 5
    current_image = 0
    meow.play()
    timer = pygame.time.get_ticks()
    
    # start main game loop
    while not done:
        
        # calculate how many seconds have elapsed
        # since calling pygame init()
        # GAME TIMER
        timer = pygame.time.get_ticks() / 1000
        
        # end loop if user closes game window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # event handling for right and left arrow keys
            if not did_win and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    current_image = (current_image + 1) % len(cat_images)
                    play_sound(current_image)
                elif event.key == pygame.K_LEFT:
                    current_image = (current_image - 1) % len(cat_images)
                    play_sound(current_image)

        # display background
        screen.fill([255, 255, 255])
        screen.blit(background.image, background.rect)
        
        # render rectangles (if color is assigned) and text for
        # various prompts
        for key in all_prompts:
            if all_prompts[key]["color"]:
                pygame.draw.rect(screen, all_prompts[key]["color"], all_prompts[key]["rectangle"])
            
            # selectively style prompts based on if the prompt
            # tracks points or not
            has_point = "points" in all_prompts[key].keys()
            if has_point:
                label = all_prompts[key]["label"] + all_prompts[key]["points"]
            else:
                label = all_prompts[key]["label"]
            text = font.render(label, True, (0, 0, 0))
            screen.blit(text, all_prompts[key]["location"])

        # overlay background with current cat image
        if not show_devil:           
            screen.blit(cat_images[current_image], (15,125))
        else:
            screen.blit(devil_cat, (15,125))



        #####################################
        ### start logic for moving images ###

        # throws sushi across the screen
        if has_sushi and on_screen(sushi_location_x, sushi_location_y):
            sushi_location_x += 10
            sushi_location_y += 20
            screen.blit(sushi, (sushi_location_x, sushi_location_y))
        elif has_sushi and not on_screen(sushi_location_x, sushi_location_y):
            sushi_location_x = -200
            sushi_location_y = -200
            has_sushi = False
        
        # throws brush across the screen
        if has_brush and on_screen(brush_location_x, brush_location_y):
            brush_location_x += 20
            brush_location_y += 20
            screen.blit(brush, (brush_location_x, brush_location_y))
        elif has_brush and not on_screen(brush_location_x, brush_location_y):
            brush_location_x = -200
            brush_location_y = -200
            has_brush = False

        # switch image to devil_cat 
        if has_chase:
            # print("timer: ", timer, "\nshow_devil: ", show_devil, "time_devil: ", time_devil)
            if not show_devil:
                time_devil = timer
                show_devil = True
                current_image = devil_cat
        if has_chase and timer > time_devil + 1 and not did_win:
            show_devil = False
            has_chase = False
            current_image = 0

        ### end logic for moving images ###
        ###################################





        # event handling for interactive buttons
        if not did_win:
            mouse = pygame.mouse.get_pos()

            # force user to lift mouse button in order
            # to be able to accumulate more points
            if event.type == pygame.MOUSEBUTTONUP and not first_point:
                first_point = True

            # detect if mouse click occurs on interactive buttons
            elif event.type == pygame.MOUSEBUTTONDOWN and first_point:
                x, y = mouse
                for key in active_prompts:
                    a, b = active_prompts[key]["prompts"][0], active_prompts[key]["prompts"][1]
                    c, d = active_prompts[key]["prompts"][2], active_prompts[key]["prompts"][3]
                    if (a <= x <= b) and (c <= y <= d):
                        respond_to_click(key, all_prompts, active_prompts)
                        if key == "feed":
                            has_sushi = True
                        elif key == "pet":
                            has_brush = True
                        elif key == "chase":
                            has_chase = True

                        first_point = False

        # check if game is over
        for key in active_prompts:
            if active_prompts[key]["points"] >= MAX_NUM:
                # start timer to display win_text for
                # certain length of time
                if not did_win:
                    win_time = timer
                    did_win = True
 
                # dynamically display correct win_text string
                # at the correct location
                win_text = big_font.render(active_prompts[key]["end"], True, (0,0,0))

                # text location is different for devil_cat image
                if not show_devil:
                    screen.blit(win_text, ((width / 2 - 25), (height / 2 - 50)))
                else:
                    screen.blit(win_text, (130,300))

        # let game end if enough time (2.5 seconds)
        # has elapsed since winning
        if timer > win_time + 2.5:
            done = True

        # update display each frame
        pygame.display.update()
        clock.tick(20)

    # main loop has been exited
    # and the game is finished
    pygame.quit()

# start the game by calling main()
main()