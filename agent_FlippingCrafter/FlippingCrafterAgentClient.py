import os
from uagents import Agent, Context, Model

FLIP_IMAGE_AGENT = "agent1qg35fcty0h6rysvq020upnjxgcjcjueep2g0hgksh7zc0dfqdqkgzq20nq8"

class FlipCrafterRequest(Model):
    image_path: str
    flip_type: str  # "horizontal" or "vertical"

class FlipCrafterResponse(Model):
    flipped_image_path: str
    flip_type: str

client_agent = Agent(
    name="FlipCrafterClientAgent",
    port=5064,
    seed="FlipCrafterClientAgentSeed",
    endpoint="http://localhost:5064/submit"
)

@client_agent.on_event('startup')
async def send_request(ctx: Context):
    image_path = input("Enter the image path to flip: ")
    flip_type = input("Enter flip type (horizontal/vertical): ").strip().lower()

    if flip_type not in ["horizontal", "vertical"]:
        print("Error: Invalid flip type! Choose 'horizontal' or 'vertical'.")
        return

    ctx.logger.info(f"Sending request to flip image: {image_path} ({flip_type})...")
    request = FlipCrafterRequest(image_path=image_path, flip_type=flip_type)
    await ctx.send(FLIP_IMAGE_AGENT, request)

@client_agent.on_message(model=FlipCrafterResponse)
async def handle_response(ctx: Context, sender: str, msg: FlipCrafterResponse):
    print(f'{"=" * 20} Flipped Image {"=" * 20}')
    print(f"Flipped Image Saved at: {msg.flipped_image_path} (Type: {msg.flip_type})")
    print(f'{"=" * 20}=============={"=" * 20}')

if __name__ == "__main__":
    client_agent.run()
