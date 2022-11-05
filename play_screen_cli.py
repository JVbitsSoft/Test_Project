import time
import random
import math
import screen_cli
import button_cli

class PlayScreenCLI(screen_cli.ScreenCLI):
    def __init__(self, terminal_size):
        super().__init__(terminal_size)
        self.h = 18
        self.w = 35

        self.btn1 = button_cli.ButtonCLI('', '\u001b[41m', '\u001b[101m', True, False, self.h, self.w, 1)  # red button
        self.btn2 = button_cli.ButtonCLI('', '\u001b[42m', '\u001b[102m', False, False, self.h, self.w, 2) # green button
        self.btn3 = button_cli.ButtonCLI('', '\u001b[43m', '\u001b[103m', False, False, self.h, self.w, 3) # yellow button
        self.btn4 = button_cli.ButtonCLI('', '\u001b[44m', '\u001b[104m', False, False, self.h, self.w, 4) # blue button
        self.current_btn = self.btn1
        self.score = 0

        self.next_screen = self.run()
    
    def timer(self):
        numbers_ascii_art = []
        numbers_ascii_art.append('''
██████ 
     ██
 █████ 
     ██
██████ '''.strip('\n')) # add number one
        numbers_ascii_art.append('''
██████ 
     ██
 █████ 
██     
███████'''.strip('\n')) # add number one
        numbers_ascii_art.append('''
   ██  
  ███  
   ██  
   ██  
   ██  '''.strip('\n')) # add number one        

        x_adjust = math.ceil(self.terminal_size[0]/2) - 4 # math.ceil(7/2)
        y_adjust = math.ceil(self.terminal_size[1]/2) - 3 # math.ceil(5/2)

        self.clear_screen()

        for i in numbers_ascii_art:
            print('\u001b[H', end='', flush=True)
            frame = f'\u001b[{y_adjust}E'
            for j in i.split('\n'):
                frame += f'\u001b[{x_adjust}C{j}\n'
            print(frame, end='', flush=True)
            time.sleep(1)

    def update(self):
        btn1_slices = self.btn1.get_slices()
        btn2_slices = self.btn2.get_slices()
        btn3_slices = self.btn3.get_slices()
        btn4_slices = self.btn4.get_slices()

        x_adjust = math.ceil(self.terminal_size[0]/2) - self.w
        y_adjust = math.ceil(self.terminal_size[1]/2) - math.ceil((self.h*2 + 1)/2) 

        frame = f'\u001b[{y_adjust}E'
        for i in range(self.h):
            frame += f'\u001b[{x_adjust}C{btn1_slices[i]}{btn2_slices[i]}\n'
        for i in range(self.h):
            frame += f'\u001b[{x_adjust}C{btn3_slices[i]}{btn4_slices[i]}\n'
        frame += f'\u001b[{x_adjust}C' + f'Score: {self.score}'.center(2*self.w)

        print('\u001b[H', end='', flush=True)
        print(frame, end='', flush=True)
    
    def apply_transition(self, btn: button_cli.ButtonCLI):
        self.current_btn.selected = False
        self.current_btn = btn
        self.current_btn.selected = True
        
    def blink_btn(self, btn: button_cli.ButtonCLI):
        btn.lit = True
        self.update()
        time.sleep(0.5)

        btn.lit = False
        self.update()
        time.sleep(0.5)

    def run(self):
        #self.clear_screen()

        self.timer()

        sequence = []
        while True: # main loop
            self.current_btn.selected = False
            sequence.append(random.randint(1, 4))
            for i in sequence: # runs the randomly generated sequence
                match i:
                    case 1:
                        self.blink_btn(self.btn1)
                    case 2:
                        self.blink_btn(self.btn2)
                    case 3:
                        self.blink_btn(self.btn3)
                    case 4:
                        self.blink_btn(self.btn4)
            self.current_btn.selected = True

            for j in sequence: # waits for the player to run the randomly generated sequence
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
                                case self.btn3.id:
                                    self.apply_transition(self.btn1)
                                case self.btn4.id:
                                    self.apply_transition(self.btn2)
                        case 97:  # a key
                            match self.current_btn.id:
                                case self.btn2.id:
                                    self.apply_transition(self.btn1)
                                case self.btn4.id:
                                    self.apply_transition(self.btn3)
                        case 115: # s key
                            match self.current_btn.id:
                                case self.btn1.id:
                                    self.apply_transition(self.btn3)
                                case self.btn2.id:
                                    self.apply_transition(self.btn4)
                        case 100: # d key
                            match self.current_btn.id:
                                case self.btn1.id:
                                    self.apply_transition(self.btn2)
                                case self.btn3.id:
                                    self.apply_transition(self.btn4)
                        case 13:  # enter key
                            if self.current_btn.id == j:
                                self.current_btn.lit = True
                                self.update()
                                time.sleep(0.3)
                                
                                self.current_btn.lit = False
                                self.update()
                                time.sleep(0.1)
                                break
                            else:
                                return 0 # go to GameOverScreenCLI
                        case 27:   # esc key
                            return 1 # go to MenuScreenCLI
            self.score += 1
            time.sleep(1)