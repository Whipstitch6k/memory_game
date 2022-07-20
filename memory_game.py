import random

class Card:
  def __init__(self, value):
    self.value = value
    self.flipped = False #is the card flipped so that the value is facing up on the board
    self.showing = False #has the card's match been found

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
    x_coord = ord(player_coord[0])-65
    y_coord = int(player_coord[1])
    return [x_coord,y_coord]

  def validate_player_coord(self, player_coord):
    list_coord = self.convert_player_coord_to_list_coord(player_coord)
    if (list_coord[0] > len(self.game_grid[0])) or (list_coord[1] > len(self.game_grid[1])):
      print ("invalid coordinate")
      return False
    else:
      print ("valid coord")
      return True

class Game_grid_gui(Game_grid):
  pass



class Player:
  def __init__(self):
    self.score = 0;



class Memory_game:
  def __init__(self, player_count, grid_size):
    self.players = self.intialize_players(player_count) #list of Player objects
    self.game_grid_object = Game_grid(grid_size)
    self.gamestate = True #True == game in progress, False == game has ended

  def intialize_players(self, player_count):
    player_list = []
    for i in range(player_count):
      player_list.append(Player)
    return player_list

  def play_game(self):
    current_player = self.players[0]
    while self.gamestate:
      print("playing")
      #say which player
      #take first input
      #update display
      #take second input
      #update display
      #check match
        #if match
          #update score
          #set cards matched
          #player takes another turn
        #else
          #delay flipping the cards back
          #flip cards back
      #cycle to next player

      #note to self: maybe have play_game part of the super function but player turn part of the child function
      self.gamestate = False

class Memory_game_console(Memory_game):
  def __init__(self, player_count, grid_size):
    super().__init__(player_count, grid_size)
    self.game_grid_object = Game_grid_console(grid_size)

class Memory_game_gui(Memory_game):
  pass



#create a new game with known grid size
print("starting")
memory_game = Memory_game_console(1,[2,3])
memory_game.game_grid_object.display_game_grid()
memory_game.play_game()

#test_grid = Game_grid_console([2,3])
#test_grid.display_game_grid()
#print(test_grid.game_grid)
#test_grid.validate_player_coord("D2")