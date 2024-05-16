import numpy as np
import pygame
import sys
import time
import copy
import random
import math

import six_men_morris as smm

HEIGHT = 5
WIDTH = 5

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)
RED = "#FF7276"
YELLOW = "#FFF36D"
BG = "#203972"
BLUE = "#3E5AAA"


board = smm.create_board()


#Player Initialization
user = None
ai_turn = False
player = smm.p1
all_pieces_placed = False
clicked_piece = (None, None)
free_slots = set()
line_forms = set()
pieces_can_remove = set()
line_moved = False
temp_line_forms = set()

ai_mills = set()
player_mills = set()

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# Draw board
def draw_board():
    pygame.draw.rect(screen, BLUE, ((20,20), (680,680)))
    pygame.draw.rect(screen, BG, ((220,220), (280,280)), 5)
    pygame.draw.rect(screen, BG, ((87,87), (550,550)), 5)
    pygame.draw.line(screen, BG, (85, (board_width/2-47)), (225, board_width/2-47), 5)
    pygame.draw.line(screen, BG, (495, (board_width/2-47)), (635, board_width/2-47), 5)
    pygame.draw.line(screen, BG, (board_width/2-47, 85), (board_width/2-47, 220), 5)
    pygame.draw.line(screen, BG, (board_width/2-47, 500), (board_width/2-47, 635), 5)

    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            circle = (
                board_origin[0] + j * cell_size + 68,
                board_origin[1] + i * cell_size + 68,
            )

            if board[i][j] != smm.X:
                pygame.draw.circle(screen, BG, circle, 15)

                if board[i][j] == smm.EMPTY and not all_pieces_placed:
                    pygame.draw.circle(screen, WHITE, circle, 40, 3)
            
            # Draw red pieces
            if board[i][j] == smm.p1:
                pygame.draw.circle(screen, RED, circle, 40)

            # Draw yellow pieces
            if board[i][j] == smm.p2:
                pygame.draw.circle(screen, YELLOW, circle, 40)
            
            # Highlight clicked piece
            if (i,j) == clicked_piece:
                pygame.draw.circle(screen, BLACK, circle, 40, 3)

            # Highlight possible moves
            if (i,j) in free_slots:
                pygame.draw.circle(screen, WHITE, circle, 40, 3)


            # Highlight enemy pieces that can be removed
            if (i,j) in pieces_can_remove and (i,j) not in ai_mills:
                pygame.draw.circle(screen, BLACK, circle, 40, 3)
                

            row.append(rect)
        cells.append(row)

        # pygame.display.flip()


# Remove piece
def remove_piece(board, pos):
    """
    Removes piece from the board
    """
    result = copy.deepcopy(board)
    removed = False

    while(not removed):
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    if (cells[i][j].collidepoint(mouse) and (i,j) in pieces_can_remove):
                            result[pos[0]][pos[1]] = smm.EMPTY
                            time.sleep(0.3)
                            pieces_can_remove.clear()
                            removed = True 
    
    return result



# Create game
pygame.init()
size = width, height = 1280, 720
screen = pygame.display.set_mode(size)


smallFont = pygame.font.Font(None, 20)
mediumFont = pygame.font.Font(None, 28)
largeFont = pygame.font.Font(None, 40)
boldFont = pygame.font.Font(None, 80)


# Compute board size
BOARD_PADDING = 20
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# # Show instructions initially
# instructions = True



game_over = False

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BG)

    # Show game instructions
    if user is None:

        # Title
        title = boldFont.render("Play Six Men Morris", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Players take turns to place their pieces",
            "onto the empty spots on the board",
            "",
            "If your form a line of 3 pieces (a mill),",
            "click to remove one of the computer's pieces.",
            "Pieces of a formed mill cannot be removed",
            "unless no other pieces are left on the board."
        ]
        for i, rule in enumerate(rules):
            line = mediumFont.render(rule, True, WHITE)
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)


        # Play as red button
        play_red_button = pygame.Rect((width / 4)+50, 400, 200, 100)
        buttonText = mediumFont.render("Play as Red", True, WHITE)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = play_red_button.center
        pygame.draw.rect(screen, BLUE, play_red_button)
        screen.blit(buttonText, buttonTextRect)

        # Play as red button
        play_yellow_button = pygame.Rect((width / 4) + 350, 400, 200, 100)
        buttonText = mediumFont.render("Play as Yellow", True, WHITE)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = play_yellow_button.center
        pygame.draw.rect(screen, BLUE, play_yellow_button)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if play_red_button.collidepoint(mouse):
                time.sleep(0.2)
                user = smm.p1
            elif play_yellow_button.collidepoint(mouse):
                time.sleep(0.2)
                user = smm.p2

        pygame.display.flip()
        continue
    
    # Draw board
    cells = []
    draw_board()
    

    # Checks if all pieces are placed to the board
    if smm.p1_piece_count == 0 and smm.p2_piece_count == 0:
        all_pieces_placed = True

    # line = smm.line_forms(board, player)


    # Show title    
    if game_over:
        winner = smm.winner(board)
        title = f"Game Over: {winner} wins."
    elif user == player:
        title = f"Your turn"
    else:
        title = f"Computer thinking..."
    draw_text(title, largeFont, WHITE, screen, 800, 50)


    # ------------------ Draw players pieces ----------------------
    if not game_over:
        if user == smm.p1:
            draw_text("You", boldFont, WHITE, screen, 820, 120)
            draw_text("Computer", boldFont, WHITE, screen, 820, 440)
        elif user == smm.p2:
            draw_text("Computer", boldFont, WHITE, screen, 820, 120)
            draw_text("You", boldFont, WHITE, screen, 820, 440)

    for i in range(smm.p1_piece_count):
        pos = (
            850 + (i % 3) *100,
            250 + (i // 3) *100 
        )
        pygame.draw.circle(screen, RED, pos, 40)

    for i in range(smm.p2_piece_count):
        pos = (
            850 + (i % 3) *100,
            560 + (i // 3) *100 
        )
        pygame.draw.circle(screen, YELLOW, pos, 40)


    
    if not all_pieces_placed:
        # -------------------- Check for AI move ---------------------------
        if user != player:

            move = smm.pick_best_move(board, player)
            smm.put_piece(board, move, player)
            smm.subtract_piece(player)

            mill = smm.line_forms(board, player)
            
            if not mill.issubset(ai_mills):
                can_remove = smm.pieces_can_remove(board, player, ai_mills)
                remove = random.choice(list(can_remove))
                smm.remove_piece(board, remove)
                for pos in mill:
                    ai_mills.add(pos) 
            
            
            player = smm.change_player(player)


        # -------------------- Check for a user move -------------------------
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):

                    if (board[i][j] == smm.EMPTY and cells[i][j].collidepoint(mouse)):
                        smm.subtract_piece(player)
                        
                        smm.put_piece(board, (i,j), player)

                        line = smm.line_forms(board, player)

                        if not line.issubset(player_mills):
                            pieces_can_remove = smm.pieces_can_remove(board, player, ai_mills)
                            for pos in line:
                                player_mills.add(pos)
                        else:
                            player = smm.change_player(player)
                        

                    if (cells[i][j].collidepoint(mouse) and (i,j) in pieces_can_remove):
                        smm.remove_piece(board, (i,j))
                        pieces_can_remove.clear()
                        player = smm.change_player(player)

    else:
        game_over = smm.winner(board)
        # -------------------- Check for a user move -------------------------
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):



                    if board[i][j] == user and cells[i][j].collidepoint(mouse):
                        clicked_piece = (i, j)
                        free_slots = smm.moves(board, clicked_piece, player)
                        
                    if (cells[i][j].collidepoint(mouse) and (i,j) in free_slots):
                        smm.move_piece(board, clicked_piece, (i,j), player)
                        if clicked_piece in player_mills:
                            player_mills.clear()
                        
                        line = smm.line_forms(board, player)

                        if not line.issubset(player_mills):
                            pieces_can_remove = smm.pieces_can_remove(board, player, ai_mills)
                            for pos in line:
                                player_mills.add(pos)
                        else:
                            player = smm.change_player(player)
                            pass
                        

                    if (cells[i][j].collidepoint(mouse) and (i,j) in pieces_can_remove):
                        smm.remove_piece(board, (i,j))
                        pieces_can_remove.clear()
                        player = smm.change_player(player)

        # -------------------- Check for AI move ---------------------------
        if user != player and not game_over:
            time.sleep(0.5)

            # piece_to_move = random.choice(list(smm.pieces_can_move(board, player)))
            # move = random.choice(list(smm.moves(board, piece_to_move, player)))

            mill = smm.line_forms(board, player)
            
            if not mill.issubset(ai_mills):
                for pos in mill:
                    ai_mills.add(pos)

            action, minimax_score = smm.minimax(board, 5, -math.inf, math.inf, True, player, ai_mills, player_mills)

            print("the action is: ", action)
            
            # if action[2]:
            #     print("piece was removed")
            #     # smm.move_piece(board, action[0], action[1], player)
            #     smm.remove_piece(board, action[2])
            # elif action[2] == None:
            #     print("piece was moved")
            #     smm.move_piece(board, action[0], action[1], player)
            #     mill = smm.line_forms(board, player)
            #     if not mill.issubset(ai_mills):
            #         for pos in mill:
            #             ai_mills.add(pos)
            #         # can_remove = smm.pieces_can_remove(board, player, player_mills)
            #         # remove = random.choice(list(can_remove))
            #         action, minimax_score = smm.minimax(board, 1, -math.inf, math.inf, True, player, ai_mills, player_mills)
            #         smm.remove_piece(board, action[2])
            

            if action[2]:
                print("piece was removed")
                smm.move_piece(board, action[0], action[1], player)
                smm.remove_piece(board, action[2])
            elif action[2] == None:
                print("piece was moved")
                smm.move_piece(board, action[0], action[1], player)
                
            print("Ai mills: ", ai_mills)
            print("Player mills: ", player_mills)
            
            if action[0] in ai_mills:
                ai_mills.clear()

            # mill = smm.line_forms(board, player)
            
            # if not mill.issubset(ai_mills):
            #     for pos in mill:
            #         ai_mills.add(pos)
            #     can_remove = smm.pieces_can_remove(board, player, player_mills)
            #     remove = random.choice(list(can_remove))
            #     board = smm.remove_piece(board, remove)
                
                     
            player = smm.change_player(player)

        """
        # -------------------- Check for AI move ---------------------------
        if user != player and not game_over:
            if ai_turn:
                

                
                time.sleep(0.5)
                
                line = smm.line_forms(board, player)
                # print(line)

                if not line.issubset(line_forms):
                    move = smm.minimax(board, player)
                    board = smm.result(board, move, player)


                    player = smm.change_player(player)

                    for pos in line:
                        line_forms.add(pos)
                else:
                    move = smm.minimax(board, player)
                    board = smm.result(board, move, player)

                    smm.subtract_piece(player)
                    line = smm.line_forms(board, player)


                    if not line.issubset(line_forms):
                        move = smm.minimax(board, player)
                        board = smm.result(board, move, player)
                        for pos in line:
                            line_forms.add(pos)



                # if not line.issubset(line_forms):
                #     ai_turn = True
                #     for pos in line:
                #         line.add(pos)
                # else:
                player = smm.change_player(player)

                ai_turn = False
            else:
                ai_turn = True

        # -------------------- Check for a user move -------------------------
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):
                    # line = smm.line_forms(board, user)

                    # if not line.issubset(smm.mills):
                        
                    if (board[i][j] == smm.EMPTY and cells[i][j].collidepoint(mouse)):
                        smm.subtract_piece(player)
                        move = [(i, j), None, None]
                        board = smm.result(board, move, player)

                        line = smm.line_forms(board, player)
                        if not line.issubset(smm.user_mills):
                            pieces_can_remove = smm.pieces_can_remove(board, player, line)
                            for pos in line:
                                smm.user_mills.add(pos) 
                        else:
                            player = smm.change_player(player)
                        

                    if (cells[i][j].collidepoint(mouse) and (i,j) in pieces_can_remove):
                        board = smm.remove_piece(board, (i,j))
                        pieces_can_remove.clear()


                        player = smm.change_player(player)
    """

    """
    # ------- instructions if all pieces are not yet placed ----------
    if not all_pieces_placed:
        # -------------------- Check for AI move ---------------------------
        if user != player and not game_over:
            if ai_turn:
                line = smm.line_forms(board, user)

                print(line)

                if not line.issubset(line_forms):
                    print("line forms")
                    ai_turn = False
                    player = smm.change_player(player)
                # elif smm.line_forms(board, player):  
                #     time.sleep(0.5)
                #     move = smm.minimax(board, player)
                #     board = smm.result(board, move, player)
                #     player = smm.change_player(player)
                #     ai_turn = False
                else:
                    print("gumawa ng move Ai")
                    time.sleep(0.5)
                    smm.subtract_piece(player)
                    move = smm.minimax(board, player)
                    board = smm.result(board, move, player)
                    player = smm.change_player(player)
                    ai_turn = False
            else:
                ai_turn = True
                        


        # -------------------- Check for a user move -------------------------
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1 and user == player and not game_over:
            mouse = pygame.mouse.get_pos()
            for i in range(HEIGHT):
                for j in range(WIDTH):

                    line = smm.line_forms(board, player)
                    # print(line)
                    if not line.issubset(line_forms):
                    # if line:
                        print("burat")
                        pieces_can_remove = smm.pieces_can_remove(board, player, line)
                        print(pieces_can_remove)

                        if (cells[i][j].collidepoint(mouse) and (i,j) in pieces_can_remove):
                            print("REMOVED")
                            board = remove_piece(board, (i,j))
                            player = smm.change_player(player)

                            # line.clear()
                            # pieces_can_remove.clear()

                            for pos in line:
                                line_forms.add(pos)                        
                    elif (board[i][j] == smm.EMPTY and cells[i][j].collidepoint(mouse)):
                        smm.subtract_piece(player)
                        move = [(i, j), None, None]
                        board = smm.result(board, move, player)
                        player = smm.change_player(player)

    """








    # # -------------------- Check for AI move ---------------------------
    # if user != player and not game_over:
    #     if ai_turn and not all_pieces_placed:
    #         time.sleep(0.5)
    #         # smm.subtract_piece(player)
    #         move = smm.minimax(board, player)
    #         board = smm.result(board, move, player)
    #         player = smm.change_player(player)
    #         ai_turn = False
    #     elif ai_turn and all_pieces_placed:
    #         player = smm.change_player(player)              #TEMPORARY
    #     else:
    #         ai_turn = True



    # click, _, _ = pygame.mouse.get_pressed()
    # if click == 1 and user == player and not game_over:
    #     mouse = pygame.mouse.get_pos()
    #     for i in range(HEIGHT):
    #         for j in range(WIDTH):
    #             line_forms = smm.line_forms(board, player)
    #             if line_forms:
    #                 pieces_can_remove = smm.pieces_can_remove(board, player, line_forms)
    #                 if (cells[i][j].collidepoint(mouse) and (i,j) in pieces_can_remove):
    #                     print("REMOVED")
    #                     board = smm.remove_piece(board, (i,j))
    #                     time.sleep(0.3)
    #                     pieces_can_remove.clear


    # -------------------- Check for a user move -------------------------
    # click, _, _ = pygame.mouse.get_pressed()
    # if click == 1 and user == player and not game_over:
    #     mouse = pygame.mouse.get_pos()
    #     for i in range(HEIGHT):
    #         for j in range(WIDTH):
                

    #             if not all_pieces_placed:
    #                 line_moved = True

    #             line_forms = smm.line_forms(board, player)
    #             if line_forms and line_moved or len(line_forms) == 5:
    #                 pieces_can_remove = smm.pieces_can_remove(board, player, line_forms)
    #                 if (cells[i][j].collidepoint(mouse) and (i,j) in pieces_can_remove):
    #                     print("REMOVED")
    #                     board = smm.remove_piece(board, (i,j))
    #                     time.sleep(0.3)
    #                     pieces_can_remove.clear()

    #                     line_moved = False


    #             elif (board[i][j] == smm.EMPTY and cells[i][j].collidepoint(mouse) and not all_pieces_placed):
    #                 board = smm.result(board, (i, j), player)
    #                 line_moved = True

    #                 player = smm.change_player(player)
    #             elif (board[i][j] == user and cells[i][j].collidepoint(mouse) and all_pieces_placed):
    #                 clicked_piece = (i, j)
    #                 free_slots = smm.moves(board, clicked_piece, player)
                    
    #             if (cells[i][j].collidepoint(mouse) and (i,j) in free_slots):
    #                 print("clicked")
    #                 board = smm.result(board, (i, j), player, clicked_piece)
    #                 if clicked_piece in line_forms:
    #                     line_moved = True






                
                    

    pygame.display.flip()
