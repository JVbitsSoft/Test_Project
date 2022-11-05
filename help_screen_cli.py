import math
import screen_cli

class HelpScreenCLI(screen_cli.ScreenCLI):
    def __init__(self, terminal_size):
        super().__init__(terminal_size)

        self.run()
    
    def run(self):
        self.update()
        self.get_key()

    def update(self):
        text1 = '''
Use the W, A, S, D keys to navigate between buttons:
                       ———  
                      | W |
                       ———
                 ———   ———   ———
                | A | | S | | D |
                 ———   ———   ———'''
        text2 = '''
Use the Enter key to execute the desired option:
                    —————
                   |  ⏎  |
                    —    |
                     |   |
                      ———'''

        x_adjust = math.ceil(self.terminal_size[0]/2) - 26
        y_adjust = math.ceil(self.terminal_size[1]/2) - 6

        frame = f'\u001b[{y_adjust}E'

        for i in text1.split('\n'):
            frame += f'\u001b[{x_adjust}C{i}\n'
        
        x_adjust = math.ceil(self.terminal_size[0]/2) - 24
        for i in text2.split('\n'):
            frame += f'\u001b[{x_adjust}C{i}\n'
        
        frame += f'Press any key to continue...'.center(self.terminal_size[0])

        self.clear_screen()
        print(frame, end='', flush=True)