import AIArena.games as games


class Ref:
    """ This class coordinates, executes, and determines which AI or player won a given (locally run) game. It is reasonable to assume that AIOlympics uses a similar process to perform game execution for the purposes of AI development.
    """
    
    #def __init__(self, state=None):
    def createGame(self,game,players):
        """ Initializes a given game with a given set of players (human and/or AI). This takes the place of a constructor.
        
        :param game: Name of a game to set up (currently, only "Connect4" is implemented)
        :type game: string
        :param players: List of :class:`aiolympics.AI.Player` objects to have play the game.
        :type players: list
        """
        self.pids = [x.name for x in players]
        self.players = players
        self.moves = []

        if game == "Connect4":
            self.game = games.Connect4(None, self.pids)
        
        elif game=="GymBlackjack":
            self.game=games.GymBlackjack(None, self.pids)
        
        elif game=="GymFrozenLake":
            self.game=games.GymFrozenLake(None, self.pids)



    def runGame(self, display=False):
        """ Steps through player moves (in order) until the game specified by createGame() is finished.
        
        :param display: Whether or not to print every move and game state as they occur. Default value is False
        :type display: bool
        :return: The final game state. 
        :rtype: dict
        """
        while "Winner" not in self.game.state:
            #print("turn", self.game.state["turn"])
            move = self.players[self.game.state["turn"]].makeMove(self.game.state)
            self.moves.append(move)
            if not self.move(move):
                return -1
            if display:
                self.game.print()
        return self.game.state["Winner"]


    def move(self, move):
        """ Runs the move passed.
        
        :param move: The move to directly run in-game.
        :return: Whether or not the move was successful.
        :rtype: bool
        """
        if self.game.validateMove(move):
            self.game.makeMove(move)
            self.game.postMove()
            return True
        return False

    def endGame(self):
        pass
