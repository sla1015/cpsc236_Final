import pygame, sys, random, csv
# A means that the lines follwing it were altered.

# Initiates
pygame.init()
pygame.display.set_caption("Dogdle")
WIDTH, HEIGHT = 1500, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 30

# Handles the various colors of the GUI
GREY = (100, 100, 100)
DARK_GREY = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (255, 108, 108)
COLOR_INCORRECT = (50, 50, 50)
COLOR_MISPLACED = (255, 193, 53)
COLOR_CORRECT = (0, 185, 6)
COLOR_BUTTON_LIGHT = (170,170,170)
COLOR_BUTTON_DARK = (100,100,100)

# Used to time temporary pop-up notifications
TEXT_TIMER = 2

# Handles the rectangles and the various dimensions about them
NUM_ROWS = 8
NUM_COLS = 6
RECT_WIDTH = 30
RECT_HEIGHT = 30
DX = 10 # Pixels between rectangles width-wise
DY = (HEIGHT/NUM_ROWS)/2.5 # Pixels between rectangles height-wise

# Initializes the mouse
mouse = pygame.mouse.get_pos()

# Leftmost topmost coordinate where the first rect will be drawn, should be symmetrical. Accounts for number of rects, pixels between rects and rect sizes.
BASE_OFFSET_X = (WIDTH/2)-((NUM_COLS/2)*DX)-((NUM_COLS/2)*RECT_WIDTH)+(((NUM_COLS+1)%2)*(DX/2))
BASE_OFFSET_Y = (HEIGHT/2)-((NUM_ROWS/2)*DY)-((NUM_ROWS/2)*RECT_HEIGHT)+(((NUM_ROWS+1)%2)*(DY/2))

INPUT_RECT = pygame.Rect(BASE_OFFSET_X, BASE_OFFSET_Y, 140, 40)

# Loads the images for the hint giving
correct = pygame.image.load("hints/correct.png")
incorrect = pygame.image.load("hints/incorrect.png")
higher = pygame.image.load("hints/higher.png")
lower = pygame.image.load("hints/lower.png")
correct_continent = pygame.image.load("hints/continent.png")

def main():
    clock = pygame.time.Clock()
   
    # Sets the various fonts the game uses
    stat_text = pygame.font.Font(None, 100)
    letter_font = pygame.font.Font(None, 65)
    text = pygame.font.Font(None, 40)
    small_text = pygame.font.Font(None, 29)
   
    # All these variables handle typing and storing the guesses made by the user
    guessed_dogs = []
    curr_dog = ""
    guess_input=""
    dog_count = 0
    curr_letter = 0
    rects = []
   
    # Flags used to manage the various states the game can be in
    flag_win = False
    flag_lose = False
    flag_invalid_dog = False
    flag_show_menu = False
    flag_show_dog_list = False
    flag_show_dog_stats=False
    flag_setup=True
    timer_flag_1 = 0
   
    # Creates the List of possible inputs and the answer, along with the name of the file
    file_name="Dog201.csv"
    dog_Key,Dog_List,data=create_List(file_name)
    dog_Key_Name=dog_Key["Name"]
   
   
    # Variables handling both buttons locations and dimensions
    list_button_location=[WIDTH-200,HEIGHT-60]
    menu_button_location=[60,HEIGHT-60]
    button_dim=[140,40]
   
    # Game Loop
    while True:
        mouse = pygame.mouse.get_pos()
       
        # Used for determining if the mouse is over the button
        mouse_on_list_button=(list_button_location[0] <= mouse[0] <= list_button_location[0]+button_dim[0]
                              and list_button_location[1] <= mouse[1] <= list_button_location[1]+button_dim[1])
        mouse_on_menu_button=(menu_button_location[0] <= mouse[0] <= menu_button_location[0]+button_dim[0]
                              and menu_button_location[1] <= mouse[1] <= menu_button_location[1]+button_dim[1])

        # Handles getting the game events # Mostly written by Sage
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Option to restart game
            if flag_win or flag_lose:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                       
            # Checks if the mouse clicks. If it clicks on a button it changes the state of various flags to change screens
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_on_list_button:
                    if flag_show_dog_list==True:
                        if flag_show_dog_stats==True:
                            flag_show_dog_stats=False
                        elif flag_show_dog_stats==False:
                            flag_show_dog_list=False
                    elif flag_show_dog_list==False:
                        flag_show_dog_list=True
                elif mouse_on_menu_button==True:
                    if flag_show_menu==True:
                        flag_show_menu=False
                    elif flag_show_menu==False:
                        flag_show_menu=True
            else:
                # Upon keypress
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        # Prevents IndexErrors
                        if curr_dog:
                            curr_dog = curr_dog[:-1]
                            curr_letter -= 1
                    elif event.key == pygame.K_RETURN:
                        # Handles the user submitting a guess
                        if curr_dog.title() in Dog_List:
                            dog_count += 1
                            guessed_dogs.append(curr_dog)
                            guess_input=curr_dog
                            curr_dog = ""
                            curr_letter = 0
                        else:
                            flag_invalid_dog = True
                            timer_flag_1 = 0
                    # Handles ways the user may type, either a letter or a space
                    elif event.key == pygame.K_SPACE:
                        curr_dog += " "
                        curr_letter += 1
                    else:
                        if event.unicode.isalpha():
                            curr_dog += event.unicode.upper()
                            curr_letter += 1
       
        # Initiates the mouse
        mouse = pygame.mouse.get_pos()
       
        # Set the Background
        SCREEN.fill(DARK_GREY)
       
        # Draws the buttons and Highlights them if hovered over also prints lables on them. Seth
        if mouse_on_list_button:
            pygame.draw.rect(SCREEN,COLOR_BUTTON_LIGHT,[list_button_location[0],list_button_location[1],button_dim[0],button_dim[1]])
            
        else:
            pygame.draw.rect(SCREEN,COLOR_BUTTON_DARK,[list_button_location[0],list_button_location[1],button_dim[0],button_dim[1]])
       
        if mouse_on_menu_button:
            pygame.draw.rect(SCREEN,COLOR_BUTTON_LIGHT,[menu_button_location[0],menu_button_location[1],button_dim[0],button_dim[1]])
            
        else:
            pygame.draw.rect(SCREEN,COLOR_BUTTON_DARK,[menu_button_location[0],menu_button_location[1],button_dim[0],button_dim[1]])
        button_Text = small_text.render("Show Dog List", True, WHITE)
        SCREEN.blit(button_Text,(WIDTH-200,HEIGHT-55))
       
        button_Text = small_text.render("How to Play", True, WHITE)
        SCREEN.blit(button_Text,(60,HEIGHT-55))
       
        # Draw title and underline
        draw_title(letter_font)
       
        # Draws the rectangle the User types in
        pygame.draw.rect(SCREEN, GREY, INPUT_RECT)
       
        # Draws base 5x6 grid for letters. Seth
        for y in range(NUM_ROWS):
            row_rects = []  
            for x in range(NUM_COLS):
                x_pos = BASE_OFFSET_X+(x*DX)+(x*RECT_WIDTH)
                y_pos = BASE_OFFSET_Y+(y*DY)+(y*RECT_HEIGHT)+50
                curr_rect = pygame.Rect((x_pos, y_pos), (RECT_WIDTH, RECT_HEIGHT))
                pygame.draw.rect(SCREEN,GREY,curr_rect,2)
                row_rects.append((x_pos, y_pos))
            rects.append(row_rects)
           
       
        # Alerts player that Dog is not in the list of Dogs. Text appears for 2 seconds. Sage
        if flag_invalid_dog:
            text_surface = text.render("Not a valid dog", True, RED)
            x_pos = BASE_OFFSET_X + (RECT_WIDTH * (NUM_COLS/5))
            y_pos = BASE_OFFSET_Y - (DY)
            SCREEN.blit(text_surface, (x_pos, y_pos))
            timer_flag_1 += 1
            if timer_flag_1 == TEXT_TIMER * FPS:
                flag_invalid_dog = False
                timer_flag_1 = 0
   
       
   
        # Blits each letter of the dog's name the user is currently typing.
        # Firstly renders each letter, then blits it in the input rectangle. Seth
        if curr_dog:
            for letter_index in range(len(curr_dog)):
                text_surface = letter_font.render(curr_dog, True, (255, 255, 255))
                INPUT_RECT.w = max(100, text_surface.get_width())
                SCREEN.blit(text_surface, (INPUT_RECT.x, INPUT_RECT.y))
   
        # Renders the dogs stats next to its hints. Seth
        if guessed_dogs:
            for dog_index in range(len(guessed_dogs)):
           
                for hint_index in range(len(guessed_dogs[dog_index])):
                    this_dog=guessed_dogs[dog_index].title()
                   
                   
                    dog_display="Name: "+data[this_dog]["Name"]+". Group: "+data[this_dog]["Group"]+"\n"\
                                "Height: "+data[this_dog]["Average Male Height"]+". Weight: "+data[this_dog]["Average Male Weight"]+\
                                "Year: "+data[this_dog]["Year of Recognition"]+". Rank: "+data[this_dog]["Popularity Rank"]+"\n"\
                                "Region: "+data[this_dog]["Place of Origin"][0]+". Continent: "+data[this_dog]["Place of Origin"][1]
                   
                    pos=[BASE_OFFSET_X+(NUM_COLS*DX)+(NUM_COLS*RECT_WIDTH),(BASE_OFFSET_Y+(dog_index*DY)+(dog_index*RECT_HEIGHT)+DY)-(small_text.size("")[1])]
                   
                    blit_Long_Text(text=dog_display, pos=pos, font=small_text)
                 
        evaluate(guessed_dogs, rects, dog_Key, data)
       
        # Handles if the user won or not. Sage    
        if guess_input.title() == dog_Key_Name:
            flag_win = True
        elif len(guessed_dogs) == NUM_ROWS:
            flag_lose = True
       
        # Displays a message upon game over, either a winning message or a losing message. Sage
        if flag_win:
            success_message="Correct! Press 'R' to play again"
            text_surface = text.render(success_message, True, WHITE)
            x_pos = WIDTH/2 - text.size(success_message)[0]/2
            y_pos = BASE_OFFSET_Y + (DY*9) + (RECT_HEIGHT * NUM_ROWS)
            SCREEN.blit(text_surface, (x_pos, y_pos))
        if flag_lose:
            failure_Message="Too bad, The Answer was "+dog_Key_Name+"! Press 'R' to play again"
            text_surface = text.render(failure_Message, True, WHITE)
            x_pos = WIDTH/2 - text.size(failure_Message)[0]/2
            y_pos = BASE_OFFSET_Y + (DY*9) + (RECT_HEIGHT * NUM_ROWS)
            SCREEN.blit(text_surface, (x_pos, y_pos))
       
        # Handles displaying the list of dogs, changes the size of the font according to the amount displaying. Seth
        if flag_show_dog_list:
            if file_name=="Dog25.csv":
                font=letter_font
                spaceing=50
            elif file_name=="Dog100.csv":
                font=text
                spaceing=30
            elif file_name=="Dog201.csv":
                font=small_text
                spaceing=20
            SCREEN.fill(DARK_GREY)
           
            # Draws the button to hide the list of dogs and labels it. Seth
            if mouse_on_list_button:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_LIGHT,[list_button_location[0],list_button_location[1],button_dim[0],button_dim[1]])
                
            else:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_DARK,[list_button_location[0],list_button_location[1],button_dim[0],button_dim[1]])
            button_Text = small_text.render("Hide Dog List", True, WHITE)
            SCREEN.blit(button_Text,(WIDTH-200,HEIGHT-55))
           
            # Handles formatting the dogs. Seth
            x_dog_pos=5
            y_dog_pos=0
            y_inc=font.size(Dog_List[1])[1]
            dog_locations=[]
            for i in range(len(Dog_List)):
                dog_location=[]
                print_text=Dog_List[i]+" ||"
                dog_width=font.size(Dog_List[i])[0]
                dog_height=font.size(Dog_List[i])[1]
                text_surface = font.render(print_text, True, WHITE)
                SCREEN.blit(text_surface,(x_dog_pos,y_dog_pos))
                dog_location=[Dog_List[i],x_dog_pos,y_dog_pos,dog_width,dog_height]
                dog_locations.append(dog_location)
                x_inc=font.size(Dog_List[i])[0]
                x_dog_pos+=x_inc+spaceing
               
                if (font.size(Dog_List[i])[0]+x_dog_pos)>1400:
                    x_dog_pos=5
                    y_dog_pos+=y_inc
            # Used for allowing the user to click on the dog in question and see a page showing their stats. Seth
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(dog_locations)):
                    mouse_on_dog=dog_locations[i][1] <= mouse[0] <= dog_locations[i][1]+dog_locations[i][3] and dog_locations[i][2] <= mouse[1] <= dog_locations[i][2]+dog_locations[i][4]
                    if mouse_on_dog:
                        clicked_dog=dog_locations[i][0]
                        flag_show_dog_stats=True
                       
        # Shows the user the stats of the dog in question. Seth            
        if flag_show_dog_stats:
            SCREEN.fill(DARK_GREY)
            if mouse_on_list_button:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_LIGHT,[list_button_location[0],list_button_location[1],button_dim[0],button_dim[1]])
                
            else:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_DARK,[list_button_location[0],list_button_location[1],button_dim[0],button_dim[1]])
                
            button_Text = small_text.render("Hide Dog Stats", True, WHITE)
            SCREEN.blit(button_Text,(WIDTH-200,HEIGHT-55))
            y_pos=0
            for item in data[clicked_dog]:
                if item=="Place of Origin":
                    for i in range(2):
                        this_item=item+" "+data[clicked_dog.title()][item][i]
                        stats = stat_text.render(this_item, True, WHITE)
                        x_pos=WIDTH/2-stat_text.size(this_item)[0]/2
                        SCREEN.blit(stats,(x_pos,y_pos))
                        y_pos+=stat_text.size(this_item)[1]
                else:
                    this_item=item+" "+data[clicked_dog.title()][item]
                    stats = stat_text.render(this_item, True, WHITE)
                    x_pos=WIDTH/2-stat_text.size(this_item)[0]/2
                    SCREEN.blit(stats,(x_pos,y_pos))
                    y_pos+=stat_text.size(this_item)[1]
       
        # Prints a screen that display a guide for how to play dogdle. Sage
        if flag_show_menu:
            SCREEN.fill(DARK_GREY)
            # draws a button for the how to play and labels it
            if mouse_on_menu_button:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_LIGHT,[menu_button_location[0],menu_button_location[1],button_dim[0],button_dim[1]])
                
            else:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_DARK,[menu_button_location[0],menu_button_location[1],button_dim[0],button_dim[1]])
               
            button_Text = small_text.render("Back to Game", True, WHITE)
            SCREEN.blit(button_Text,(60,HEIGHT-55))
           
            how_to_Play=("To play dogdle, type the name of one of the official AKC recognized dog breeds.\n"\
                          "You may see a list of those by clicking the 'Show dog list' Button on the home screen.\n"\
                          "With this screen you can click on the name of a dog and a menu will appear showing you that dogs stats.\n"\
                          "After entering the Name of this dog, you will see hints about the various statistics of that dog.")
            pos=[100,50]
               
            blit_Long_Text(text=how_to_Play,pos=pos,font=letter_font)
       
        # Displays a menu allowing the user to select a dififculty option. Sage
        if flag_setup:
            file_name=''
            mouse = pygame.mouse.get_pos()

            SCREEN.fill(DARK_GREY)
           
            setup_text="Would you like to select Easy, Medium, or Hard?\nEasy is a list of 25 most popular dogs.\n"\
                        "Medium is the top 100.\nHard is the full list of 201 AKC dogs"
                       
            pos=[200,100]
           
            blit_Long_Text(text=setup_text,pos=pos,font=letter_font)
           
           
            mouse_on_easy_button=WIDTH/4 <= mouse[0] <= WIDTH/4+button_dim[0] and HEIGHT-100 <= mouse[1] <= HEIGHT-100+button_dim[1]
            mouse_on_medium_button=WIDTH/2 <= mouse[0] <= WIDTH/2+button_dim[0]+45 and HEIGHT-100 <= mouse[1] <= HEIGHT-100+button_dim[1]
            mouse_on_hard_button=WIDTH*(3/4) <= mouse[0] <= WIDTH*(3/4)+button_dim[0] and HEIGHT-100 <= mouse[1] <= HEIGHT-100+button_dim[1]
           
            # draws buttons for the difficulties and labels them
            if mouse_on_easy_button:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_LIGHT,[WIDTH/4,HEIGHT-100,button_dim[0],button_dim[1]])
            
            else:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_DARK,[WIDTH/4,HEIGHT-100,button_dim[0],button_dim[1]])
            button_Text = letter_font.render("EASY", True, WHITE)
            SCREEN.blit(button_Text,(WIDTH/4,HEIGHT-100))
               
            if mouse_on_medium_button:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_LIGHT,[WIDTH/2,HEIGHT-100,button_dim[0]+45,button_dim[1]])
            
            else:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_DARK,[WIDTH/2,HEIGHT-100,button_dim[0]+45,button_dim[1]])
            button_Text = letter_font.render("MEDIUM", True, WHITE)
            SCREEN.blit(button_Text,(WIDTH/2,HEIGHT-100))
               
            if mouse_on_hard_button:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_LIGHT,[WIDTH*(3/4),HEIGHT-100,button_dim[0],button_dim[1]])
            
            else:
                pygame.draw.rect(SCREEN,COLOR_BUTTON_DARK,[WIDTH*(3/4),HEIGHT-100,button_dim[0],button_dim[1]])
            button_Text = letter_font.render("HARD", True, WHITE)
            SCREEN.blit(button_Text,(WIDTH*(3/4),HEIGHT-100))
           
            # Handles clicking the button and assigning the dog key as needed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if mouse_on_easy_button:
                        file_name="Dog25.csv"
                        dog_Key,Dog_List,data=create_List(file_name)
                        dog_Key_Name=dog_Key["Name"]
                        flag_setup=False
                    elif mouse_on_medium_button:
                        file_name="Dog100.csv"
                        dog_Key,Dog_List,data=create_List(file_name)
                        dog_Key_Name=dog_Key["Name"]
                        flag_setup=False
                    elif mouse_on_hard_button:
                        file_name="Dog201.csv"
                        dog_Key,Dog_List,data=create_List(file_name)
                        dog_Key_Name=dog_Key["Name"]
                        flag_setup=False

        pygame.display.update()
        clock.tick(FPS)
       
def blit_Long_Text(text,pos,font):
    """
    Parameters
    ----------
    text : STRING
        The string that this function will blit.
    pos : TUPLE
        Contains the first starting location for the text.
    font : FONT
        The font that pygames will use to blit and render.

    Returns
    -------
    None.
   
    Functions
    ---------
    this function is used to blit a long piece of text. its used this way so that long strings wont go off the screen
   
    Authored
    --------
    Fully Written by Sage

    """
    max_Width=WIDTH-100
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x_pos,y_pos=pos
    for line in words:
        for word in line:
            text_surface=font.render(word, True, WHITE)
            word_width, word_height = font.size(word)
            if x_pos+word_width>=max_Width:
                x_pos=pos[0]
                y_pos+=word_height
            SCREEN.blit(text_surface,(x_pos,y_pos))
            x_pos+=word_width+space
        x_pos=pos[0]
        y_pos+=word_height

def evaluate(guessed_dogs, rects, dog_Key, data):
    """
    Parameters
    ----------
    guessed_dogs : LIST
        A list of the dogs that the user has guessed.
    rects : MATRIX
        Contains the rectangle locations for where the hints go.
    dog_Key : Dictionary
        A dictionary of the stats for the correct dog.
    data : 2D Dictionary
        A Nested dicionary of all the dogs and their stats
    Returns
    -------
    None.
   
    Functions
    ---------
    Compares the users guess and displays hints to aid in gameplay
   
    Authored
    --------
    Fully Written by Seth

    """
   
    for dog_index in range(len(guessed_dogs)):
       
        if dog_index==0:
            for i in range(6):
               
                curr_rect = pygame.Rect((rects[0][i][0], rects[0][i][1]), (RECT_WIDTH, RECT_HEIGHT))                    
               
                if i==0:
                    if dog_Key["Group"]==data[guessed_dogs[dog_index].title()]["Group"]:
                        SCREEN.blit(correct, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
                if i==1:
                    if dog_Key["Average Male Height"]==data[guessed_dogs[dog_index].title()]["Average Male Height"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Height"])>int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Height"])<int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==2:
                    if dog_Key["Average Male Weight"]==data[guessed_dogs[dog_index].title()]["Average Male Weight"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])>int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])<int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==3:
                    if dog_Key["Year of Recognition"]==data[guessed_dogs[dog_index].title()]["Year of Recognition"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])>int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])<int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==4:
                    if dog_Key["Popularity Rank"]==data[guessed_dogs[dog_index].title()]["Popularity Rank"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])>int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])<int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==5:
                    if dog_Key["Place of Origin"][0]==data[guessed_dogs[dog_index].title()]["Place of Origin"][0]:
                        SCREEN.blit(correct, (curr_rect))
                    elif dog_Key["Place of Origin"][1]==data[guessed_dogs[dog_index].title()]["Place of Origin"][1]:
                        SCREEN.blit(correct_continent, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
        elif dog_index==1:
            for i in range(6):
               
                curr_rect = pygame.Rect((rects[1][i][0], rects[1][i][1]), (RECT_WIDTH, RECT_HEIGHT))                    
               
                if i==0:
                    if dog_Key["Group"]==data[guessed_dogs[dog_index].title()]["Group"]:
                        SCREEN.blit(correct, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
                if i==1:
                    if dog_Key["Average Male Height"]==data[guessed_dogs[dog_index].title()]["Average Male Height"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Height"])>int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Height"])<int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==2:
                    if dog_Key["Average Male Weight"]==data[guessed_dogs[dog_index].title()]["Average Male Weight"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])>int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])<int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==3:
                    if dog_Key["Year of Recognition"]==data[guessed_dogs[dog_index].title()]["Year of Recognition"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])>int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])<int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==4:
                    if dog_Key["Popularity Rank"]==data[guessed_dogs[dog_index].title()]["Popularity Rank"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])>int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])<int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==5:
                    if dog_Key["Place of Origin"][0]==data[guessed_dogs[dog_index].title()]["Place of Origin"][0]:
                        SCREEN.blit(correct, (curr_rect))
                    elif dog_Key["Place of Origin"][1]==data[guessed_dogs[dog_index].title()]["Place of Origin"][1]:
                        SCREEN.blit(correct_continent, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
        elif dog_index==2:
            for i in range(6):
               
                curr_rect = pygame.Rect((rects[2][i][0], rects[2][i][1]), (RECT_WIDTH, RECT_HEIGHT))                    
               
                if i==0:
                    if dog_Key["Group"]==data[guessed_dogs[dog_index].title()]["Group"]:
                        SCREEN.blit(correct, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
                if i==1:
                    if dog_Key["Average Male Height"]==data[guessed_dogs[dog_index].title()]["Average Male Height"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Height"])>int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Height"])<int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==2:
                    if dog_Key["Average Male Weight"]==data[guessed_dogs[dog_index].title()]["Average Male Weight"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])>int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])<int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==3:
                    if dog_Key["Year of Recognition"]==data[guessed_dogs[dog_index].title()]["Year of Recognition"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])>int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])<int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==4:
                    if dog_Key["Popularity Rank"]==data[guessed_dogs[dog_index].title()]["Popularity Rank"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])>int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])<int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==5:
                    if dog_Key["Place of Origin"][0]==data[guessed_dogs[dog_index].title()]["Place of Origin"][0]:
                        SCREEN.blit(correct, (curr_rect))
                    elif dog_Key["Place of Origin"][1]==data[guessed_dogs[dog_index].title()]["Place of Origin"][1]:
                        SCREEN.blit(correct_continent, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
        elif dog_index==3:
            for i in range(6):
               
                curr_rect = pygame.Rect((rects[3][i][0], rects[3][i][1]), (RECT_WIDTH, RECT_HEIGHT))                    
               
                if i==0:
                    if dog_Key["Group"]==data[guessed_dogs[dog_index].title()]["Group"]:
                        SCREEN.blit(correct, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
                if i==1:
                    if dog_Key["Average Male Height"]==data[guessed_dogs[dog_index].title()]["Average Male Height"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Height"])>int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Height"])<int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==2:
                    if dog_Key["Average Male Weight"]==data[guessed_dogs[dog_index].title()]["Average Male Weight"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])>int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])<int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==3:
                    if dog_Key["Year of Recognition"]==data[guessed_dogs[dog_index].title()]["Year of Recognition"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])>int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])<int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==4:
                    if dog_Key["Popularity Rank"]==data[guessed_dogs[dog_index].title()]["Popularity Rank"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])>int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])<int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==5:
                    if dog_Key["Place of Origin"][0]==data[guessed_dogs[dog_index].title()]["Place of Origin"][0]:
                        SCREEN.blit(correct, (curr_rect))
                    elif dog_Key["Place of Origin"][1]==data[guessed_dogs[dog_index].title()]["Place of Origin"][1]:
                        SCREEN.blit(correct_continent, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
        elif dog_index==4:
            for i in range(6):
               
                curr_rect = pygame.Rect((rects[4][i][0], rects[4][i][1]), (RECT_WIDTH, RECT_HEIGHT))                    
               
                if i==0:
                    if dog_Key["Group"]==data[guessed_dogs[dog_index].title()]["Group"]:
                        SCREEN.blit(correct, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
                if i==1:
                    if dog_Key["Average Male Height"]==data[guessed_dogs[dog_index].title()]["Average Male Height"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Height"])>int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Height"])<int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==2:
                    if dog_Key["Average Male Weight"]==data[guessed_dogs[dog_index].title()]["Average Male Weight"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])>int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])<int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==3:
                    if dog_Key["Year of Recognition"]==data[guessed_dogs[dog_index].title()]["Year of Recognition"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])>int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])<int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==4:
                    if dog_Key["Popularity Rank"]==data[guessed_dogs[dog_index].title()]["Popularity Rank"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])>int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])<int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==5:
                    if dog_Key["Place of Origin"][0]==data[guessed_dogs[dog_index].title()]["Place of Origin"][0]:
                        SCREEN.blit(correct, (curr_rect))
                    elif dog_Key["Place of Origin"][1]==data[guessed_dogs[dog_index].title()]["Place of Origin"][1]:
                        SCREEN.blit(correct_continent, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
        elif dog_index==5:
            for i in range(6):
               
                curr_rect = pygame.Rect((rects[5][i][0], rects[5][i][1]), (RECT_WIDTH, RECT_HEIGHT))                    
               
                if i==0:
                    if dog_Key["Group"]==data[guessed_dogs[dog_index].title()]["Group"]:
                        SCREEN.blit(correct, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
                if i==1:
                    if dog_Key["Average Male Height"]==data[guessed_dogs[dog_index].title()]["Average Male Height"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Height"])>int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Height"])<int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==2:
                    if dog_Key["Average Male Weight"]==data[guessed_dogs[dog_index].title()]["Average Male Weight"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])>int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])<int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==3:
                    if dog_Key["Year of Recognition"]==data[guessed_dogs[dog_index].title()]["Year of Recognition"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])>int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])<int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==4:
                    if dog_Key["Popularity Rank"]==data[guessed_dogs[dog_index].title()]["Popularity Rank"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])>int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])<int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==5:
                    if dog_Key["Place of Origin"][0]==data[guessed_dogs[dog_index].title()]["Place of Origin"][0]:
                        SCREEN.blit(correct, (curr_rect))
                    elif dog_Key["Place of Origin"][1]==data[guessed_dogs[dog_index].title()]["Place of Origin"][1]:
                        SCREEN.blit(correct_continent, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
        elif dog_index==6:
            for i in range(6):
               
                curr_rect = pygame.Rect((rects[6][i][0], rects[6][i][1]), (RECT_WIDTH, RECT_HEIGHT))                    
               
                if i==0:
                    if dog_Key["Group"]==data[guessed_dogs[dog_index].title()]["Group"]:
                        SCREEN.blit(correct, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
                if i==1:
                    if dog_Key["Average Male Height"]==data[guessed_dogs[dog_index].title()]["Average Male Height"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Height"])>int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Height"])<int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==2:
                    if dog_Key["Average Male Weight"]==data[guessed_dogs[dog_index].title()]["Average Male Weight"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])>int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])<int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==3:
                    if dog_Key["Year of Recognition"]==data[guessed_dogs[dog_index].title()]["Year of Recognition"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])>int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])<int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==4:
                    if dog_Key["Popularity Rank"]==data[guessed_dogs[dog_index].title()]["Popularity Rank"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])>int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])<int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==5:
                    if dog_Key["Place of Origin"][0]==data[guessed_dogs[dog_index].title()]["Place of Origin"][0]:
                        SCREEN.blit(correct, (curr_rect))
                    elif dog_Key["Place of Origin"][1]==data[guessed_dogs[dog_index].title()]["Place of Origin"][1]:
                        SCREEN.blit(correct_continent, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
        elif dog_index==7:
            for i in range(6):
               
                curr_rect = pygame.Rect((rects[7][i][0], rects[7][i][1]), (RECT_WIDTH, RECT_HEIGHT))                    
               
                if i==0:
                    if dog_Key["Group"]==data[guessed_dogs[dog_index].title()]["Group"]:
                        SCREEN.blit(correct, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
                if i==1:
                    if dog_Key["Average Male Height"]==data[guessed_dogs[dog_index].title()]["Average Male Height"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Height"])>int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Height"])<int(data[guessed_dogs[dog_index].title()]["Average Male Height"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==2:
                    if dog_Key["Average Male Weight"]==data[guessed_dogs[dog_index].title()]["Average Male Weight"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])>int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Average Male Weight"])<int(data[guessed_dogs[dog_index].title()]["Average Male Weight"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==3:
                    if dog_Key["Year of Recognition"]==data[guessed_dogs[dog_index].title()]["Year of Recognition"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])>int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Year of Recognition"])<int(data[guessed_dogs[dog_index].title()]["Year of Recognition"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==4:
                    if dog_Key["Popularity Rank"]==data[guessed_dogs[dog_index].title()]["Popularity Rank"]:
                        SCREEN.blit(correct, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])>int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(higher, (curr_rect))
                    elif int(dog_Key["Popularity Rank"])<int(data[guessed_dogs[dog_index].title()]["Popularity Rank"]):
                        SCREEN.blit(lower, (curr_rect))
                if i==5:
                    if dog_Key["Place of Origin"][0]==data[guessed_dogs[dog_index].title()]["Place of Origin"][0]:
                        SCREEN.blit(correct, (curr_rect))
                    elif dog_Key["Place of Origin"][1]==data[guessed_dogs[dog_index].title()]["Place of Origin"][1]:
                        SCREEN.blit(correct_continent, (curr_rect))
                    else:
                        SCREEN.blit(incorrect, (curr_rect))
                       
def create_List(file_name):
    """
    Parameters
    ----------
    file_name : STRING
        A list of the dogs that the user has guessed.
   
    Returns
    -------
    dog : DICTIONARY
        a dictionary of the stats of the secret dog
    Dog_List : LIST
        a list of all of the names of the dogs
    data : NESTED DICTIONARY
        a nested dictionary containing the names and stats of every dog
   
    Functions
    ---------
    Creates the various lists and dictionaries used to handle the bank of dogs
   
    Authored
    --------
    Fully Written by Sage

    """
   
    data={}

    with open(file_name, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            keyname=row[0].title()
            key={}
            key={
                "Name":row[0].title(),"Group":row[1],"Average Male Height":row[2],
                "Average Male Weight":row[3],"Year of Recognition":row[4],
                "Popularity Rank":row[5],"Place of Origin":[row[6],row[7]]}
            data[keyname]=key

    dict_list=data.keys()
    Dog_List=[]
    for i in dict_list:
        Dog_List.append(i)
        dog=data[random.choice(Dog_List)]
    return dog,Dog_List,data

def draw_title(font):
    """
    Parameters
    ----------
    font: FONT
        the font used to display print the title
   
    Returns
    -------
   
    Functions
    ---------
    prints the title
   
    Authored
    --------
    Fully Written by Seth
    """
    pygame.draw.line(SCREEN, WHITE, (BASE_OFFSET_X-RECT_WIDTH, BASE_OFFSET_Y-RECT_HEIGHT),
                     (BASE_OFFSET_X + (RECT_WIDTH*(NUM_COLS+1)) + (DX*(NUM_COLS-1)), BASE_OFFSET_Y-RECT_HEIGHT), width=1)
    title_surface = font.render("DOGDLE", True, WHITE)
    SCREEN.blit(title_surface, (BASE_OFFSET_X, BASE_OFFSET_Y-(RECT_HEIGHT*3)))

if __name__ == "__main__":
    main()
