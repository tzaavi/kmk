import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.serialace import SerialACE
from pitec_com import PiTecCom

keyboard = KMKKeyboard()
keyboard.debug_enabled = True
keyboard.col_pins = (board.TX, board.RX)
keyboard.row_pins = (board.D2, board.D3)
keyboard.diode_orientation = DiodeOrientation.COL2ROW
keyboard.modules.append(SerialACE())
keyboard.modules.append(PiTecCom())

keyboard.keymap = [
    [
        KC.A,
        KC.B,
        KC.C,
        KC.D,
    ]
]

if __name__ == "__main__":
    keyboard.go(https://github.com/glucometers-tech/freestyle-hid.git)
