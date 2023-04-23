# pi-pico-keyboard

Updated April 2023: v2 'alpha' is reduced to around the size of a quarter (note: code in this repository is still for v1)


---


A 59-key USB HID open hardware PC keyboard using a Raspberry Pi Pico microcontroller and CircuitPython for the key matrix decoder.  This might be the smallest PC keyboard -- it fits within the outline of the Pico for direct soldering.

Build video: [YouTube](https://www.youtube.com/watch?v=iWWTJKWFNok)

Code explanation video: [YouTube](https://www.youtube.com/watch?v=V2ivH2PEoiA)

This code requires the CircuitPython interpreter installed on your Raspberry Pi Pico: https://circuitpython.org/board/raspberry_pi_pico/ (just copy the UF2 file to the Pico)

This code also requires the Adafruit HID keyboard and keycode files in your library: https://github.com/adafruit/Adafruit_CircuitPython_HID/releases/
(download the Adafruit library that matches your CircuitPython version and copy the /lib/adafruit_hid/ files into your Pico's /lib folder)
```
key matrix logical layout (rows/columns) <--> pin layout <--> Pico pin names in CircuitPython <--> physical layout/silkscreen
 var          c0  c1  c2  c3  c4  c5  c6  c7     c8  c9    c10  c11  c12   c13   c14
    pin       1   2   4   5   6   7   9   10     11  12    14   15   16    17    19
        name  GP0 GP1 GP2 GP3 GP4 GP5 GP6 GP7    GP8 GP9   GP10 GP11 GP12  GP13  GP14
 r0 20  GP15  ESC `~  1   2   3   4   5   6      7   8     9    0    -_    =+    BACKSPACE
 r1 21  GP16  TAB Q   W   E   R   T   Y   U      I   null  O    P    [{    ]}    \|
 r2 22  GP17  A   S   D   F   G   H   J   null   K   L     ;:   UP   '"    DOWN  ENTER
 r3 27  GP21  Z   X   C   V   B   N   M   SPACE  ,<  .>    /?   LEFT null  null  RIGHT

same for modifier keys
 var                alt  ctrl shift
           pin      34   32   31
               name GP28 GP27 GP26
 modifiers 29  GP22 ALT  CTRL SHIFT
```
There is no ctrl+alt+del due to no delete key; if you want this, I suggest implementing delete via shift+backspace as a special case such that ctrl+alt+shift+backspace sends the ctrl+alt+del combination
