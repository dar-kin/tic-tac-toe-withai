from math import inf


def print_field():
    global field
    print("---------")
    for i in range(3):
        print("| ", end="")
        for j in range(3):
            print(field[i][j], end=" ")
        if i == 2:
            break
        print("|")
    print("|\n---------")


def make_best_move():
    global player
    best_score = -inf
    best_move = None
    real_player = player
    for move in get_possible_moves():
        move_min(move)
        score = minimax(False, real_player)
        undo()
        if score > best_score:
            best_score = score
            best_move = move
    player = real_player
    move_min(best_move)


def get_state():
    if check_win():
        return "Over"
    for i in range(3):
        for j in range(3):
            if field[i][j] == "_":
                return "unfinished"
    else:
        return "Draw"


def minimax(max_turn, real_player):
    state = get_state()
    if state == "Draw":
        return 0
    elif state == "Over":
        return 1 if player == real_player else -1
    scores = []
    for move in get_possible_moves():
        swap_player()
        move_min(move)
        scores.append(minimax(not max_turn, real_player))
        undo()
    return max(scores) if player == real_player else min(scores)


def get_possible_moves():
    moves = []
    for i in range(3):
        for j in range(3):
            if field[i][j] == "_":
                moves.append((i, j))
    return moves


def undo():
    l_m = last_move.pop()
    field[l_m[0]][l_m[1]] = "_"


def move_min(move):
    global field, last_move
    field[move[0]][move[1]] = player
    last_move.append((move[0], move[1]))


def swap_player():
    global player
    if player == "X":
        player = "O"
    else:
        player = "X"


def make_random_move():
    global field, last_move
    for i in range(3):
        for j in range(3):
            if field[i][j] == "_":
                field[i][j] = player
                last_move.append((i, j))
                return


def make_move():
    global field
    if operators[player] == "hard":
        make_best_move()
    elif operators[player] == "medium":
        print('Making move level "medium"')
        move = check_pre_win()
        if check_pre_win():
            move_min([move[0], move[1]])
        else:
            make_random_move()
    elif operators[player] == "easy":
        print('Making move level "easy"')
        make_random_move()
        return
    else:
        while True:
            coords = input("Enter the coordinates: ").split()
            if not coords[0].isnumeric() or not coords[1].isnumeric():
                print("You should enter numbers!")
            elif int(coords[0]) not in range(1, 4) or int(coords[1]) not in range(1, 4):
                print("Coordinates should be from 1 to 3!")
            elif field[3 - int(coords[1])][int(coords[0]) - 1] != "_":
                print("This cell is occupied! Choose another one!")
            else:
                move_min([3 - int(coords[1]), int(coords[0]) - 1])
                break


def check_win():
    for i in range(3):
        if field[i] == win_cond_x or field[i] == win_cond_o:
            return True
        row = ["" for k in range(3)]
        for j in range(3):
            row[j] = field[j][i]
        if row == win_cond_x or row == win_cond_o:
            return True
    else:
        row = ["" for k in range(3)]
        for i in range(3):
            row[i] = field[i][i]
        if row == win_cond_x or row == win_cond_o:
            return True
        for i in range(3):
            row[i] = field[i][2 - i]
        if row == win_cond_x or row == win_cond_o:
            return True
    return False


def mostly_finished(row):
    return (row.count("X") == 2 or row.count("O") == 2) and "_" in row


def check_pre_win():
    for i in range(3):
        if mostly_finished(field[i]):
            return i, field[i].index("_")
        row = ["" for k in range(3)]
        for j in range(3):
            row[j] = field[j][i]
        if mostly_finished(row):
            return row.index("_"), i
    else:
        row = ["" for k in range(3)]
        for i in range(3):
            row[i] = field[i][i]
        if mostly_finished(row):
            coord = row.index("_")
            return coord, coord
        for i in range(3):
            row[i] = field[i][2 - i]
        if mostly_finished(row):
            coord = row.index("_")
            return coord, 2 - coord
    return []


ais = ("easy", "user", "medium", "hard")
while True:
    op1, op2 = "", ""
    command = input().split()
    if command[0] == "exit":
        break
    elif command[0] == "start":
        if len(command) != 3 or command[1] not in ais or command[2] not in ais:
            print("Bad parameters!")
            break
        else:
            last_move = []
            op1, op2 = command[1], command[2]
            field = [["_" for i in range(3)] for j in range(3)]
            print_field()
            player = "X"
            operators = {"X": op1, "O": op2}
            win_cond_x = ["X", "X", "X"]
            win_cond_o = ["O", "O", "O"]
            for _i in range(9):
                make_move()
                print_field()
                if check_win():
                    print(f"{player} wins")
                    break
                swap_player()
            else:
                print("Draw")
