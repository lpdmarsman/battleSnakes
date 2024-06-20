# Welcome to
# __________         __    __  .__                          https://Battlesnake-1.bobswag1.repl.co     __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
# Made by Howie Lo I suppose
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing

# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#2877D1",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "pixel",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    #Need boolean operators, incase we find ourselves in a situtation where the math tells us moving into a wall is the most optimal solution (just in case)
    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }
    #We should have a check to determine how good a route possibly is

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    my_health = game_state["you"]["health"]
    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    if my_head["x"] == 0:
      is_move_safe["left"] = False
    elif my_head["x"] == board_width - 1:
      is_move_safe["right"] = False

    if my_head["y"] == 0:
      is_move_safe["down"] = False
    elif my_head["y"] == board_height - 1:
      is_move_safe["up"] = False
  #print(game_state["you"]["body"])
    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    #print(my_body)
    for body_part in my_body:
      #left
      if {"x": my_head["x"]-1, "y": my_head["y"]} == body_part:
        is_move_safe["left"] = False
      #right
      if {"x": my_head["x"]+1, "y": my_head["y"]} == body_part:
        is_move_safe["right"] = False
      #up
      if {"x": my_head["x"], "y": my_head["y"]+1} == body_part:
        is_move_safe["up"] = False
      #down
      if {"x": my_head["x"], "y": my_head["y"]-1} == body_part:
        is_move_safe["down"] = False
        
      #DeprecationWarning
    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    #my_length = game_state["you"]["length"]
    #print(opponents)
    for opponent_body in opponents:
        #TODO: include check to see if I ram into an opponents head, if I do then do it if I have more length we continue 
        
        #left
        if {"x": my_head["x"]-1, "y": my_head["y"]} in opponent_body["body"]:
          is_move_safe["left"] = False
                      
        #right
        if {"x": my_head["x"]+1, "y": my_head["y"]} in opponent_body["body"]:
          is_move_safe["right"] = False
         
        #up
        if {"x": my_head["x"], "y": my_head["y"]+1} in opponent_body["body"]:
          is_move_safe["up"] = False
            
        #down
        if {"x": my_head["x"], "y": my_head["y"]-1}in opponent_body["body"]:
          is_move_safe["down"] = False
          
    #print(is_move_safe)
      # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    best_path = -999999
    path_choice = optimal_route(game_state)
    for direction in path_choice:
      if (path_choice[direction] > best_path) and direction in safe_moves:
        next_move = direction
        best_path = path_choice[direction]

  
    food = game_state['board']['food']
    #print(f"{food} those are the food locations")
    if my_health < 30:
      next_move_test = food_search_dh(my_head, food,safe_moves)
      if next_move_test in safe_moves:
        next_move = next_move_test
    #print(f"MOVE {game_state['turn']}: {next_move}")

  
    #print(f"next move is {next_move}")
    return {"move": next_move}

#This Food search is if food is below 25 and our snake boy is desperate food, calculates the shortest possible path with minimum concern regarding safety
def food_search_dh(head: typing.Dict, food_loc: list, safe_moves: list) -> typing.Dict:
  shortest_path = {"x": 10000, "y": 10000, "steps": 100000}
  for food in food_loc:
    path_len = (abs(head["x"] - food["x"]) + abs(head["y"] - food["y"]))
    #print(path_len)
    #print(food)
    #print(f"{head} head value")
    if path_len < shortest_path["steps"]:
      shortest_path["x"] = food["x"]
      shortest_path["y"] = food["y"]
      shortest_path["steps"] = path_len
    #print(f"{shortest_path} shortest path value")
    #print(f"{safe_moves} save moves")
      #left
  if (abs(head["x"]-1 - shortest_path["x"]) < abs(head["x"] - shortest_path["x"])) and ("left" in safe_moves):
    #print("1 is")
    return "left"
      #right
  if (abs(head["x"]+1 - shortest_path["x"]) < abs(head["x"] - shortest_path["x"])) and ("right" in safe_moves):
    #print("2 is")
    return "right"
      #up
  if (abs(head["y"] - 1 - shortest_path["y"]) < abs(head["y"] - shortest_path["y"])) and ("down" in safe_moves):
    #print("3 is")
    return "down"
  if (abs(head["y"] + 1 - shortest_path["y"]) < abs(head["y"] - shortest_path["y"])) and ("up" in safe_moves):
    #print("4 is")
    return "up"
    
    
    
#if this function worked it would be more complicated, predicting enemy movements and seeing if their path was more optimal then mine
def food_search_nd(head: typing.Dict, food_loc: list) -> typing.Dict:
  print("oh")

def snake_head_mov(head: typing.Dict) -> list:
  return [{'x': head['x'] + 1, 'y': head['y']}, {'x': head['x'] - 1, 'y': head['y']}, {'x': head['x'], 'y': head['y'] + 1}, {'x': head['x'], 'y': head['y'] - 1}, {'x': head['x'] + 1, 'y': head['y'] + 1}, {'x': head['x'] -1, 'y': head['y'] -1}, {'x': head['x'] + 1, 'y': head['y'] - 1}, {'x': head['x'] - 1, 'y': head['y'] + 1}]





#########################################################3





def danger_zone(game_state: typing.Dict) -> list:
  #11x11 board, max 121 tiles, or things we need to append. That probably negligable
  murder_zone = []
  my_body = game_state['you']['body']
  for body_part in my_body:
    murder_zone.append(body_part)

  opponents = game_state['board']['snakes']
  for opponent_body in opponents:
    for enemy_parts in opponent_body["body"]:
      murder_zone.append(enemy_parts)
      
  #not needed probably
  #murder_zone.append(bonus)

  return murder_zone


def bfs_pos(game_state: typing.Dict, murder_zone: list, length: int, size: int, cur: typing.Dict) -> int:
    #from ipdb import set_trace; set_trace();
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    #print(murder_zone)
    length += 1
    if (cur in murder_zone) or (length >= size + 50):
      return length
    murder_zone.append(cur)
    max = 0
    
    if cur["x"] != 0:
      length = bfs_pos(game_state, murder_zone, length, size, {"x": cur["x"] - 1, "y": cur["y"]})
      if length > max:
        max = length
        
    if cur["x"] != board_width - 1:
      length = bfs_pos(game_state, murder_zone, length, size, {"x": cur["x"] + 1, "y": cur["y"]})
      if length > max:
        max = length
        
    if cur["y"] != board_height - 1:
      length = bfs_pos(game_state, murder_zone, length, size, {"x": cur["x"], "y": cur["y"] + 1})
      if length > max:
        max = length
        
    if cur["y"] != 0:
      length = bfs_pos(game_state, murder_zone, length, size, {"x": cur["x"], "y": cur["y"] - 1})  
      if length > max:
        max = length

    return max
      







#######################################



  

def optimal_route(game_state: typing.Dict):


    is_move_optimal = {
        "up": 0, 
        "down": 0, 
        "left": 0, 
        "right": 0,
    #route is a list of dictionarys that show the possible paths
       # "route": [] nvm don't need lol
    }
  
    my_head = game_state["you"]["body"][0]
    #my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    #my_health = game_state["you"]["health"]
    opponents = game_state['board']['snakes']
    my_length = game_state["you"]["length"]
    elim_bonus = 5
    #print(opponents)
    for opponent_body in opponents:
      opponent_head_pos = snake_head_mov(opponent_body["head"])
      #print(f"{opponent_head_pos} these are the opponents head")
      #print(f"{my_head} these are the my head")
    #left 
      if ({"x": my_head["x"]-1, "y": my_head["y"]} in opponent_head_pos) and (my_length > opponent_body["length"] + 1):
        is_move_optimal["left"] += elim_bonus
      elif({"x": my_head["x"]-1, "y": my_head["y"]} in opponent_head_pos) and (my_length <= opponent_body["length"] + 1):
        is_move_optimal["left"] -= 500
    #right
      if ({"x": my_head["x"]+1, "y": my_head["y"]} in opponent_head_pos) and (my_length > opponent_body["length"] + 1):
        is_move_optimal["right"] += elim_bonus
      elif({"x": my_head["x"]+1, "y": my_head["y"]} in opponent_head_pos) and (my_length <= opponent_body["length"] + 1):
        is_move_optimal["right"] -= 500
    #up
      if ({"x": my_head["x"], "y": my_head["y"]+1} in opponent_head_pos) and (my_length > opponent_body["length"] + 1):
        is_move_optimal["up"] += elim_bonus
      elif({"x": my_head["x"], "y": my_head["y"]+1} in opponent_head_pos) and (my_length <= opponent_body["length"] + 1):
        is_move_optimal["up"] -= 500
        
    #down
      if ({"x": my_head["x"], "y": my_head["y"]-1} in opponent_head_pos) and (my_length > opponent_body["length"] + 1):
       is_move_optimal["down"] += elim_bonus
      elif({"x": my_head["x"], "y": my_head["y"]-1} in opponent_head_pos) and (my_length <= opponent_body["length"] + 1):
        is_move_optimal["down"] -= 500

    murder_zone = danger_zone(game_state)
    
    is_move_optimal["left"] += bfs_pos(game_state,murder_zone, 0, my_length, {"x": my_head["x"] - 1, "y": my_head["y"]})

    is_move_optimal["right"] += bfs_pos(game_state,murder_zone, 0, my_length, {"x": my_head["x"] + 1, "y": my_head["y"]})

    is_move_optimal["up"] += bfs_pos(game_state,murder_zone, 0, my_length, {"x": my_head["x"], "y": my_head["y"] + 1})

    is_move_optimal["down"] += bfs_pos(game_state,murder_zone, 0, my_length, {"x": my_head["x"], "y": my_head["y"] - 1})
    
    #print(f"{is_move_optimal} this is apparently the optimal move")
    return is_move_optimal



# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
