from . import client
from PIL import Image, ImageDraw, ImageFont
from asyncio import get_event_loop

async def download_image(url: str, name: str) -> str:
	file = await client.req.make_async_request("GET", api=url)
	ext = url.split(".")[-1]
	data = await file.get_bytes()
	with open(f"cache/{name}.{ext}", "wb") as f:
		f.write(data)
	
	return f"cache/{name}.{ext}"

async def create_greeting_image(
    nick: str,
    chat_name: str,
    participants_count: int,
    avatar_path: str,
    output_path: str,
    background_path: str = "background.png",
    image_width: int = 800,
    image_height: int = 450
) -> str:
    def _create_image():
        try:
            img = Image.open(background_path).convert("RGB")
            img = img.resize((image_width, image_height), Image.Resampling.LANCZOS)
        except:
            img = Image.new("RGB", (image_width, image_height), color=(45, 85, 140))
            draw = ImageDraw.Draw(img)
            for y in range(image_height):
                ratio = y / image_height
                r = int(45 + (100 - 45) * ratio)
                g = int(85 + (160 - 85) * ratio)
                b = int(140 + (200 - 140) * ratio)
                draw.line([(0, y), (image_width, y)], fill=(r, g, b))
        
        overlay = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 60))
        img = img.convert("RGBA")
        img = Image.alpha_composite(img, overlay)
        img = img.convert("RGB")
        
        avatar = Image.open(avatar_path).convert("RGBA")
        avatar_size = 220
        avatar = avatar.resize((avatar_size, avatar_size), Image.Resampling.LANCZOS)
        
        mask = Image.new("L", (avatar_size, avatar_size), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, avatar_size, avatar_size), fill=255)
        avatar.putalpha(mask)
        
        border_size = avatar_size + 12
        border = Image.new("RGBA", (border_size, border_size), (255, 255, 255, 0))
        border_draw = ImageDraw.Draw(border)
        border_draw.ellipse((0, 0, border_size, border_size), fill=(255, 255, 255, 255))
        border.paste(avatar, (6, 6), avatar)
        

        avatar_x = 60
        avatar_y = (image_height - border_size) // 2
        img.paste(border, (avatar_x, avatar_y), border)
        
        draw = ImageDraw.Draw(img)
        
        try:
            title_font = ImageFont.truetype("fonts/DejaVuSans-Bold.ttf", 56)
            welcome_font = ImageFont.truetype("fonts/DejaVuSans.ttf", 32)
            info_font = ImageFont.truetype("fonts/DejaVuSans.ttf", 26)
        except OSError:
            title_font = ImageFont.load_default()
            welcome_font = ImageFont.load_default()
            info_font = ImageFont.load_default()

        text_x = avatar_x + border_size + 70
        text_y_start = 80
        line_spacing = 20
        
        welcome_text = "Welcome to"
        shadow_offset = 2
        draw.text(
            (text_x + shadow_offset, text_y_start + shadow_offset),
            welcome_text,
            fill=(0, 0, 0, 120),
            font=welcome_font
        )
        draw.text(
            (text_x, text_y_start),
            welcome_text,
            fill=(220, 220, 220),
            font=welcome_font
        )
        
        chat_text = chat_name
        draw.text(
            (text_x + shadow_offset, text_y_start + 50 + shadow_offset),
            chat_text,
            fill=(0, 0, 0, 150),
            font=title_font
        )
        draw.text(
            (text_x, text_y_start + 50),
            chat_text,
            fill=(255, 255, 255),
            font=title_font
        )
        
        info_text = f"{nick}"
        draw.text(
            (text_x, text_y_start + 130),
            info_text,
            fill=(200, 200, 200),
            font=info_font
        )
        
        members_text = f"{participants_count} members"
        draw.text(
            (text_x, text_y_start + 165),
            members_text,
            fill=(200, 200, 200),
            font=info_font
        )
        
        img.save(output_path, "PNG", quality=95)
        return output_path
    
    loop = get_event_loop()
    result = await loop.run_in_executor(None, _create_image)
    return result