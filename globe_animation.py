import time
import os
from asciimatics.screen import Screen

def globe_animation(screen):
    for i in range(screen.width):
        screen.print_at('🌍', (screen.width//2) + (i%2)*2 - 1, screen.height//2, colour=2)
        ev = screen.get_key()
        if ev in (ord('Q'), ord('q')):
            return
        screen.refresh()
        time.sleep(0.1)

Screen.wrapper(globe_animation)
time.sleep(3)
os.system('clear')


