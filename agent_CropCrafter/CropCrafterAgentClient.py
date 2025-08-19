import os
import subprocess
import platform
from uagents import Agent, Context, Model

imagePath = ''

CROP_IMAGE_AGENT = 'agent1q2508al73s82tu6hq5jdllqfc7szde2ehz6qrsclkfs6fpjxna5w230tuen'

class CropCrafterRequest(Model):
    image_path: str

class CropCrafterResponse(Model):
    cropped_image_path: str

client_agent = Agent(
    name="CropCrafterClientAgent",
    port=5060,
    seed="CropCrafterClientAgentSeed",
    endpoint="http://localhost:5060/submit"
)

def prepare_query(usr_query: str) -> None:
    """
    Sets the global imagePath variable.
    """
    global imagePath
    imagePath = usr_query

@client_agent.on_event('startup')
async def send_request(ctx: Context):
    ctx.logger.info(f"Sending request to crop image: {imagePath}...")
    request = CropCrafterRequest(image_path=imagePath)
    await ctx.send(CROP_IMAGE_AGENT, request)

@client_agent.on_message(model=CropCrafterResponse)
async def handle_response(ctx: Context, sender: str, msg: CropCrafterResponse):
    print(f'{"=" * 20} Cropped Image {"=" * 20}')
    print(f"Cropped Image Saved at: {msg.cropped_image_path}")
    print(f'{"=" * 20}=============={"=" * 20}')
    print('Opening the cropped image...')

if __name__ == "__main__":
    img_path = input('Give the image path to be cropped: ')
    prepare_query(img_path)
    client_agent.run()
