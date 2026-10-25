import io
from PIL import Image

def create_image(image_bytes: bytes) -> io.BytesIO:
    # 建立空白畫布
    canvas = Image.new("RGBA", (600, 400), (255, 255, 255, 0))

    # 將圖片轉成 Image 物件並縮放為 300x200
    image = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    image = image.resize((300, 200))

    # 取得置中座標 (左上角座標)
    x = (canvas.width - image.width) // 2
    y = (canvas.height - image.height) // 2

    # 將圖片貼上
    canvas.paste(image, (x, y), image)

    # 將畫布存進記憶體
    buffer = io.BytesIO()
    canvas.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer

def create_inventory() -> io.BytesIO:
    slot = Image.open("slot.png").convert("RGBA")
    item = Image.open("item.png").convert("RGBA")

    canvas = Image.new("RGBA", (600, 400), (255, 255, 255, 0))
    canvas.paste(slot, (10, 10), slot)
    canvas.paste(item, (10 + 3, 10 + 3), item)

    buffer = io.BytesIO()
    canvas.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer