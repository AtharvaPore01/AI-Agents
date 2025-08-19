import os
import subprocess
import platform
from uagents import Agent, Context, Model

imagePath = ''
imageWidth = 0
imageHeight = 0

RESIZE_IMAGE_AGENT = "agent1qfve6yghlatlnckf76t8lgn9870zgjwrre7nrlsh7qzvw87r2ypyuzmw0hl"

class ResizeCrafterRequest(Model):
    image_path: str
    width: int
    height: int

class ResizeCrafterResponse(Model):
    resized_image_path: str

client_agent = Agent(
    name="ResizeCrafterClientAgent",
    port=5061,
    seed="ResizeCrafterClientAgentSeed",
    endpoint="http://localhost:5061/submit"
)

def prepare_query(img_path: str, width: int, height: int) -> None:
    """
    Sets the global image path, width, and height variables.
    """
    global imagePath, imageWidth, imageHeight
    imagePath = img_path
    imageWidth = width
    imageHeight = height

@client_agent.on_event('startup')
async def send_request(ctx: Context):
    ctx.logger.info(f"Sending request to resize image: {imagePath} to {imageWidth}x{imageHeight}...")
    request = ResizeCrafterRequest(image_path=imagePath, width=imageWidth, height=imageHeight)
    await ctx.send(RESIZE_IMAGE_AGENT, request)

@client_agent.on_message(model=ResizeCrafterResponse)
async def handle_response(ctx: Context, sender: str, msg: ResizeCrafterResponse):
    print(f'{"=" * 20} Resized Image {"=" * 20}')
    print(f"Resized Image Saved at: {msg.resized_image_path}")
    print(f'{"=" * 20}=============={"=" * 20}')
    print('Opening the resized image...')

    # Open the image based on OS
    if platform.system() == "Darwin":  # macOS
        subprocess.run(["open", msg.resized_image_path])
    elif platform.system() == "Windows":  # Windows
        os.startfile(msg.resized_image_path)
    else:  # Linux
        subprocess.run(["xdg-open", msg.resized_image_path])

if __name__ == "__main__":
    img_path = input('Enter the image path to be resized: ')
    width = int(input('Enter the new width: '))
    height = int(input('Enter the new height: '))
    prepare_query(img_path, width, height)
    client_agent.run()
