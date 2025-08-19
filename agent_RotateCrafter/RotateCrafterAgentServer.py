import os
import cv2
from uagents import Agent, Context, Model

CLIENT_AGENT_ADDRESS = "agent1qwhwj84zyw39hxyhcclx9ka2573py5ftatc92mw2wc98tvdj6e6cjrjjwjt"

class RotateCrafterRequest(Model):
    image_path: str
    angle: int  # User-specified angle

class RotateCrafterResponse(Model):
    rotated_image_path: str
    angle: int  # Confirmed rotation angle

RotateCrafterAgent = Agent(
    name="RotateCrafterServerAgent",
    port=5003,
    endpoint="http://localhost:5003/submit",
    seed="RotateCrafterAgentSeed"
)

def rotate_image(image_path, angle):
    save_path = os.path.dirname(image_path)
    image_name = os.path.basename(image_path).split('.')

    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Could not read the image at {image_path}")
        return None, None

    # Rotate the image based on user-specified angle
    if angle == 90:
        rotated = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif angle == 180:
        rotated = cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270:
        rotated = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        print(f"Error: Unsupported rotation angle {angle}. Use 90, 180, or 270 degrees.")
        return None, None

    # Save the rotated image
    rotated_image_name = f"{image_name[0]}_rotated_{angle}.{image_name[1]}"
    rotated_image_path = os.path.join(save_path, rotated_image_name)

    os.makedirs(os.path.dirname(rotated_image_path), exist_ok=True)
    cv2.imwrite(rotated_image_path, rotated)

    print(f"Rotated image saved as '{rotated_image_path}' with angle {angle}°")
    return rotated_image_path, angle

@RotateCrafterAgent.on_message(model=RotateCrafterRequest)
async def handle_request(ctx: Context, sender: str, request: RotateCrafterRequest):
    rotated_image_path, angle = rotate_image(request.image_path, request.angle)

    if rotated_image_path:
        await ctx.send(
            CLIENT_AGENT_ADDRESS,
            RotateCrafterResponse(rotated_image_path=rotated_image_path, angle=angle)
        )

if __name__ == "__main__":
    RotateCrafterAgent.run()
