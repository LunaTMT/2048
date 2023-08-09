show_menu = True
handle_menu_buttons = True
dissolve_buttons = False
play_game = False

def reset():
    global show_menu
    global handle_menu_buttons
    global dissolve_buttons
    global play_game

    show_menu = True
    handle_menu_buttons = True
    dissolve_buttons = False
    play_game = False

def initiate_game():
    global show_menu
    global dissolve_buttons
    global play_game
    
    show_menu = False
    dissolve_buttons = False
    play_game = True