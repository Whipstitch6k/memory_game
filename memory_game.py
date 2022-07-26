import random
import time
import os #for console version clear screen, currently uses clear (unix)
from tkinter import *    #using tikinter for the gui because it's simple and comes with python
from tkinter import ttk

class Card:
  def __init__(self, value):
    self.value = value
    self.flipped = False #is the card flipped so that the value is facing up on the board
    self.matched = False #has the card's match been found

  def __str__(self):
    return f'{self.value}'

  def __repr__(self):
    return f'{self.value}' #TODO: add other statuses. Using value only for easier reading when calling Game_board



class Game_grid:
  #grid_size = array [grid_width, grid_height]
  def __init__(self, grid_size):
    self.game_grid = self.initialze_game_grid(grid_size)

  def initialze_game_grid(self, grid_size):
    #start by creating a deck, 1D list of paired Card objects (value is a character), in order (ie [A, A, B, B, C, C])
    #the algorithm used does still generate workable grids when given an odd grid (ie a 3x3 grid has 9 spaces, but the algorithm creates 8 cards)
    deck = [];
    current_char = 'A'
    card_count = grid_size[0]*grid_size[1]
    for i in range(0,card_count-1,2):
      deck.append(Card(current_char))
      deck.append(Card(current_char)) #do it twice so there's matching cards
      current_char = chr(ord(current_char)+1) #incriment current_char. Note: as currently written, for decks larger than 52 (26*2), this will go past letters

    random.shuffle(deck)
    
    #convert into 2D list of size grid_size using List Comprehension (https://docs.python.org/2/tutorial/datastructures.html#list-comprehensions)
    grid = [deck[i:i+grid_size[0]] for i in range(0, len(deck), grid_size[0])]

    return grid

  #returns true if all matches have been made
  def verify_all_matches_made(self):
    for i in self.game_grid:
      for j in i:
        if not j.matched:
          return False
    return True

class Game_grid_console(Game_grid):

  #print the grid like this (in example A1 is flipped, all others not)
  #    1   2  
  #A  [B] [ ]
  #B  [ ] [ ]
  #C  [ ] [ ]
  def display_game_grid(self):
    #print column labels.
    line_string = "   "
    for i in range (len(self.game_grid[0])):
      line_string += ' ' + str(i+1) + '  '
    print(line_string)

    #print each row with a leading row label
    row_name = 'A'
    for i in self.game_grid:
      line_string = row_name + ' '
      for j in i:
        displayed_card_value = " "
        if j.flipped:
          displayed_card_value = j.value
        line_string += ' [' + displayed_card_value + ']'
      row_name = chr(ord(row_name)+1)
      print(line_string)

  #converts player_coord (ie "A2") into list_coord (ie [0,1])
  #note: as written only works for boards smaller than 26x10
  def convert_player_coord_to_list_coord(self, player_coord):
    x_coord = ord(player_coord[0])-65 #"A" is ascii 65
    y_coord = int(player_coord[1])-1 #subtract to move from 1 base to 0 base
    return [x_coord,y_coord]

  #validates player_coord (ie "A2") is within board range (ie D3 on a 2x2 board would not be in range)
  #returns true if valid, false if invalid
  def validate_player_coord(self, player_coord):
    list_coord = self.convert_player_coord_to_list_coord(player_coord)
    if (list_coord[0] > len(self.game_grid[0])) or (list_coord[1] >= len(self.game_grid[1])):
      return False
    else:
      return True



class Player:
  def __init__(self,name):
    self.name = name
    self.score = 0;



class Memory_game:
  def __init__(self, player_count, grid_size):
    self.players = self.intialize_players(player_count) #list of Player objects
    self.game_grid_object = Game_grid(grid_size)
    self.gamestate = True #True == game in progress, False == game has ended

  def intialize_players(self, player_count):
    player_list = []
    for i in range(player_count):
      player_list.append(Player("Player " + str(i+1)))
    return player_list

  #goes to next player. If at last player, cycles back to first player
  #returns Player object
  def cycle_to_next_player(self, current_player):
    current_player_index = self.players.index(current_player)
    current_player_index +=1
    if current_player_index >= len(self.players):
      current_player_index = 0
    return self.players[current_player_index]

  def play_game(self):
    self.game_start_message()
    current_player = self.players[0]
    while self.gamestate:
      #display current player
      self.display_current_player(current_player)

      #display grid
      self.game_grid_object.display_game_grid()

      #take card choice
      card_choice1_grid_coord = self.accept_and_process_player_input()
      card_choice1 = self.game_grid_object.game_grid[card_choice1_grid_coord[0]][card_choice1_grid_coord[1]]

      #update correct card
      card_choice1.flipped = True

      #update display
      self.game_grid_object.display_game_grid()

      #take card choice
      card_choice2_grid_coord = self.accept_and_process_player_input()
      card_choice2 = self.game_grid_object.game_grid[card_choice2_grid_coord[0]][card_choice2_grid_coord[1]]

      #update correct card
      card_choice2.flipped = True

      #update display
      self.game_grid_object.display_game_grid()
      
      #check match
      if card_choice1.value == card_choice2.value:
        current_player.score +=1
        card_choice1.matched = True
        card_choice2.matched = True
        #player takes another turn, don't update player

      else:
        card_choice1.flipped = False
        card_choice2.flipped = False
        current_player = self.cycle_to_next_player(current_player)

      #verify all matches are not yet made and game is still ongoing
      self.gamestate = not self.game_grid_object.verify_all_matches_made()

    #finish game
    self.finish_game()

class Memory_game_console(Memory_game):
  def __init__(self, player_count, grid_size):
    super().__init__(player_count, grid_size)
    self.game_grid_object = Game_grid_console(grid_size)

  def game_start_message(self):
    print("Welcome to Concentration")
    print("inputs are letter, then number, ie 'A2'")
    print("") #newline

  def display_current_player(self, current_player):
    time.sleep(2)
    os.system("clear")
    print(current_player.name)
    print("Score: " + str(current_player.score))

  #takes player input, validates, returns converted choice (ie A2 = [0,1])
  def accept_and_process_player_input(self):
    input_valid = False
    while(not input_valid):
      player_card_choice = input("please select a card: ")
      converted_card_choice = self.game_grid_object.convert_player_coord_to_list_coord(player_card_choice)
      
      range_valid = self.game_grid_object.validate_player_coord(player_card_choice)
      if range_valid:
        card_flipped_status = self.game_grid_object.game_grid[converted_card_choice[0]][converted_card_choice[1]].flipped
      
      if not range_valid:
        print("invalid range")
      elif card_flipped_status:
        print("card already flipped")
      else:
        input_valid = True

    return converted_card_choice

  def finish_game(self):
    print("Final Score:")
    for i in self.players:
      print(i.name + ": " + str(i.score))



class Memory_game_gui(Memory_game):
  def __init__(self, player_count, grid_size):
    super().__init__(player_count, grid_size)
    #self.game_grid_object = Game_grid_gui(grid_size)
    self.current_player = self.players[0]
    self.current_player_phase = 0 # 0 = no selections yet, 1= one selection made, 2 = both selections made
    self.current_player_selections = [] #list, of cards player selects this turn, returns to empty after turn
    
    #setup window and grid
    self.root = Tk()
    self.frame = ttk.Frame(self.root, padding=10) #create frame
    self.frame.grid()


  def play_game(self):

    self.display_game_grid()

    self.root.mainloop()


  def display_game_grid(self):

    for i in self.game_grid_object.game_grid:
      for j in i:
        if j.flipped:
          displayed_card_value = j.value
        else:
          displayed_card_value = " "
        button_coord = [i.index(j), self.game_grid_object.game_grid.index(i)]
        ttk.Button(self.frame, text=displayed_card_value, command=lambda button_coord_to_pass = button_coord: self.advance_game_state(button_coord_to_pass)).grid(column=button_coord[0], row=button_coord[1])
    ttk.Label(self.frame, text=self.current_player.name).grid(column=0, row=len(self.game_grid_object.game_grid[0])+1)
    ttk.Label(self.frame, text="Score: " + str(self.current_player.score)).grid(column=0, row=len(self.game_grid_object.game_grid[0])+2)


  def advance_game_state(self, grid_coord):
    self.current_player_selections.append(self.game_grid_object.game_grid[grid_coord[1]][grid_coord[0]])
    self.current_player_selections[-1].flipped = True
    self.display_game_grid()

    if self.current_player_phase == 1: #two selections have been made
      print()
      if self.current_player_selections[0].value == self.current_player_selections[1].value:
        self.current_player.score += 1
        self.current_player_selections[0].matched = True
        self.current_player_selections[1].matched = True
      else:
        self.current_player_selections[0].flipped = False
        self.current_player_selections[1].flipped = False
        self.current_player = self.cycle_to_next_player(self.current_player)
      
      self.current_player_selections = [] #reset for next turn

    self.advance_player_phase()

    if self.game_grid_object.verify_all_matches_made():
      self.finish_game()


  def advance_player_phase(self):
    self.current_player_phase += 1
    if self.current_player_phase >1:
      self.current_player_phase = 0


  #display a new window with final scores
  def finish_game(self):
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    current_row = 1
    ttk.Label(frm, text="Final Score:").grid(column=0, row=0)
    for i in self.players:
      ttk.Label(frm, text=i.name + ": " + str(i.score)).grid(column=0, row=current_row)
      current_row += 1
    root.mainloop()



#create a new game with known grid size

#switch these out to play console or gui
#args are(number_of_players, [grid_width, grid_height])
#memory_game = Memory_game_console(1,[2,3])
memory_game = Memory_game_gui(1,[2,3])

memory_game.play_game()


#notes on gui: At current, intead of doing a delay after a mismatch and then flipping the cards back, it flips the cards back after the next selection. In a multi-player game this is also when it updates the player currently playing. Usage of sleeps seems to cause it to sleep before the second card reveal no matter where I put the sleep. Also gui does not yet handle re-selecting an already flipped card. 

#console version is pretty solid but could be expanded on. Only works if inputs are a single letter followe dy a single number. Game won't work right if more wider than 9 columns