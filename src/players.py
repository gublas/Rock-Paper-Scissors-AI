import random
import json

class Player:
    def __init__(self, ptype = 'p'):
        self.ptype = ptype
        self.history = []   # Saves last 5 moves
        self.points = 0

    def ask_choice(self) -> None:
        try:
            self.choice = str(input("Introduce tu elección [piedra / papel / tijera]:\n⇒ ").lower())
        except:
            print("Introduce una opción válida")
        if self.choice == "piedra":
            self.shown_choice = '🗿'
        elif self.choice == "papel":
            self.shown_choice = '🧻'
        elif self.choice == "tijera":
            self.shown_choice = '✂'
        else:
            print("¡Esa no es una opción!")
            self.ask_choice()

    def update_history(self):
        self.old_history = self.history.copy()
        self.history.append(self.choice)
        self.history = self.history[-5:]

class PlayerAI(Player):
    def __init__(self, ptype = 'ai'):
        super().__init__(ptype)
        self.ptype = ptype
        self.posible_actions = ('piedra', 'papel', 'tijera')
        self.q_table = {}

    def take_action(self):
        self.state = tuple(self.opponent.history)
        if self.state not in self.q_table:
            self.q_table[self.state] = {action: 0 for action in self.posible_actions}
            self.choice = self.posible_actions[random.randint(0, 2)]
            return
        
        self.choice = max(self.q_table[self.state], key=self.q_table[self.state].get)

        if self.choice == "piedra":
            self.shown_choice = '🗿'
        elif self.choice == "papel":
            self.shown_choice = '🧻'
        elif self.choice == "tijera":
            self.shown_choice = '✂'

    def train_move(self):
        self.state = tuple(self.opponent.history)
        if self.state not in self.q_table:
            self.q_table[self.state] = {action: 0 for action in self.posible_actions}
            self.choice = self.posible_actions[random.randint(0, 2)]
            return

        if random.random() < 0.3:   # Just makes random moves while training
            self.choice = self.posible_actions[random.randint(0, 2)]
        else:
            self.choice = max(self.q_table[self.state], key=self.q_table[self.state].get)
    
    def update_qtable(self, reward, lr=0.1, gamma=0.8):
        self.state = tuple(self.opponent.old_history)
        self.next_state = tuple(self.opponent.history)
        self.lr = lr
        self.gamma = gamma
        self.reward = reward

        if self.next_state not in self.q_table:
            self.q_table[self.next_state] = {action: 0 for action in self.posible_actions}
        
        self.q_table[self.state][self.choice] += lr * (reward + self.gamma * max(self.q_table[self.next_state].values()) - self.q_table[self.state][self.choice])
    
    def save_qtable(self, filename):
        with open(f'{filename}.json', 'w') as f:
            json.dump(self.q_table, f)

    def load_model(self): # TODO: change filename default name
        _ = input("Would you like to load a saved model? (y/n)\n")
        if _ == 'y':
            filename = input("Enter the model's filename: ")
        try:
            with open(f'models/{filename}', 'r') as file:
                self.q_table = json.load(file)
        except FileNotFoundError:
            print(f"No '{filename}' file found, starting with default model.")
            self.q_table = {}


    def show_qtable(self):
        # TODO: Add JSON format
        print(self.q_table)
