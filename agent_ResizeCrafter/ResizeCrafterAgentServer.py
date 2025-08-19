import os
import cv2
from uagents import Agent, Context, Model

CLIENT_AGENT_ADDRESS = "agent1qvfs476ta09v5tkvtwtwvascgwtpz5pcxxdrg0dydyl6e9cvevx3z2nyel3"

class ResizeCrafterRequest(Model):
    image_path: str
    width: int
    height: int

class ResizeCrafterResponse(Model):
    resized_image_path: str

ResizeCrafterAgent = Agent(
    name="ResizeCrafterServerAgent",
    port=5003,
    endpoint="http://localhost:5003/submit",
    seed="ResizeCrafterAgentSeed"
)

def resize_image(image_path, width, height):
    if not os.path.exists(image_path):
        print("Error: Image file not found.")
        return None

    save_path = os.path.dirname(image_path)
    image_name = os.path.basename(image_path).split('.')
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Unable to read image.")
        return None

    resized_image = cv2.resize(image, (width, height))  # Resize operation

    resized_image_name = image_name[0] + '_resized.' + image_name[1]
    save_path = os.path.join(save_path, resized_image_name)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    cv2.imwrite(save_path, resized_image)  # Save resized image

    print(f"Resized image saved as '{save_path}'")
    return save_path

@ResizeCrafterAgent.on_message(model=ResizeCrafterRequest)
async def handle_request(ctx: Context, sender: str, request: ResizeCrafterRequest):
    resized_image_path = resize_image(request.image_path, request.width, request.height)
    await ctx.send(CLIENT_AGENT_ADDRESS, ResizeCrafterResponse(resized_image_path=resized_image_path))

if __name__ == "__main__":
    ResizeCrafterAgent.run()
