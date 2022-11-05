import math
import struct
import time
import screen_cli
import button_cli

class GameOverScreenCLI(screen_cli.ScreenCLI):
    def __init__(self, terminal_size, score, best_score):
        super().__init__(terminal_size)
        self.score = score
        self.best_score = best_score

        self.btn_play_again = button_cli.ButtonCLI('Play Again', '\u001b[48;5;235m', '\u001b[7m', True, False, 5, 20, 1)
        self.btn_back_to_menu = button_cli.ButtonCLI('Back to Menu', '\u001b[48;5;235m', '\u001b[7m', False, False, 5, 20, 2)
        self.current_btn = self.btn_play_again

        self.next_screen = self.run()
    
    def blink_btn(self, btn: button_cli.ButtonCLI):
        btn.lit = True
        self.update()
        time.sleep(0.1)
    
    def save_new_score(self):
        with open('database.db', 'wb') as database:
            database.write(struct.pack('I', self.score))
    
    def apply_transition(self, btn: button_cli.ButtonCLI):
        self.current_btn.selected = False
        self.current_btn = btn
        self.current_btn.selected = True

    def run(self):
        if self.score > self.best_score:
             self.new_record()
             self.save_new_score()
        else:
            self.game_over()
        
        while True:
            self.update()
            key = self.get_key()
            try:
                key = ord(key)
            except TypeError:
                key = ord(key[0])
            
            match key:
                case 97:  # a key
                    if self.current_btn.id == self.btn_back_to_menu.id:
                        self.apply_transition(self.btn_play_again)
                case 100: # d key
                    if self.current_btn.id == self.btn_play_again.id:
                        self.apply_transition(self.btn_back_to_menu)
                case 13:  # enter key
                    if self.current_btn.id == self.btn_play_again.id:
                        self.blink_btn(self.current_btn)
                        return 0 # go to PlayScreenCLI
                    else:
                        self.blink_btn(self.current_btn)
                        return 1 # go to MenuScreenCLI
    
    def update(self):
        btn_play_again_slices = self.btn_play_again.get_slices()
        btn_back_to_menu_slices = self.btn_back_to_menu.get_slices()

        x_adjust = math.ceil(self.terminal_size[0]/2) - 20 # math.ceil(40/2)

        frame = self.incomplete_frame
        for i in range(5):
            frame += '\n' + f'\u001b[{x_adjust}C{btn_play_again_slices[i]}{btn_back_to_menu_slices[i]}'
        
        self.clear_screen()
        print(frame, end='', flush=True)

    def game_over(self):
        game_over_str = '''
 ██████   █████  ███    ███ ███████      ██████  ██    ██ ███████ ██████ 
██       ██   ██ ████  ████ ██          ██    ██ ██    ██ ██      ██   ██
██   ███ ███████ ██ ████ ██ █████       ██    ██ ██    ██ █████   ██████ 
██    ██ ██   ██ ██  ██  ██ ██          ██    ██  ██  ██  ██      ██   ██
 ██████  ██   ██ ██      ██ ███████      ██████    ████   ███████ ██   ██'''.strip('\n')

        x_adjust = math.ceil(self.terminal_size[0]/2) - 36 # math.ceil(36/2)
        y_adjust = math.ceil(self.terminal_size[1]/2) - 3 # math.ceil(5/2)

        self.clear_screen()
        frame = f'\u001b[{y_adjust}E'
        for i in game_over_str.split('\n'):
            frame += f'\u001b[{x_adjust}C{i}\n'
        frame += '\n' + f'Score: {self.score}  Best Score: {self.best_score}'.center(self.terminal_size[0])
        #print('\u001b[H', end='', flush=True)
        #print(frame, end='', flush=True)

        self.incomplete_frame = frame

    def new_record(self):
        game_over_str = '''

███    ██ ███████ ██     ██     ██████  ███████  ██████  ██████  ██████  ██████ 
████   ██ ██      ██     ██     ██   ██ ██      ██      ██    ██ ██   ██ ██   ██
██ ██  ██ █████   ██  █  ██     ██████  █████   ██      ██    ██ ██████  ██   ██
██  ██ ██ ██      ██ ███ ██     ██   ██ ██      ██      ██    ██ ██   ██ ██   ██
██   ████ ███████  ███ ███      ██   ██ ███████  ██████  ██████  ██   ██ ██████ '''.strip('\n')

        x_adjust = math.ceil(self.terminal_size[0]/2) - math.ceil(79/2)
        y_adjust = math.ceil(self.terminal_size[1]/2) - 3 # math.ceil(5/2)

        self.clear_screen()
        frame = f'\u001b[{y_adjust}E'
        for i in game_over_str.split('\n'):
            frame += f'\u001b[{x_adjust}C{i}\n'
        frame += '\n' + f'New Best Score: {self.score}  Old Best Score: {self.best_score}'.center(self.terminal_size[0])
        #print('\u001b[H', end='', flush=True)
        #print(frame, end='', flush=True)

        self.incomplete_frame = frame