#!/usr/bin/env python

import curses
import time

def main():
    curses.wrapper(start)

def start(stdscr):
    pad = curses.newpad(100,100)

    for y in range(0,100):
        for x in range(0,100):
            try: pad.addch(y,x,ord('a')+(x*x+y*y) % 26)
            except curses.error: pass

    for i in range(100):
        pad.noutrefresh(i,i, 0,0, 20, 75)
        curses.doupdate()
        time.sleep(0.25)

if __name__ == '__main__':
    main()
