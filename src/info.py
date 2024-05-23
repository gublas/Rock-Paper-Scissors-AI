from main import Game
import json

class GameInfo:
    def __init__(self, game: Game):
        self.p1 = game.p1
        self.p2 = game.p2
        self.game = game

    def get_info(self) -> json:
        info_json = json.dumps({
            'game': {
                'rounds': f'',
                'last winner': f'player {self.game.getroundwinner()}',
                'scoreboard': f'{self.p1.points} - {self.p2.points}'
            },
            f'{'human' if self.p1.ptype == 'p' else 'ia'}': {
                'type': f'{'human' if self.p1.ptype == 'p' else 'ai'}',
                'points': self.p1.points,
                'history': self.p1.history
            },
            f'{'ai' if self.p2.ptype == 'ai' else 'human'}': {
                'type': f'{'ai' if self.p2.ptype == 'ai' else 'human'}',
                'points': self.p2.points,
                'history': self.p2.history
            }
        }, indent=4)
        return info_json