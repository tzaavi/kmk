import usb_cdc
import usb_hid
import pitec_com

usb_cdc.enable(data=True)


# import board
#
# from kmk.bootcfg import bootcfg
#
# bootcfg(
#     sense=board.TX,  # column
#     source=board.D2, # row
# )

usb_hid.enable( (pitec_com.pitec_com_hid, usb_hid.Device.CONSUMER_CONTROL, usb_hid.Device.KEYBOARD) )
