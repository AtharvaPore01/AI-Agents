import os
import subprocess
import platform
from uagents import Agent, Context, Model

imagePath = ''
brightness = 1.0
contrast = 1.0
saturation = 1.0

COLOR_ADJUST_AGENT = "agent1qf6jgazryggqlqetd8kg0vtmcptfg8evv9zhyht3npfck3v96elc7nj0z8h"

# Request & Response Models (Must Match Server)
class ColorGenixRequest(Model):
    image_path: str
    brightness: float
    contrast: float
    saturation: float

class ColorGenixResponse(Model):
    processed_image_path: str

client_agent = Agent(
    name="ColorGenixClientAgent",
    port=5070,
    seed="ColorGenixClientAgentSeed",
    endpoint="http://localhost:5070/submit"
)

def prepare_query(usr_query: str, usr_brightness: float, usr_contrast: float, usr_saturation: float) -> None:
    """
    Sets the global variables for image path and color adjustment parameters.
    """
    global imagePath, brightness, contrast, saturation
    imagePath = usr_query
    brightness = usr_brightness
    contrast = usr_contrast
    saturation = usr_saturation

@client_agent.on_event('startup')
async def send_request(ctx: Context):
    ctx.logger.info(f"Sending request to adjust image colors: {imagePath}...")
    request = ColorGenixRequest(
        image_path=imagePath, 
        brightness=brightness, 
        contrast=contrast, 
        saturation=saturation
    )
    await ctx.send(COLOR_ADJUST_AGENT, request)

@client_agent.on_message(model=ColorGenixResponse)
async def handle_response(ctx: Context, sender: str, msg: ColorGenixResponse):
    print(f'{"=" * 20} Processed Image {"=" * 20}')
    print(f"Processed Image Saved at: {msg.processed_image_path}")
    print(f'{"=" * 20}================{"=" * 20}')
    print('Opening the processed image...')

    # Open the image based on OS
    if platform.system() == "Darwin":  # macOS
        subprocess.run(["open", msg.processed_image_path])
    elif platform.system() == "Windows":  # Windows
        os.startfile(msg.processed_image_path)
    else:  # Linux
        subprocess.run(["xdg-open", msg.processed_image_path])

if __name__ == "__main__":
    img_path = input('Enter the image path for color adjustment: ')
    brightness = float(input('Enter brightness factor (1.0 = no change): '))
    contrast = float(input('Enter contrast factor (1.0 = no change): '))
    saturation = float(input('Enter saturation factor (1.0 = no change): '))

    prepare_query(img_path, brightness, contrast, saturation)
    client_agent.run()
