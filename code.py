# CircuitPython/Raspberry Pi Pico'firmware' for The Smallest Keyboard
# Build video: https://www.youtube.com/watch?v=iWWTJKWFNok
# All files, notes, etc. are available at the project page: https://hackaday.io/project/178204-the-smallest-keyboard
# This code requires the CircuitPython installed on your Raspberry Pi Pico: https://circuitpython.org/board/raspberry_pi_pico/ (just copy the U2F file to the Pico)
# This code also requires the Adafruit HID keyboard and keycode files in your library: https://github.com/adafruit/Adafruit_CircuitPython_HID/releases/
# (download the Adafruit library that matches your CircuitPython version and copy the /lib/adafruit_hid/ files into your Pico's /lib folder)

#key matrix logical layout (rows/columns) <--> pin layout <--> Pico pin names in CircuitPython <--> physical layout/silkscreen
# var          c0  c1  c2  c3  c4  c5  c6  c7     c8  c9    c10  c11  c12   c13   c14
#    pin       1   2   4   5   6   7   9   10     11  12    14   15   16    17    19
#        name  GP0 GP1 GP2 GP3 GP4 GP5 GP6 GP7    GP8 GP9   GP10 GP11 GP12  GP13  GP14
# r0 20  GP15  ESC `~  1   2   3   4   5   6      7   8     9    0    -_    =+    BACKSPACE
# r1 21  GP16  TAB Q   W   E   R   T   Y   U      I   null  O    P    [{    ]}    \|
# r2 22  GP17  A   S   D   F   G   H   J   null   K   L     ;:   UP   '"    DOWN  ENTER
# r3 27  GP21  Z   X   C   V   B   N   M   SPACE  ,<  .>    /?   LEFT null  null  RIGHT

#same for modifier keys
# var                alt  ctrl shift
#           pin      34   32   31
#               name GP28 GP27 GP26
# modifiers 29  GP22 ALT  CTRL SHIFT

#currently there is no ctrl+alt+del due to no delete key; if you want this, I suggest implementing delete via shift+backspace as a special case such that ctrl+alt+shift+backspace sends the ctrl+alt+del combination

import time
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

#optional delay before creating the HID for maximum compatibility
time.sleep(1)

#create the HID
kbd = Keyboard(usb_hid.devices)

#set up the row, column, and modifier arrays
rows = []
row_pins = [board.GP15, board.GP16, board.GP17, board.GP21]
for row in row_pins:
    row_key = digitalio.DigitalInOut(row)
    row_key.direction = digitalio.Direction.OUTPUT
    rows.append(row_key)

columns = []
column_pins = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9, board.GP10, board.GP11, board.GP12, board.GP13, board.GP14]
for column in column_pins:
    column_key = digitalio.DigitalInOut(column)
    column_key.direction = digitalio.Direction.INPUT
    column_key.pull = digitalio.Pull.DOWN
    columns.append(column_key)

#this is 'overkill' for code consistency and hardware flexibility; you could alternatively connect modifiers directly to a constant high or low and read the switches without an enable/disable pin
modifier_enable = []
modifier_enable_pin = [board.GP22]
for mod in modifier_enable_pin:
    mod_enable = digitalio.DigitalInOut(mod)
    mod_enable.direction = digitalio.Direction.OUTPUT
    modifier_enable.append(mod_enable)

modifiers = []
modifier_pins = [board.GP28, board.GP27, board.GP26]
for mod_pin in modifier_pins:
    mod_key = digitalio.DigitalInOut(mod_pin)
    mod_key.direction = digitalio.Direction.INPUT
    mod_key.pull = digitalio.Pull.DOWN
    modifiers.append(mod_key)

#array of modifier keycodes
mod_keymap = [Keycode.LEFT_ALT,Keycode.LEFT_CONTROL,Keycode.LEFT_SHIFT]

#array of keycodes; if you want to remap see: https://circuitpython.readthedocs.io/projects/hid/en/latest/api.html#adafruit-hid-keycode-keycode /'None' values have no physical connection
keymap = [Keycode.ESCAPE,Keycode.GRAVE_ACCENT,Keycode.ONE,Keycode.TWO,Keycode.THREE,Keycode.FOUR,Keycode.FIVE,Keycode.SIX,Keycode.SEVEN,Keycode.EIGHT,Keycode.NINE,Keycode.ZERO,Keycode.MINUS,Keycode.EQUALS,Keycode.BACKSPACE,
    Keycode.TAB,Keycode.Q,Keycode.W,Keycode.E,Keycode.R,Keycode.T,Keycode.Y,Keycode.U,Keycode.I,None,Keycode.O,Keycode.P,Keycode.LEFT_BRACKET,Keycode.RIGHT_BRACKET,Keycode.BACKSLASH,
    Keycode.A,Keycode.S,Keycode.D,Keycode.F,Keycode.G,Keycode.H,Keycode.J,None,Keycode.K,Keycode.L,Keycode.SEMICOLON,Keycode.UP_ARROW,Keycode.QUOTE,Keycode.DOWN_ARROW,Keycode.ENTER,
    Keycode.Z,Keycode.X,Keycode.C,Keycode.V,Keycode.B,Keycode.N,Keycode.M,Keycode.SPACEBAR,Keycode.COMMA,Keycode.PERIOD,Keycode.FORWARD_SLASH,Keycode.LEFT_ARROW,None,None,Keycode.RIGHT_ARROW]

#main loop
while True:
    for m_e in modifier_enable:
        m_e.value=1 #set the modifier pin to high
    for r in rows: #for each row
        r.value=1 #set row r to high
        for c in columns: #and then for each column
            if c.value: #if a keypress is detected (high row output --> switch closing circuit --> high column input)
                while c.value: #wait until the key is released, which avoids sending duplicate keypresses
                    time.sleep(0.01) #sleep briefly before checking back
                key = rows.index(r) * 15 + columns.index(c) #identify the key pressed via the index of the current row (r) and column (c)
                for m in modifiers: #check each modifier to see if it is pressed
                    if m.value: #if pressed
                        m_key = modifiers.index(m) #identify which modifier
                        kbd.press((mod_keymap[m_key])) #and press (and hold) it
                kbd.press((keymap[key])) #press the (non-modifier) key
                kbd.release_all() #then release all keys pressed
        r.value=0 #return the row to a low state, in preparation for the next row in the loop