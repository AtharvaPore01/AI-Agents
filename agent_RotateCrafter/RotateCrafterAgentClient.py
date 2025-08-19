import os
import subprocess
import platform
from uagents import Agent, Context, Model

imagePath = ''
rotationAngle = 0

ROTATE_IMAGE_AGENT = "agent1q2p7d9d8wp8cw3enu674hcrqy997w0urnmtymcxyy3ylftpryxhyytvkx93"

class RotateCrafterRequest(Model):
    image_path: str
    angle: int  # User-specified rotation angle

class RotateCrafterResponse(Model):
    rotated_image_path: str
    angle: int  # Confirmed rotation angle

client_agent = Agent(
    name="RotateCrafterClientAgent",
    port=5070,
    seed="RotateCrafterClientAgentSeed",
    endpoint="http://localhost:5070/submit"
)

def prepare_query(usr_query: str, usr_angle: int) -> None:
    """
    Sets the global variables for imagePath and rotationAngle.
    """
    global imagePath, rotationAngle
    imagePath = usr_query
    rotationAngle = usr_angle

@client_agent.on_event('startup')
async def send_request(ctx: Context):
    ctx.logger.info(f"Sending request to rotate image: {imagePath} at {rotationAngle}°...")
    request = RotateCrafterRequest(image_path=imagePath, angle=rotationAngle)
    await ctx.send(ROTATE_IMAGE_AGENT, request)

@client_agent.on_message(model=RotateCrafterResponse)
async def handle_response(ctx: Context, sender: str, msg: RotateCrafterResponse):
    print(f'{"=" * 20} Rotated Image {"=" * 20}')
    print(f"Rotated Image Saved at: {msg.rotated_image_path}")
    print(f"Rotation Angle: {msg.angle}°")
    print(f'{"=" * 20}=============={"=" * 20}')
    print('Opening the rotated image...')
    
   # Open the image based on OS
    if platform.system() == "Darwin":  # macOS
        subprocess.run(["open", msg.resized_image_path])
    elif platform.system() == "Windows":  # Windows
        os.startfile(msg.resized_image_path)
    else:  # Linux
        subprocess.run(["xdg-open", msg.resized_image_path])

if __name__ == "__main__":
    img_path = input('Give the image path to be rotated: ')
    angle = int(input('Enter the rotation angle (in degrees): '))
    prepare_query(img_path, angle)
    client_agent.run()
