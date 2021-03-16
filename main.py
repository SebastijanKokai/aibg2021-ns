import requests

import numpy as np

global playerId
playerId = 818662

global gameState
global ukucani_game_id
ukucani_game_id = 0
global skipped_moves
skipped_moves = 0
global numOfMove
numOfMove = 0


class Move:
    def __init__(self, direction, distance):
        self.direction = direction
        self.distance = distance


def createPlayer1(gameStateJSON):
    x = gameStateJSON.get('player1').get('x')
    y = gameStateJSON.get('player1').get('y')
    score = gameStateJSON.get('player1').get('score')
    gatheredKoalas = gameStateJSON.get('player1').get('gatheredKoalas')
    energy = gameStateJSON.get('player1').get('energy')
    hasFreeASpot = gameStateJSON.get('player1').get('hasFreeASpot')
    teamName = gameStateJSON.get('player1').get('teamName')
    numberOfUsedFAS = gameStateJSON.get('player1').get('numberOfUsedFreeASpot')
    numOfSkips = gameStateJSON.get('player1').get('numOfSkipATurnUsed')
    executedAction = gameStateJSON.get('player1').get('executedAction')

    return Player(x, y, score, gatheredKoalas, energy, hasFreeASpot, numberOfUsedFAS, numOfSkips,
                  executedAction, teamName)


def createPlayer2(gameStateJSON):
    x = gameStateJSON.get('player2').get('x')
    y = gameStateJSON.get('player2').get('y')
    score = gameStateJSON.get('player2').get('score')
    gatheredKoalas = gameStateJSON.get('player2').get('gatheredKoalas')
    energy = gameStateJSON.get('player2').get('energy')
    hasFreeASpot = gameStateJSON.get('player2').get('hasFreeASpot')
    teamName = gameStateJSON.get('player2').get('teamName')
    numberOfUsedFAS = gameStateJSON.get('player2').get('numberOfUsedFreeASpot')
    numOfSkips = gameStateJSON.get('player2').get('numOfSkipATurnUsed')
    executedAction = gameStateJSON.get('player2').get('executedAction')

    return Player(x, y, score, gatheredKoalas, energy, hasFreeASpot, numberOfUsedFAS, numOfSkips,
                  executedAction, teamName)


def popuniMapu(matrica, gameStateJSON):
    tilesJSON = gameStateJSON.get('map').get('tiles')
    for j in range(27):
        for i in range(9):
            row = tilesJSON[j][i].get('row')
            column = tilesJSON[j][i].get('column')
            ownedByTeam = tilesJSON[j][i].get('ownedByTeam')
            tileContent = (tilesJSON[j][i].get('tileContent').get('itemType'),
                           tilesJSON[j][i].get('tileContent').get('numOfItems'))
            tile = Tile(row, column, ownedByTeam, tileContent)
            matrica[j][i] = tile
    return matrica


def inicirajGameState(gameStateJSON):
    player1 = createPlayer1(gameStateJSON)
    player2 = createPlayer2(gameStateJSON)

    tiles = np.full((27, 9), Tile(None, None, None, None))

    tiles = popuniMapu(tiles, gameStateJSON)

    gameId = gameStateJSON.get('gameId')

    numberOfFreeSpots = gameStateJSON.get('map').get('numberOfFreeSpots')

    player1ChangedTiles = gameStateJSON.get('player1ChangedTiles')

    player2ChangedTiles = gameStateJSON.get('player2ChangedTiles')

    numOfMove = gameStateJSON.get('numOfMove')

    winnerTeamName = gameStateJSON.get('winnerTeamName')

    finished = gameStateJSON.get('finished')

    currentPlayer = gameStateJSON.get('currentPlayer')

    return GameState(gameId, player1, player2, currentPlayer, tiles, numberOfFreeSpots, player1ChangedTiles,
                     player2ChangedTiles, numOfMove, winnerTeamName, finished)


class GameState:
    def __init__(self, gameId, player1, player2, currentPlayer, tiles, numOfFreeSpots,
                 player1ChangedTiles, player2ChangedTiles, numOfMove, winnerTeamName, finished):
        self.gameId = gameId
        self.player1 = player1
        self.player2 = player2
        self.currentPlayer = currentPlayer
        self.tiles = tiles
        self.numOfFreeSpots = numOfFreeSpots
        self.player1ChangedTiles = player1ChangedTiles
        self.player2ChangedTiles = player2ChangedTiles
        self.numOfMove = numOfMove
        self.winnerTeamName = winnerTeamName
        self.finished = finished


class Player:
    def __init__(self, x, y, score, gatheredKoalas, energy, hasFreeASpot, numberOfUsedFAS,
                 numOfSkips, executedAction, teamName):
        self.x = x
        self.y = y
        self.score = score
        self.gatheredKoalas = gatheredKoalas
        self.energy = energy
        self.hasFreeASpot = hasFreeASpot
        self.teamName = teamName
        self.numberOfUsedFAS = numberOfUsedFAS
        self.numOfSkips = numOfSkips
        self.executedAction = executedAction


class Tile:
    def __init__(self, row, column, ownedByTeam, tileContent):
        self.row = row
        self.column = column
        self.ownedByTeam = ownedByTeam
        self.tileContent = tileContent


class CommunicationApi:

    def __init__(self, is_train_mode):
        self.is_train_mode = is_train_mode

    def is_in_training_mode(self):
        return self.is_train_mode

    def get_url(self):
        return 'https://aibg2021.herokuapp.com/train/' if self.is_train_mode else 'https://aibg2021.herokuapp.com/'

    # vraca mapu
    def make_get_request(self, relative_url):
        r = requests.get(url=self.get_url() + relative_url)
        data = r.json()
        return data

    # vraca mapu nakon sto se joinuje
    # def join_game(self, playerId, gameId):
    #    return self.make_get_request('/game/play?playerId=' + str(playerId) + '&gameId=' + str(gameId))
    # https: // aibg2021.herokuapp.com / train / makeGame?playerId = 818662
    def play_against_bot(self):
        return self.make_get_request('makeGame?playerId=' + str(playerId))

    # https://aibg2021.herokuapp.com/joinGame?playerId=123456&gameId=123
    def play_against_player(self):
        global ukucani_game_id
        return self.make_get_request('joinGame?playerId=' + str(playerId) + "&gameId=" + str(ukucani_game_id))

    # https: // aibg2021.herokuapp.com / botVSbot?player1Id = 123456 & player2Id = 123457
    def play_against_yourself(self):
        return self.make_get_request('botVSbot?player1Id= ' + str(playerId) + "&player2Id=" + str(playerId + 1))

    # https://aibg2021.herokuapp.com/train/move?playerId=818662&gameId=23&direction=d&distance=4
    def move_player(self, playerId, gameId, direction, distance):
        URL = 'move?playerId=' + str(
            playerId) + '&gameId=' + str(gameId) + '&direction=' + str(direction) + '&distance=' + str(distance)
        print(URL)
        response = self.make_get_request(URL)
        return response

    # https://aibg2021.herokuapp.com/train/skipATurn?playerId=818662&gameId=23
    def skip_a_move(self, playerId, gameId):
        URL = 'skipATurn?playerId=' + str(playerId) + '&gameId=' + str(gameId)
        print(URL)
        response = self.make_get_request(URL)
        return response

    # https://aibg2021.herokuapp.com/train/stealKoalas?playerId=818662&gameId=23
    def steal_koalas(self, playerId, gameId):
        URL = 'stealKoalas?playerId=' + str(playerId) + '&gameId=' + str(gameId)
        print(URL)
        response = self.make_get_request(URL)
        return response

    # https://aibg2021.herokuapp.com/train/freeASpot?playerId=818662&gameId=23&x=2&y=3
    #    #92.168.17.189:8080[/train]/freeAPlayer?playerId=567348&gameId=30&x=2&y=3

    def free_a_spot_or_teleport(self, playerId, gameId, x, y):
        URL = "freeASpot?playerId=" + str(playerId) + '&gameId=' + str(gameId) + '&x=' + str(x) + '&y=' + str(y)
        print(URL)
        response = self.make_get_request(URL)
        return response


class Game:
    def __init__(self, communication_api, is_train_mode):
        self.communication_api = communication_api
        self.is_train_mode = is_train_mode

    def start_game(self):
        if self.is_train_mode:
            gameStateJSON = self.communication_api.play_against_bot()
            self.play(gameStateJSON)
        else:
            gameStateJSON = self.communication_api.play_against_player()
            self.play(gameStateJSON)

    def play(self, gameStateJSON):
        player1 = createPlayer1(gameStateJSON)
        player2 = createPlayer2(gameStateJSON)
        matrix = np.full((27, 9), Tile(None, None, None, None))

        matrix = popuniMapu(matrix, gameStateJSON)
        gameId = gameStateJSON.get('gameId')
        print(gameId)
        numberOfFreeSpots = 247
        for i in range(27):
            for j in range(9):
                if not (self.isValid(i, j, matrix)):
                    numberOfFreeSpots -= 1
        print(numberOfFreeSpots)
        print(numOfMove)
        # gameState = GameState(gameId, player1, player2, None, matrix, counter)

        if player1.teamName == 'SVS':
            res = self.action_logic(matrix, playerId, gameId, player1.energy, player1.x, player1.y, player2.x,
                                        player2.y, player2.energy, self.communication_api, player1.hasFreeASpot,
                                        player1.numberOfUsedFAS, numberOfFreeSpots)
            print(res)
            self.play(res)
            # response = self.action_logic(matrix, playerId, gameId, player1.energy, 0, player1.energy)
        elif player2.teamName == 'SVS':
            res = self.action_logic(matrix, playerId, gameId, player2.energy, player2.x, player2.y, player1.x,
                                    player1.y, player1.energy, self.communication_api, player2.hasFreeASpot,
                                    player2.numberOfUsedFAS, numberOfFreeSpots)
            print(res)
            self.play(res)
            # response = self.action_logic(matrix, playerId, gameId, player2.energy, 0, player2.energy)

    # napravi potez itd
    def playerBeside(self, x, y, target_x, target_y):
        action = ''

        even = False
        if x % 2 == 0:
            even = True

        if even:
            if x + 2 == target_x and y == target_y:
                return True
            if x - 2 == target_x and y == target_y:
                return True
            if x + 1 == target_x and y == target_y:
                return True
            if x - 1 == target_x and y == target_y:
                return True
            if x + 1 == target_x and y - 1 == target_y:
                return True
            if x - 1 == target_x and y - 1 == target_y:
                return True

        else:
            if x + 2 == target_x and y == target_y:
                return True
            if x - 2 == target_x and y == target_y:
                return True
            if x - 1 == target_x and y == target_y:
                return True
            if x - 1 == target_x and y + 1 == target_y:
                return True
            if x + 1 == target_x and y == target_y:
                return True
            if x + 1 == target_x and y + 1 == target_y:
                return True

        return False

    def freeASpot(self, x, y, matrix):

        even = False
        if x % 2 == 0:
            even = True
        # matrix[x][y].tileContent[0] == 'HOLE' and not matrix[x][y].ownedByTeam != ''
        if even:
            if 26 >= x + 2 >= 0 and 8 >= y >= 0 and matrix[x + 2][y].ownedByTeam != '' and not \
            matrix[x + 2][y].tileContent[0] == 'HOLE':
                return (x + 2, y)
            if 26 >= x - 2 >= 0 and 8 >= y >= 0 and matrix[x - 2][y].ownedByTeam != '' and not \
            matrix[x - 2][y].tileContent[0] == 'HOLE':
                return (x - 2, y)
            if 26 >= x + 1 >= 0 and 8 >= y >= 0 and matrix[x + 1][y].ownedByTeam != '' and not \
            matrix[x + 1][y].tileContent[0] == 'HOLE':
                return (x + 1, y)
            if 26 >= x - 1 >= 0 and 8 >= y >= 0 and matrix[x - 1][y].ownedByTeam != '' and not \
            matrix[x - 1][y].tileContent[0] == 'HOLE':
                return (x - 1, y)
            if 26 >= x + 1 >= 0 and 8 >= y - 1 >= 0 and matrix[x + 1][y - 1].ownedByTeam != '' and not \
            matrix[x + 1][y - 1].tileContent[0] == 'HOLE':
                return (x + 1, y - 1)
            if 26 >= x - 1 >= 0 and 8 >= y - 1 >= 0 and matrix[x - 1][y - 1].ownedByTeam != '' and not \
            matrix[x - 1][y - 1].tileContent[0] == 'HOLE':
                return (x - 1, y - 1)

        else:
            if 26 >= x + 2 >= 0 and 8 >= y >= 0 and matrix[x + 2][y].ownedByTeam != '' and not \
            matrix[x + 2][y].tileContent[0] == 'HOLE':
                return (x + 2, y)
            if 26 >= x - 2 >= 0 and 8 >= y >= 0 and matrix[x - 2][y].ownedByTeam != '' and not \
            matrix[x - 2][y].tileContent[0] == 'HOLE':
                return (x - 2, y)
            if 26 >= x - 1 >= 0 and 8 >= y >= 0 and matrix[x - 1][y].ownedByTeam != '' and not \
            matrix[x - 1][y].tileContent[0] == 'HOLE':
                return (x - 1, y)
            if 26 >= x - 1 >= 0 and 8 >= y + 1 >= 0 and matrix[x - 1][y + 1].ownedByTeam != '' and not \
            matrix[x - 1][y + 1].tileContent[0] == 'HOLE':
                return (x - 1, y + 1)
            if 26 >= x + 1 >= 0 and 8 >= y >= 0 and matrix[x + 1][y].ownedByTeam != '' and not \
            matrix[x + 1][y].tileContent[0] == 'HOLE':
                return (x + 1, y)
            if 26 >= x + 1 >= 0 and 8 >= y + 1 >= 0 and matrix[x + 1][y + 1].ownedByTeam != '' and not \
            matrix[x + 1][y + 1].tileContent[0] == 'HOLE':
                return (x + 1, y + 1)

        return (-99, -99)

    def countPoints(self, x, y, matrix, action, distance):

        points = 0

        for i in range(1, distance + 1):

            even = False
            if x % 2 == 0:
                even = True

            if action == 'w':
                tile = matrix[x - 2][y].tileContent[0]
                x = x - 2
            elif action == 's':
                tile = matrix[x + 2][y].tileContent[0]
                x = x + 2
            elif action == 'q':
                if even:
                    tile = matrix[x - 1][y - 1].tileContent[0]
                    x = x - 1
                    y = y - 1
                else:
                    tile = matrix[x - 1][y].tileContent[0]
                    x = x - 1
            elif action == 'e':
                if even:
                    tile = matrix[x - 1][y].tileContent[0]
                    x = x - 1
                else:
                    tile = matrix[x - 1][y + 1].tileContent[0]
                    x = x - 1
                    y = y + 1
            elif action == 'd':
                if even:
                    tile = matrix[x + 1][y].tileContent[0]
                    x = x + 1
                else:
                    tile = matrix[x + 1][y + 1].tileContent[0]
                    x = x + 1
                    y = y + 1
            elif action == 'a':
                if even:
                    tile = matrix[x + 1][y - 1].tileContent[0]
                    x = x + 1
                    y = y - 1
                else:
                    tile = matrix[x + 1][y].tileContent[0]
                    x = x + 1

            if (tile == 'KOALA'):
                points += 150
            if (tile == 'ENERGY'):
                points += 200
            if (tile == 'KOALA_CREW'):
                points += 1500
            if (tile == 'EMPTY'):
                points += 50
            if (tile == 'FREE_A_SPOT'):
                points += 1000

        # points = points - distance * 100

        return points

    def first_moves_logic(self, matrix, playerId, gameId, energy, x, y, target_x, target_y, target_energy, communication_api,
                     hasFreeASpot, numberOfUsedFAS, numberOfFreeSpots):

        if self.playerBeside(x, y, target_x, target_y) and (energy / 5) >= (target_energy / 5):
            communication_api.steal_koalas(playerId, gameId)

        for i in range(1, 16):

            if i % 2 == 0:
                communication_api.move_player(playerId, gameId, 'd', 1)
            else:
                communication_api.move_player(playerId, gameId, 'e', 1)

    def action_logic(self, matrix, playerId, gameId, energy, x, y, target_x, target_y, target_energy, communication_api,
                     hasFreeASpot, numberOfUsedFAS, numberOfFreeSpots):

        global skipped_moves
        global numOfMove
        move = None
        listOfActions = ['q', 'w', 'e', 'a', 's', 'd']
        availableActions = 0

        if self.playerBeside(x, y, target_x, target_y) and (energy / 5) >= (target_energy / 5):
            communication_api.steal_koalas(playerId, gameId)

        # go to edges
        # if numOfMove <= 16 and numOfMove % 2 == 0:
        #     numOfMove += 1
        #     return communication_api.move_player(playerId, gameId, 'd', 1)
        # if numOfMove <= 16 and not numOfMove % 2 == 0:
        #     numOfMove += 1
        #     return communication_api.move_player(playerId, gameId, 'e', 1)

        for action in listOfActions:
            if self.canGo(x, y, action, matrix, 0, energy) > 0:
                availableActions += 1

        if numberOfFreeSpots <= 90 and availableActions == 1:
            for action in listOfActions:
                if self.canGo(x, y, action, matrix, 0, energy) == 0:
                    return communication_api.move_player(playerId, gameId, action, 1)

        distance = 2
        points = 0
        for action in listOfActions:
            if self.canGo(x, y, action, matrix, 0, energy) >= distance and numberOfFreeSpots <= 160:
                pointsTemp = self.countPoints(x, y, matrix, action, distance)
                if points < pointsTemp:
                    points = pointsTemp
                    move = Move(action, distance)

        if move is not None:
            return communication_api.move_player(playerId, gameId, move.direction, move.distance)
        else:
            distance = 1
            for action in listOfActions:
                if self.canGo(x, y, action, matrix, 0, energy) >= distance:
                    pointsTemp = self.countPoints(x, y, matrix, action, distance)
                    if points < pointsTemp:
                        points = pointsTemp
                        move = Move(action, distance)
            if move is not None:
                return communication_api.move_player(playerId, gameId, move.direction, move.distance)
            else:
                if skipped_moves >= 5:
                    return communication_api.move_player(playerId, gameId, 'w', 1)
                else:
                    skipped_moves = skipped_moves + 1
                    return communication_api.skip_a_move(playerId, gameId)
                    # if hasFreeASpot and numberOfUsedFAS == 0:
                    #     x, y = self.freeASpot(x, y, matrix)
                    #     if(x != -99):
                    #         return communication_api.free_a_spot_or_teleport(playerId, gameId, x, y)
                    #     else:
                    #         skipped_moves = skipped_moves + 1
                    #         return communication_api.skip_a_move(playerId, gameId)
                    # else:
                    #     skipped_moves = skipped_moves + 1
                    #     return communication_api.skip_a_move(playerId, gameId)

    def isValid(self, x, y, matrix):
        if (26 >= x >= 0 and 8 >= y >= 0 and not matrix[x][y].tileContent[0] == 'HOLE' and not matrix[x][
                                                                                                   y].ownedByTeam != ''):
            return True
        return False

    def canGo(self, x, y, action, matrix, counter, energy):

        if counter == energy:
            return counter

        even = False
        if x % 2 == 0:
            even = True

        if action == 'w':
            if self.isValid(x - 2, y, matrix):
                return self.canGo(x - 2, y, 'w', matrix, counter + 1, energy)
        elif action == 's':
            if self.isValid(x + 2, y, matrix):
                return self.canGo(x + 2, y, 's', matrix, counter + 1, energy)
        elif action == 'q':
            if even:
                if self.isValid(x - 1, y - 1, matrix):
                    return self.canGo(x - 1, y - 1, 'q', matrix, counter + 1, energy)
            else:
                if self.isValid(x - 1, y, matrix):
                    return self.canGo(x - 1, y, 'q', matrix, counter + 1, energy)
        elif action == 'e':
            if even:
                if self.isValid(x - 1, y, matrix):
                    return self.canGo(x - 1, y, 'e', matrix, counter + 1, energy)
            else:
                if self.isValid(x - 1, y + 1, matrix):
                    return self.canGo(x - 1, y + 1, 'e', matrix, counter + 1, energy)
        elif action == 'd':
            if even:
                if self.isValid(x + 1, y, matrix):
                    return self.canGo(x + 1, y, 'd', matrix, counter + 1, energy)
            else:
                if self.isValid(x + 1, y + 1, matrix):
                    return self.canGo(x + 1, y + 1, 'd', matrix, counter + 1, energy)
        elif action == 'a':
            if even:
                if self.isValid(x + 1, y - 1, matrix):
                    return self.canGo(x + 1, y - 1, 'a', matrix, counter + 1, energy)
            else:
                if self.isValid(x + 1, y, matrix):
                    return self.canGo(x + 1, y, 'a', matrix, counter + 1, energy)

        return counter


def main():
    global ukucani_game_id
    ukucani_game_id
    is_train_mode = False
    print("Is this a competitive game? Y or N")
    is_it_a_game = input()

    if is_it_a_game == 'Y':
        print("Enter game id")
        ukucani_game_id = input()
        is_train_mode = False
    elif is_it_a_game == 'N':
        is_train_mode = True
    else:
        print("Bad input")
        main()
    communication_api = CommunicationApi(is_train_mode)
    game = Game(communication_api, is_train_mode)
    game.start_game()


main()

# UPUSTVO, ENDPOINTI ITD...
# ID NAM JE 818662
# moguci smerovi su q, w, e, a, s, d

# ODIGRAJ POTEZ
# https://aibg2021.herokuapp.com/train/move?playerId=818662&gameId=23&direction=d&distance=4

# IGRANJE PROTIV BOTA
# https://aibg2021.herokuapp.com/train/makeGame?playerId=818662

# GLEDANJE PARTIJE
# https://aibg2021.herokuapp.com/html/duel.html

# moguce samo tri poteza zaredom propustiti, otherwise gubimo partiju
# https://aibg2021.herokuapp.com/train/skipATurn?playerId=818662&gameId=23

# moguce je odmah ukrasti nazad koale od protivnika (zahteva 5 energije akcija)
# https://aibg2021.herokuapp.com/train/stealKoalas?playerId=818662&gameId=23

# ako smo odabrali polje koje je pored nas i ako imamo free a spot, u suprotnom radi teleport
# https://aibg2021.herokuapp.com/train/freeAPlayer?playerId=818662&gameId=23&x=2&y=3
