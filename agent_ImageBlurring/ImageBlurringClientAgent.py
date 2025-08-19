import os
import subprocess
import platform
from uagents import Agent, Context, Model

imagePath = ''
blurType = ''
kernelSize = 0

BLUR_IMAGE_AGENT = "agent1q2e2mve6kk8gyp5q645jl688awau6zsqt89e0qprth6y7lkvz4gpyllkqku"

class BlurRequest(Model):
    image_path: str
    blur_type: str  # 'gaussian', 'median', or 'bilateral'
    kernel_size: int  # Kernel size for blurring

class BlurResponse(Model):
    blurred_image_path: str
    blur_type: str  # Confirmed blur type
    kernel_size: int  # Confirmed kernel size

client_agent = Agent(
    name="BlurCrafterClientAgent",
    port=5071,
    seed="BlurCrafterClientAgentSeed",
    endpoint="http://localhost:5071/submit"
)

def prepare_query(usr_query: str, usr_blur_type: str, usr_kernel_size: int) -> None:
    """
    Sets the global variables for imagePath, blurType, and kernelSize.
    """
    global imagePath, blurType, kernelSize
    imagePath = usr_query
    blurType = usr_blur_type
    kernelSize = usr_kernel_size

@client_agent.on_event('startup')
async def send_request(ctx: Context):
    ctx.logger.info(f"Sending request to apply {blurType} blur with kernel size {kernelSize} on image: {imagePath}...")
    request = BlurRequest(image_path=imagePath, blur_type=blurType, kernel_size=kernelSize)
    await ctx.send(BLUR_IMAGE_AGENT, request)

@client_agent.on_message(model=BlurResponse)
async def handle_response(ctx: Context, sender: str, msg: BlurResponse):
    print(f'{"=" * 20} Blurred Image {"=" * 20}')
    print(f"Blurred Image Saved at: {msg.blurred_image_path}")
    print(f"Blur Type: {msg.blur_type}")
    print(f"Kernel Size: {msg.kernel_size}")
    print(f'{"=" * 20}=============={"=" * 20}')
    print('Opening the blurred image...')
    
    # Open the image based on OS
    if platform.system() == "Darwin":  # macOS
        subprocess.run(["open", msg.blurred_image_path])
    elif platform.system() == "Windows":  # Windows
        os.startfile(msg.blurred_image_path)
    else:  # Linux
        subprocess.run(["xdg-open", msg.blurred_image_path])

if __name__ == "__main__":
    img_path = input('Enter the image path: ')
    blur_type = input('Choose blur type (gaussian, median, bilateral): ').strip().lower()
    kernel_size = int(input('Enter the kernel size (must be an odd number): '))
    
    if kernel_size % 2 == 0:
        print("Error: Kernel size must be an odd number!")
        exit(1)

    prepare_query(img_path, blur_type, kernel_size)
    client_agent.run()
