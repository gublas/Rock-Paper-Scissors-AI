from time import sleep
from players import Player, PlayerAI

class Game:
    def __init__(self):
        self.p1 = PlayerAI()
        self.p2 = PlayerAI()
        self.p1.load_model()
        self.p2.load_model()
        self.scoreboard = [self.p1.points, self.p2.points]
        self.winner = None
        self.rounds = 0
        self.p1.opponent = self.p2
        self.p2.opponent = self.p1

    def countdown(self) -> None:
        for sec in range(0, 3):
            print(3 - sec)
            sleep(1)

    def get_round_winner(self):
        self.results = {
            'piedra':{
                'piedra': None,
                'papel': self.p2,
                'tijera': self.p1
            },
            'papel': {
                'piedra': self.p1,
                'papel': None,
                'tijera': self.p2
            },
            'tijera': {
                'piedra': self.p2,
                'papel': self.p1,
                'tijera': None
            }
        }
        self.winner = (self.results[f'{self.p1.choice}'][f'{self.p2.choice}'])
        return self.winner

    def decider(self):
        self.round = f'⇒ {self.p1.shown_choice} ({self.p1.choice}) vs {self.p2.shown_choice} ({self.p2.choice})'
        print(self.round)
        if self.get_round_winner() == None:
            self.rounds += 1
            print('⇒ ¡Ha habido un empate!')
            print(f'⇒ {'Humano' if self.p1.ptype == 'p' else 'IA'} |{self.p1.points} - {self.p2.points}| {'IA' if self.p2.ptype == 'ai' else 'Humano'}')
            pass
        if self.get_round_winner() == self.p1:
            self.p1.points += 1
            self.rounds += 1
            print(f'⇒ ¡{'El humano' if self.p1.ptype == 'p' else 'La IA'}{' 1' if self.p1.ptype == self.p2.ptype else ''} gana la ronda!')
            print(f'⇒ {'Humano' if self.p1.ptype == 'p' else 'IA'}{' 1' if self.p1.ptype == self.p2.ptype else ''} |{self.p1.points} - {self.p2.points}| {'IA' if self.p2.ptype == 'ai' else 'Humano'}{' 2' if self.p1.ptype == self.p2.ptype else ''}')
            pass
        if self.get_round_winner() == self.p2:
            self.p2.points += 1
            self.rounds += 1
            print(f'⇒ ¡{'La IA' if self.p2.ptype == 'ai' else 'El humano'}{' 2' if self.p1.ptype == self.p2.ptype else ''} gana la ronda!')
            print(f'⇒ {'Humano' if self.p1.ptype == 'p' else 'IA'}{' 1' if self.p1.ptype == self.p2.ptype else ''} |{self.p1.points} - {self.p2.points}| {'IA' if self.p2.ptype == 'ai' else 'Humano'}{' 2' if self.p1.ptype == self.p2.ptype else ''}')
            pass

    def train_decider(self):
        if self.get_round_winner() == None:
            self.rounds += 1
            pass
        if self.get_round_winner() == self.p1:
            self.p1.points += 1
            self.rounds += 1
            pass
        if self.get_round_winner() == self.p2:
            self.p2.points += 1
            self.rounds += 1
            pass

    def play(self):
        self.p1 = Player()
        self.p1.points = 0  # Reset points (saved from training)
        self.p2.points = 0

        try:
            self.win_points = 3
            self.win_points = int(input('Introduce la cantidad necesaria de puntos para ganar (default = 3): '))
            if self.win_points <= 0:
                print('Número inválido. Ganará el que consiga 3 puntos')
                self.win_points = 3
        except ValueError:
            print('¡Eso no es un número! Ganará el que consiga 3 puntos')
            self.win_points = 3

        while self.p1.points < self.win_points and self.p2.points < self.win_points:
            self.p1.ask_choice()
            self.p2.take_action()
            self.p1.update_history()
            self.p2.update_history()
            self.countdown()
            self.decider()
            if self.get_round_winner() == self.p1:
                self.p2.update_qtable(-1)
            elif self.get_round_winner() == self.p2:
                self.p2.update_qtable(1)
            else:
                self.p2.update_qtable(0.05)
        if self.get_round_winner() == self.p1:
            print(f'⇒ ¡{'El humano' if self.p1.ptype == 'p' else 'La IA'}{' 1' if self.p1.ptype == self.p2.ptype else ''} gana la partida!')
        if self.get_round_winner() == self.p2:
            print(f'⇒ ¡{'La IA' if self.p2.ptype == 'ai' else 'El humano'}{' 2' if self.p1.ptype == self.p2.ptype else ''} gana la ronda!')
        
        self.save_model()

    def training(self, lr, gamma):

        while self.p1.points < 10 and self.p2.points < 10:
            self.p1.train_move()
            self.p2.train_move()
            self.p1.update_history()
            self.p2.update_history()
            self.train_decider()
            if self.get_round_winner() == self.p1:
                self.p1.update_qtable(1, lr, gamma)
                self.p2.update_qtable(-1, lr, gamma)
            elif self.get_round_winner() == self.p2:
                self.p1.update_qtable(-1, lr, gamma)
                self.p2.update_qtable(1, lr, gamma)
            else:
                self.p1.update_qtable(0.05, lr, gamma)
                self.p2.update_qtable(0.05, lr, gamma)
        

    def train(self, games, lr, gamma):
        self.games = games
        self.current_games = 0
        self.p1.opponent = self.p2
        self.p2.opponent = self.p1
        
        while self.current_games < games:
            self.training(lr, gamma)
            self.current_games += 1
            if self.current_games % 1000 == 0:
                print(f'Epoch {int(self.current_games / 1000)} ({self.current_games} games)')
    
    def save_model(self):
        save = input('Would you like to save this AI model? (y/n) ').lower()
        if save == 'y':
            filename = input('How would you like to name the file? ')
            self.p2.save_qtable(filename)
            print(f'Model saved as {filename}')