# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
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
        "color": "#32a852",  # TODO: Choose color
        "head": "eel",  # TODO: Choose head
        "tail": "do-sammy",  # TODO: Choose tail
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
    print("=== Restarting; new move ===")
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}
    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"
    print("my_head:", my_head)
    print("my_neck:", my_neck)
    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False
    print("Safe Moves after Step 0: ", is_move_safe)
    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    # print(f"Board Width: {board_width} and Board Height: {board_height}")
    is_head_at_edge = False
    if my_head["y"] == board_height - 1:
        print(f"my_head[\"y\"]: {my_head["y"]}")
        is_move_safe["up"] = False
        is_head_at_edge = True
        print("Head at top!")
    elif my_head["y"] == 0:
        print(f"my_head[\"y\"]: {my_head["y"]}")
        is_move_safe["down"] = False
        is_head_at_edge = True
        print("Head at bottom!")
    if my_head["x"] == 0:
        print(f"my_head[\"x\"]: {my_head["x"]}")
        is_move_safe["left"] = False
        is_head_at_edge = True
        print("Head at left!")
    elif my_head["x"] == board_width - 1:
        print(f"my_head[\"x\"]: {my_head["x"]}")
        is_move_safe["right"] = False
        is_head_at_edge = True
        print("Head at right!")

    print("Safe Moves after Step 1: ", is_move_safe)
    # if 0 < my_head["x"] < board_width - 1:
    #     is_head_at_edge = False
    # if 0 < my_head["y"] < board_width - 1:
    #     is_head_at_edge = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    # if not is_head_at_edge:
    #     # prev_move = "down"
    # Go through each segment and determine if segment is adjacent to head
    for segment in my_body:
        print("Segment: ", segment)
        if (segment["x"] == my_head["x"] + 1) and (segment["y"] == my_head["y"]):
            is_move_safe["right"] = False
        elif (segment["x"] == my_head["x"] - 1) and (segment["y"] == my_head["y"]):
            is_move_safe["left"] = False
        elif (segment["y"] == my_head["y"] + 1) and (segment["x"] == my_head["x"]):
            is_move_safe["up"] = False
        elif (segment["y"] == my_head["y"] - 1) and (segment["x"] == my_head["x"]):
            is_move_safe["down"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    for snake in opponents:
        for segment in snake["body"]:
            print("Segment: ", segment)
            if (segment["x"] == my_head["x"] + 1) and (segment["y"] == my_head["y"]):
                is_move_safe["right"] = False
            elif (segment["x"] == my_head["x"] - 1) and (segment["y"] == my_head["y"]):
                is_move_safe["left"] = False
            elif (segment["y"] == my_head["y"] + 1) and (segment["x"] == my_head["x"]):
                is_move_safe["up"] = False
            elif (segment["y"] == my_head["y"] - 1) and (segment["x"] == my_head["x"]):
                is_move_safe["down"] = False

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
    previous_move = next_move  # for next run

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']
    print(f"All possible moves: {safe_moves}")
    print(f"MOVE {game_state['turn']}: {next_move}")
    print() # new line
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
