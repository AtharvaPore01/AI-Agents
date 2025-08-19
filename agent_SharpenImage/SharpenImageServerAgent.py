import os
import cv2
import numpy as np
from uagents import Agent, Context, Model

CLIENT_AGENT_ADDRESS = "agent1qwrg987jq74xleadcdvzdjeq38x8kvx609atr4qm550mkrfkuvk0zdqaj42"

class SharpenRequest(Model):
    image_path: str
    intensity: float  # User-specified sharpening intensity

class SharpenResponse(Model):
    sharpened_image_path: str
    intensity: float  # Confirmed sharpening intensity

SharpVisionAgent = Agent(
    name="SharpVisionServerAgent",
    port=5004,
    endpoint="http://localhost:5004/submit",
    seed="SharpVisionAgentSeed"
)

def sharpen_image(image_path, intensity):
    save_path = os.path.dirname(image_path)
    image_name = os.path.basename(image_path).split('.')

    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Could not read the image at {image_path}")
        return None, None

    # Create a sharpening kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5 + intensity, -1],
                       [0, -1, 0]])

    sharpened = cv2.filter2D(image, -1, kernel)

    # Save the sharpened image
    sharpened_image_name = f"{image_name[0]}_sharpened_{intensity:.1f}.{image_name[1]}"
    sharpened_image_path = os.path.join(save_path, sharpened_image_name)

    os.makedirs(os.path.dirname(sharpened_image_path), exist_ok=True)
    cv2.imwrite(sharpened_image_path, sharpened)

    print(f"Sharpened image saved as '{sharpened_image_path}' with intensity {intensity}")
    return sharpened_image_path, intensity

@SharpVisionAgent.on_message(model=SharpenRequest)
async def handle_request(ctx: Context, sender: str, request: SharpenRequest):
    sharpened_image_path, intensity = sharpen_image(request.image_path, request.intensity)

    if sharpened_image_path:
        await ctx.send(
            CLIENT_AGENT_ADDRESS,
            SharpenResponse(sharpened_image_path=sharpened_image_path, intensity=intensity)
        )

if __name__ == "__main__":
    SharpVisionAgent.run()
