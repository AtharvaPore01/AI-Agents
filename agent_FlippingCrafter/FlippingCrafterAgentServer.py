import os
import cv2
from uagents import Agent, Context, Model

CLIENT_AGENT_ADDRESS = "agent1qtw6ryv7tmnk7ta4vf97vd9pm7g9t8scmufxxgav3jp3xq4rx9k35t30j3x"

class FlipCrafterRequest(Model):
    image_path: str
    flip_type: str  # "horizontal" or "vertical"

class FlipCrafterResponse(Model):
    flipped_image_path: str
    flip_type: str

FlipCrafterAgent = Agent(
    name="FlipCrafterServerAgent",
    port=5004,
    endpoint="http://localhost:5004/submit",
    seed="FlipCrafterAgentSeed"
)

def flip_image(image_path, flip_type):
    save_path = os.path.dirname(image_path)
    image_name = os.path.basename(image_path).split('.')

    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Could not read the image at {image_path}")
        return None, None

    # Perform flipping
    if flip_type == "horizontal":
        flipped = cv2.flip(image, 1)  # Flip along the Y-axis
    elif flip_type == "vertical":
        flipped = cv2.flip(image, 0)  # Flip along the X-axis
    else:
        print(f"Error: Unsupported flip type {flip_type}. Use 'horizontal' or 'vertical'.")
        return None, None

    # Save the flipped image
    flipped_image_name = f"{image_name[0]}_flipped_{flip_type}.{image_name[1]}"
    flipped_image_path = os.path.join(save_path, flipped_image_name)

    os.makedirs(os.path.dirname(flipped_image_path), exist_ok=True)
    cv2.imwrite(flipped_image_path, flipped)

    print(f"Flipped image saved as '{flipped_image_path}' with type {flip_type}")
    return flipped_image_path, flip_type

@FlipCrafterAgent.on_message(model=FlipCrafterRequest)
async def handle_request(ctx: Context, sender: str, request: FlipCrafterRequest):
    flipped_image_path, flip_type = flip_image(request.image_path, request.flip_type)

    if flipped_image_path:
        await ctx.send(
            CLIENT_AGENT_ADDRESS,
            FlipCrafterResponse(flipped_image_path=flipped_image_path, flip_type=flip_type)
        )

if __name__ == "__main__":
    FlipCrafterAgent.run()
