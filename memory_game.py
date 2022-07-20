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

  #print the grid like this (in example A1 is flipped, all others not)
  #    1   2  
  #A  [B] [ ]
  #B  [ ] [ ]
  #C  [ ] [ ]
  def display_game_grid_console(self):
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




#need a game class
  #gamestate variable (ongoing, finished), while gamestate == ongoing
  #player object containing score
  #turn method
  #display grid method
  

#create a new game with known grid size
print("starting")
test_grid = Game_grid([2,3])
test_grid.display_game_grid_console()
print(test_grid.game_grid)