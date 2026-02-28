from dotenv import load_dotenv
import os

# 1. Load the base .env first to get AGENT_TYPE
load_dotenv()

AGENT_TYPE = os.getenv("AGENT_TYPE", "interviewer").lower()

# 2. Conditionally load the specific environment variables, overriding the base ones if they exist
if AGENT_TYPE == "therapist":
    load_dotenv(".env.therapist", override=True)
else:
    load_dotenv(".env.interviewer", override=True)


from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    noise_cancellation,
)
from livekit.plugins import google
from prompts import (
    AGENT_INSTRUCTION, SESSION_INSTRUCTION,
    THERAPIST_AGENT_INSTRUCTION, THERAPIST_SESSION_INSTRUCTION
)
from tools import get_weather, search_web, send_email

if AGENT_TYPE == "therapist":
    selected_agent_instruction = THERAPIST_AGENT_INSTRUCTION
    selected_session_instruction = THERAPIST_SESSION_INSTRUCTION
    # Use a refined male voice for the Therapist (Puck or Charon)
    selected_voice = "Puck" 
else:
    selected_agent_instruction = AGENT_INSTRUCTION
    selected_session_instruction = SESSION_INSTRUCTION
    # Use the original female voice for the Interviewer
    selected_voice = "Aoede"


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=selected_agent_instruction,
            llm=google.beta.realtime.RealtimeModel(
            voice=selected_voice,
            temperature=0.8,
        ),
            tools=[
                get_weather,
                search_web,
                send_email
            ],

        )
        


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions=selected_session_instruction,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))