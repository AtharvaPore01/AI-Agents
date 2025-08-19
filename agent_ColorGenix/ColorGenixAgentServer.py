import os
import cv2
import numpy as np
from uagents import Agent, Context, Model

CLIENT_AGENT_ADDRESS = "agent1qd3v4vsy7tgtqslv06t07xva8q8rd29p82f4ckz9r44nh7r3myyhkdxvvj8"

# Define request & response models
class ColorGenixRequest(Model):
    image_path: str
    brightness: float
    contrast: float
    saturation: float

class ColorGenixResponse(Model):
    processed_image_path: str

ColorAdjustAgent = Agent(
    name="ColorGenixServerAgent",
    port=5003,
    endpoint="http://localhost:5003/submit",
    seed="ColorGenixAgentSeed"
)

# Function to adjust color properties
def adjust_colors(image, brightness=1.0, contrast=1.0, saturation=1.0):
    # Convert to HSV to adjust saturation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[:, :, 1] *= saturation  # Adjust saturation
    hsv = np.clip(hsv, 0, 255).astype(np.uint8)
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Adjust brightness & contrast
    image = cv2.convertScaleAbs(image, alpha=contrast, beta=brightness * 50)
    return image

# Function to apply adjustments and save the processed image
def process_image(image_path, brightness, contrast, saturation):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read the image at {image_path}")
        return None

    save_path = os.path.dirname(image_path)
    processed_image_name = f"processed_{os.path.basename(image_path)}"
    processed_image_path = os.path.join(save_path, processed_image_name)

    # Apply brightness, contrast, and saturation adjustments
    processed_image = adjust_colors(image, brightness, contrast, saturation)

    os.makedirs(save_path, exist_ok=True)
    cv2.imwrite(processed_image_path, processed_image)
    
    return processed_image_path

@ColorAdjustAgent.on_message(model=ColorGenixRequest)
async def handle_request(ctx: Context, sender: str, request: ColorGenixRequest):
    processed_path = process_image(request.image_path, request.brightness, request.contrast, request.saturation)

    if processed_path:
        await ctx.send(
            CLIENT_AGENT_ADDRESS,
            ColorGenixResponse(processed_image_path=processed_path)
        )
        print(f"Processed image sent to client: {processed_path}")
    else:
        print("Processing failed. No image was sent.")

if __name__ == "__main__":
    ColorAdjustAgent.run()
