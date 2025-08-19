import os
import subprocess
import platform
from uagents import Agent, Context, Model

imagePath = ''
sharpenIntensity = 0.0

SHARPEN_IMAGE_AGENT = "agent1q07smzdrh4wdz5r94cppevyc6nrl0pcchaguw3jrn05ckhcrvjfxjhx23z2"

class SharpenRequest(Model):
    image_path: str
    intensity: float  # User-specified sharpening intensity

class SharpenResponse(Model):
    sharpened_image_path: str
    intensity: float  # Confirmed sharpening intensity

client_agent = Agent(
    name="SharpVisionClientAgent",
    port=5071,
    seed="SharpVisionClientAgentSeed",
    endpoint="http://localhost:5071/submit"
)

def prepare_query(usr_query: str, usr_intensity: float) -> None:
    """
    Sets the global variables for imagePath and sharpenIntensity.
    """
    global imagePath, sharpenIntensity
    imagePath = usr_query
    sharpenIntensity = usr_intensity

@client_agent.on_event('startup')
async def send_request(ctx: Context):
    ctx.logger.info(f"Sending request to sharpen image: {imagePath} with intensity {sharpenIntensity}...")
    request = SharpenRequest(image_path=imagePath, intensity=sharpenIntensity)
    await ctx.send(SHARPEN_IMAGE_AGENT, request)

@client_agent.on_message(model=SharpenResponse)
async def handle_response(ctx: Context, sender: str, msg: SharpenResponse):
    print(f'{"=" * 20} Sharpened Image {"=" * 20}')
    print(f"Sharpened Image Saved at: {msg.sharpened_image_path}")
    print(f"Sharpening Intensity: {msg.intensity}")
    print(f'{"=" * 20}================{"=" * 20}')
    print('Opening the sharpened image...')
    
    # Open the image based on OS
    if platform.system() == "Darwin":  # macOS
        subprocess.run(["open", msg.sharpened_image_path])
    elif platform.system() == "Windows":  # Windows
        os.startfile(msg.sharpened_image_path)
    else:  # Linux
        subprocess.run(["xdg-open", msg.sharpened_image_path])

if __name__ == "__main__":
    img_path = input('Give the image path to be sharpened: ')
    intensity = float(input('Enter the sharpening intensity (0.0 - 5.0): '))
    prepare_query(img_path, intensity)
    client_agent.run()
