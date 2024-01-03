import usb_cdc
import usb_hid
from pitec.modules.row_hid import raw_hid_device


usb_cdc.enable(data=True)

# add pitec raw hid device
usb_hid.enable(
    (raw_hid_device, usb_hid.Device.CONSUMER_CONTROL, usb_hid.Device.KEYBOARD)
)
