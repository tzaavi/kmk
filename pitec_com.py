import usb_hid
from kmk.extensions import Extension
from kmk.utils import Debug
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.modules import Module

debug = Debug("code")

# fmt: off
REPORT_COUNT = 63  # size of report in bytes

# parer: https://eleccelerator.com/usbdescreqparser/#
CUSTOM_REPORT_DESCRIPTOR = bytes((
    0x06, 0x00, 0xff,  # Usage page (Vendor Defined Page1)
    0x09, 0x01,        # Usage (Vendor Page 1)
    0xA1, 0x01,        # Collection (Application)

    0x85, 0x07,        # Report ID (1)
    0x09, 0x00,        # Usage Page (Undefined)
    0x15, 0x00,        # Logical Minimum (0)
    0x26, 0xFF, 0x00,  # Logical Maximum (255)
    0x75, 0x08,        # Report Size (8 bits)
    0x95, REPORT_COUNT, # Report Count (64 fields)
    0x82, 0x02, 0x01,  # Input (Data,Var,Abs,Buf)

    0x85, 0x08,        # Report ID (2)
    0x09, 0x00,        # Usage (Undefined)
    0x09, 0x00,        # Usage Page (Undefined)
    0x15, 0x00,        # Logical Minimum (0)
    0x26, 0xFF, 0x00,  # Logical Maximum (255)
    0x75, 0x08,        # Report Size (8 bits)
    0x95, REPORT_COUNT, # Report Count (64 fields)
    0x92, 0x02, 0x01,  # Output (Data,Var,Abs,Buf)

    0xC0,        # End Collection
))
# fmt: on

usage_page = 0xFF00
usage = 0x01

pitec_com_hid = usb_hid.Device(
    report_descriptor=CUSTOM_REPORT_DESCRIPTOR,
    usage_page=usage_page,  # Vendor defined
    usage=usage,  # Vendor page 1
    report_ids=(7, 8),
    in_report_lengths=(REPORT_COUNT, 0),
    out_report_lengths=(0, REPORT_COUNT),
)


class PiTecCom(Module):
    def __init__(self):
        self.hid = None

    def __repr__(self):
        return "(PiTecCom)"

    def during_bootup(self, keyboard: KMKKeyboard):
        for dev in usb_hid.devices:
            if (
                dev.usage_page == usage_page
                and dev.usage == usage
                and hasattr(dev, "send_report")
            ):
                self.hid = dev
                break
        if self.hid is None:
            raise ValueError("Could not find pitec HID device.")

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        return

    def before_hid_send(self, keyboard):
        return

    def after_hid_send(self, keyboard: KMKKeyboard):
        # https://gist.github.com/todbot/6c39e9f2e9719643e5be8f1c82cf9f79
        if self.hid is None:
            return
        out_report = self.hid.get_last_received_report(8)  # out from computer
        if out_report:
            print("len:", len(out_report), ["%02x" % x for x in out_report])
            keyboard.keymap = [
                [
                    KC.E,
                    KC.F,
                    KC.G,
                    KC.H,
                ]
            ]

    def on_powersave_enable(self, keyboard):
        return

    def on_powersave_disable(self, keyboard):
        return
