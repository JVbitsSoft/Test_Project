import msvcrt

class ScreenCLI(object):
    def __init__(self, terminal_size):
        self.terminal_size = terminal_size
    
    def clear_screen(self):
        print('\u001b[H' + ((' '*(self.terminal_size[0] - 1) + '\n')*self.terminal_size[1]).strip('\n') + ' ' + '\u001b[H', end='', flush=True)
    
    def get_key(self):
        key = msvcrt.getch()
        if msvcrt.kbhit():
            key2 = msvcrt.getch()
            return key, key2
        return key