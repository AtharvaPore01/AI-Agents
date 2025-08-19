import json
import subprocess
import time
from uagents import Agent, Context, Model

# Start the shell script before anything else
print("Starting n8n service...")
subprocess.Popen(["bash", "/Users/aishwaryadekhane/Desktop/My_Files/Fetch.ai/Project/Sub_Agents/Technical_Analyst/open_n8n.sh"])

# Wait for a few seconds to ensure n8n starts properly
time.sleep(10)  # Adjust this if needed

REQUEST_FORWARDING_AGENT_ADDRESS = 'address'

# Define the request model (to be sent to the forwarding agent)
class requestForwardAgent(Model):
    query: str
    sender_address: str

# Define the response model (from the forwarding agent)
class responseForwardAgent(Model):
    result: str
    source: str

# Define the client agent
clientAgent = Agent(
    name='client_agent',
    port=5070,  # Specify the port for the client agent
    endpoint='http://localhost:5070/submit',  # Specify endpoint for the client agent
    seed='client_agent_seed'
)

# Handle the response from the forwarding agent
@clientAgent.on_message(model=responseForwardAgent)
async def handle_response(ctx: Context, sender: str, msg: responseForwardAgent):
    ctx.logger.info(f"Received response from {sender}: {msg.result}")
    print(f"Received result: {msg.result}")
    print(f"Source: {msg.source}")

def prepare_query(usr_query: str) -> None:
    """
    Sets the global USER QUERY variable.

    Parameters:
        usr_query (str): The incoming user query
    """
    global query
    query = usr_query

# Start the client agent
@clientAgent.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f'Client Agent {ctx.agent.name} started at {ctx.agent.address}')
    
    # Send a sample query to the forwarding agent
    sender_address = clientAgent.address
    request = requestForwardAgent(query=query, sender_address=sender_address)

    # Send the query to the forwarding agent
    await ctx.send(REQUEST_FORWARDING_AGENT_ADDRESS, request)

if __name__ == '__main__':
    query = str(input('Enter your query: '))
    prepare_query(query)
    clientAgent.run()
