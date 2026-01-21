import os
import asyncio
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv()

def run_agent_for_room(room_name):
    """Run agent for a specific room using CLI command"""
    try:
        print(f"🤖 Starting agent for room: {room_name}")
        
        # Set environment variable for the room
        env = os.environ.copy()
        env['LIVEKIT_ROOM'] = room_name
        
        # Run the agent using the LiveKit CLI
        # The agent will now listen for connections to this specific room
        result = subprocess.run([
            'python', 'agent.py', 'connect', '--room', room_name
        ], env=env)
        
        if result.returncode == 0:
            print(f"✅ Agent finished for room: {room_name}")
        else:
            print(f"❌ Agent exited with error for room: {room_name}")
            
    except Exception as e:
        print(f"❌ Error running agent: {e}")

def main():
    if len(sys.argv) > 1:
        room_name = sys.argv[1]
    else:
        room_name = input("🎯 Enter LiveKit room name: ").strip()
    
    if not room_name:
        print("❌ Room name is required")
        return
    
    run_agent_for_room(room_name)

if __name__ == "__main__":
    main()