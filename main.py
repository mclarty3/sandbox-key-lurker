import threading
import sys

from bot_behaviour import start_bot
from help import help_msg

with open('steam_creds.txt') as f:
    steam_creds = [line.strip().split(' ') for line in f]


def main(headless: bool, silent: bool, super_silent: bool, run_once: bool) -> None:
    threads = []
    for i, cred in enumerate(steam_creds):
        event = threading.Event()
        t = threading.Thread(target=start_bot, args=(event, i, cred, headless, silent, super_silent, run_once))
        t.start()
        threads.append(t)


if __name__ == '__main__':
    headless, silent, super_silent, run_once = False, False, False, False
    if len((args := sys.argv)) > 1:
        if any(arg in args for arg in ['-h', '--help']):
            print(help_msg)
            quit()
        if any(arg in args for arg in ['--headless', '-H']):
            headless = True
        if any(arg in args for arg in ['--silent', '-s']):
            silent = True
        if any(arg in args for arg in ['-S', '--super-silent']):
            silent = True
            super_silent = True
        if any(arg in args for arg in ['--run-once', '-r']):
            run_once = True

        if not (headless or silent or run_once):
            raise ValueError(f"Unrecognized argument(s): {','.join(args[1:])}\n{help_msg}")

    main(headless, silent, super_silent, run_once)
