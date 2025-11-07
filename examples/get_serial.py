import hid

VENDOR_ID  = 0x256f
PRODUCT_ID = 0xc635  # SpaceMouse Compact

for d in hid.enumerate(VENDOR_ID, PRODUCT_ID):
    print("Product:", d.get("product_string"))
    print("Manufacturer:", d.get("manufacturer_string"))
    print("Serial number:", d.get("serial_number"))
    print("Path:", d.get("path"))
    print()