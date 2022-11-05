import math
import sys
import time
import screen_cli
import button_cli

class MenuScreenCLI(screen_cli.ScreenCLI):
    def __init__(self, terminal_size):
        super().__init__(terminal_size)

        self.btn_start = button_cli.ButtonCLI('Start', '\u001b[48;5;235m', '\u001b[7m', True, False, 5, 20, 1)
        self.btn_help = button_cli.ButtonCLI('Help', '\u001b[48;5;235m', '\u001b[7m', False, False, 5, 20, 2)
        self.btn_quit = button_cli.ButtonCLI('Quit', '\u001b[48;5;235m', '\u001b[7m', False, False, 5, 20, 3)
        self.current_btn = self.btn_start

        self.next_screen = self.run()
        #self.clear_screen()
    
    def blink_btn(self, btn: button_cli.ButtonCLI):
        btn.lit = True
        self.update()
        time.sleep(0.1)
    
    def apply_transition(self, btn: button_cli.ButtonCLI):
        self.current_btn.selected = False
        self.current_btn = btn
        self.current_btn.selected = True
    
    def run(self):
        while True:
            self.update()
            key = self.get_key()
            try:
                key = ord(key)
            except TypeError:
                key = ord(key[0])
            
            match key:
                case 119: # w key
                    match self.current_btn.id:
                        case self.btn_help.id:
                            self.apply_transition(self.btn_start)
                        case self.btn_quit.id:
                            self.apply_transition(self.btn_help)
                case 115: # s key
                    match self.current_btn.id:
                        case self.btn_start.id:
                            self.apply_transition(self.btn_help)
                        case self.btn_help.id:
                            self.apply_transition(self.btn_quit)
                case 13:  # enter key
                    match self.current_btn.id:
                        case self.btn_start.id:
                            self.blink_btn(self.current_btn)
                            return 0 # go to PlayScreenCLI
                        case self.btn_help.id:
                            self.blink_btn(self.current_btn)
                            return 1 # go to HelpScreenCLI
                        case self.btn_quit.id:
                            self.blink_btn(self.current_btn)
                            print('\u001b[?25h', end='', flush=True)
                            self.clear_screen()
                            sys.exit() # quit

    def update(self):
        title = '''
███    ███ ███████ ███    ███  ██████  ██████  ██    ██      ██████   █████  ███    ███ ███████
████  ████ ██      ████  ████ ██    ██ ██   ██  ██  ██      ██       ██   ██ ████  ████ ██     
██ ████ ██ █████   ██ ████ ██ ██    ██ ██████    ████       ██   ███ ███████ ██ ████ ██ █████  
██  ██  ██ ██      ██  ██  ██ ██    ██ ██   ██    ██        ██    ██ ██   ██ ██  ██  ██ ██     
██      ██ ███████ ██      ██  ██████  ██   ██    ██         ██████  ██   ██ ██      ██ ███████'''.strip()

        btn_start_slices = self.btn_start.get_slices()
        btn_help_slices = self.btn_help.get_slices()
        btn_quit_slices = self.btn_quit.get_slices()

        x_adjust = math.ceil(self.terminal_size[0]/2) - 48 # math.ceil(95/2)
        y_adjust = math.ceil(self.terminal_size[1]/2) - 11 # math.ceil((3+5*3+1+2)/2)

        frame = f'\u001b[{y_adjust}E'
        for i in title.split('\n'):
            frame += f'\n\u001b[{x_adjust}C{i}'
        frame += '\n' + f'By João Victor Santos'.center(self.terminal_size[0]) + '\n'*2

        x_adjust = x_adjust = math.ceil(self.terminal_size[0]/2) - 10

        for i in btn_start_slices + btn_help_slices + btn_quit_slices:
            frame += f'\n\u001b[{x_adjust}C{i}'
        
        self.clear_screen()
        print(frame,  end='', flush=True)
