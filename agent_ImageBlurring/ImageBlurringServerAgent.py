import os
import cv2
from uagents import Agent, Context, Model

CLIENT_AGENT_ADDRESS = "agent1qg548jy58678szs0sxtgtnvx62rdxpsu3kgq4wfcd3fctmkndqjwznzfr5c"

class BlurRequest(Model):
    image_path: str
    blur_type: str  # 'gaussian', 'median', or 'bilateral'
    kernel_size: int  # Kernel size for blurring

class BlurResponse(Model):
    blurred_image_path: str
    blur_type: str  # Confirmed blur type
    kernel_size: int  # Confirmed kernel size

BlurCrafterAgent = Agent(
    name="BlurCrafterServerAgent",
    port=5007,
    endpoint="http://localhost:5007/submit",
    seed="BlurCrafterAgentSeed"
)

def apply_blur(image_path, blur_type, kernel_size):
    save_path = os.path.dirname(image_path)
    image_name = os.path.basename(image_path).split('.')

    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not read the image at {image_path}")
        return None, None, None

    if blur_type == "gaussian":
        blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    elif blur_type == "median":
        blurred = cv2.medianBlur(image, kernel_size)
    elif blur_type == "bilateral":
        blurred = cv2.bilateralFilter(image, kernel_size, 75, 75)
    else:
        print(f"Error: Unsupported blur type '{blur_type}'. Use 'gaussian', 'median', or 'bilateral'.")
        return None, None, None

    # Save the blurred image
    blurred_image_name = f"{image_name[0]}_{blur_type}_blurred.{image_name[1]}"
    blurred_image_path = os.path.join(save_path, blurred_image_name)

    os.makedirs(os.path.dirname(blurred_image_path), exist_ok=True)
    cv2.imwrite(blurred_image_path, blurred)

    print(f"Blurred image saved as '{blurred_image_path}' using {blur_type} blur with kernel size {kernel_size}")
    return blurred_image_path, blur_type, kernel_size

@BlurCrafterAgent.on_message(model=BlurRequest)
async def handle_request(ctx: Context, sender: str, request: BlurRequest):
    blurred_image_path, blur_type, kernel_size = apply_blur(request.image_path, request.blur_type, request.kernel_size)

    if blurred_image_path:
        await ctx.send(
            CLIENT_AGENT_ADDRESS,
            BlurResponse(blurred_image_path=blurred_image_path, blur_type=blur_type, kernel_size=kernel_size)
        )

if __name__ == "__main__":
    BlurCrafterAgent.run()
