from lib.canvas import create_inventory

with open("test.png", "rb") as f:
    buffer = create_inventory()

with open("out.png", "wb") as f:
    f.write(buffer.getvalue())