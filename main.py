import os
import struct
import menu_screen_cli
import help_screen_cli
import play_screen_cli
import game_over_screen_cli

terminal_size = os.get_terminal_size()
mscli: menu_screen_cli.MenuScreenCLI
pscli: play_screen_cli.PlayScreenCLI
gmscli: game_over_screen_cli.GameOverScreenCLI

def main():
    global terminal_size
    os.system('cls')
    print('\u001b[?25l', end='', flush=True)

    # runs screen
    run_mscli()

def run_mscli():
    global terminal_size, mscli
    mscli = menu_screen_cli.MenuScreenCLI(terminal_size)
    if mscli.next_screen == 0:
        run_pscli()
    else:
        help_screen_cli.HelpScreenCLI(terminal_size)
        run_mscli()

def run_pscli():
    global terminal_size, pscli
    pscli = play_screen_cli.PlayScreenCLI(terminal_size)
    if pscli.next_screen == 0:
        run_gmcli(pscli.score)
    else:
        run_mscli()

def run_gmcli(score):
    global terminal_size, gmscli
    gmscli = game_over_screen_cli.GameOverScreenCLI(terminal_size, score, get_best_score())
    if gmscli.next_screen == 0:
        run_pscli()
    else:
        run_mscli()

def get_best_score():
    if not os.path.exists('database.db'):
        with open('database.db', 'wb') as database:
            database.write(struct.pack('I', 0))
        return 0
    with open('database.db', 'rb') as database:
        best_score = struct.unpack('I', database.readline())
    return best_score[0]

if __name__ == '__main__':
    main()