import os
import cv2
import sys
from uagents import Agent, Context, Model

CLIENT_AGENT_ADDRESS = "agent1qdc693f5yk49ygxvg3w9af6fyhceh8xv4hdwnmd28wkrrqtdr0h0ufw6puk"

class CropCrafterRequest(Model):
    image_path: str

class CropCrafterResponse(Model):
    cropped_image_path: str

CropCrafterAgent = Agent(
    name="CropCrafterServerAgent",
    port=5002,
    endpoint="http://localhost:5002/submit",
    seed="CropCrafterAgentSeed"
)

def crop_image(image_path):
    save_path = os.path.dirname(image_path)
    image_name = os.path.basename(image_path).split('.')
    image = cv2.imread(image_path)
    cropped_image_name = image_name[0] + '_cropped.' + image_name[1]
    save_path = os.path.join(save_path, cropped_image_name)
    
    # OpenCV window name
    window_name = "Select Region"

    while True:
        roi = cv2.selectROI(window_name, image, fromCenter=False, showCrosshair=False)  # Removed grid
        
        if roi != (0, 0, 0, 0):  # If ROI is selected
            x, y, w, h = roi
            cropped = image[y:y+h, x:x+w]
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            cv2.imwrite(save_path, cropped)  # Save the cropped image
            print(f"Cropped image saved as '{save_path}'")
            
            cv2.destroyWindow(window_name)  # Explicitly close the specific window by its name
            
            return save_path
        else:
            print("No region selected.")
            return None

@CropCrafterAgent.on_message(model=CropCrafterRequest)
async def handle_request(ctx: Context, sender: str, request: CropCrafterRequest):
    cropped_image_path = crop_image(request.image_path)
    await ctx.send(CLIENT_AGENT_ADDRESS, CropCrafterResponse(cropped_image_path=cropped_image_path))

if __name__ == "__main__":
    CropCrafterAgent.run()
