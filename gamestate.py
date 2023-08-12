show_menu = True
handle_menu_buttons = True
dissolve_buttons = False

play_game = False

end_game = lose = win = False


def return_to_menu():
    global show_menu
    global handle_menu_buttons
    global dissolve_buttons
    global play_game
    global win 
    global lose
    global end_game

    show_menu = True
    handle_menu_buttons = True
    dissolve_buttons = False
    play_game = False
    end_game  = lose = win = False

def initiate_game():
    global show_menu
    global dissolve_buttons
    global play_game
    
    show_menu = False
    dissolve_buttons = False
    play_game = True

def reset_endgame_states():
    global win 
    global lose
    global end_game

    end_game  = lose = win = False