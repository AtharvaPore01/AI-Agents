from datetime import datetime
from uuid import uuid4
from typing import Any

from uagents import Context, Model, Protocol

#Import the necessary components of the chat protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec
)

from information_classifier import run_process, InformationRequestModel

#Replace the AI Agent Address with anyone of the following LLMs as they support StructuredOutput required for the processing of this agent. 


AI_AGENT_ADDRESS = 'agent1qtauvslzzjuuel22905s4wjztmf0h9903fwqnmcuvysk0w40f75nua3vplu'

if not AI_AGENT_ADDRESS:
    raise ValueError("AI_AGENT_ADDRESS not set")


def create_text_chat(text: str, end_session: bool = True) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(
        timestamp=datetime.utcnow(),
        msg_id=uuid4(),
        content=content,
    )


chat_proto = Protocol(spec=chat_protocol_spec)
struct_output_client_proto = Protocol(
    name="StructuredOutputClientProtocol", version="0.1.0"
)


class StructuredOutputPrompt(Model):
    prompt: str
    output_schema: dict[str, Any]


class StructuredOutputResponse(Model):
    output: dict[str, Any]


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    ctx.logger.info(f"Got a message from {sender}: {msg.content[0].text}")
    ctx.storage.set(str(ctx.session), sender)
    await ctx.send(
        sender,
        ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id),
    )

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Got a start session message from {sender}")
            continue
        elif isinstance(item, TextContent):
            ctx.logger.info(f"Got a message from {sender}: {item.text}")
            ctx.storage.set(str(ctx.session), sender)
            await ctx.send(
                AI_AGENT_ADDRESS,
                StructuredOutputPrompt(
                    prompt=f'You are an echo agent. Return exactly and only the text that comes after the colon in the input. Do not modify, correct, interpret, rephrase, or analyze it. No extra words, no explanations, no formatting. Just echo it back exactly as it was input.Input:{item.text}', 
                    output_schema=InformationRequestModel.schema()
                ),
            )
        else:
            ctx.logger.info(f"Got unexpected content from {sender}")


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(
        f"Got an acknowledgement from {sender} for {msg.acknowledged_msg_id}"
    )


@struct_output_client_proto.on_message(StructuredOutputResponse)
async def handle_structured_output_response(
    ctx: Context, sender: str, msg: StructuredOutputResponse
):
    #print(f'###################{str(msg.output)}###################')
    #prompt = InformationRequestModel.parse_obj(msg.output)
    #print(f'Prompt: ###################{prompt}###################')
    session_sender = ctx.storage.get(str(ctx.session))
    
    if session_sender is None:
        ctx.logger.error(
            "Discarding message because no session sender found in storage"
        )
        return

    if "<UNKNOWN>" in str(msg.output):
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your location request. Please try again later."
            ),
        )
        return

    prompt = InformationRequestModel.parse_obj(msg.output)
    print(f'Prompt.information: ###################{prompt.information}###################')
    try:
        info = await run_process(prompt.information)
    except Exception as err:
        ctx.logger.error(err)
        await ctx.send(
            session_sender,
            create_text_chat(
                "Sorry, I couldn't process your request. Please try again later."
            ),
        )
        return

    if "error" in info:
        await ctx.send(session_sender, create_text_chat(str(info["error"])))
        return

    print(f'info type: {type(info)}')
    print(f'info: {info}')
    chat_message = create_text_chat(str(info))

    await ctx.send(session_sender, chat_message)
    