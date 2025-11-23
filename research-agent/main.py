import os
import time
import logfire
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel

from dotenv import load_dotenv
load_dotenv()

# Initialize Logfire
logfire.configure()

# Create Gemini model
model = GoogleModel(
    model_name="gemini-2.0-flash"
)

# Create agent
research_agent = Agent(
    name="research-agent",
    system_prompt=(
        "You are ResearchAgent. Provide clear, concise, deeply helpful answers.\n"
        "Do not exit unless the user types 'exit' or 'quit'."
    ),
    model=model
)

def chat_loop():

    # Print Logfire project URL before anything else
    project_url = os.getenv("LOGFIRE_PROJECT_URL")
    if project_url:
        print(f"Logfire project URL: {project_url}\n")

    print("Research Agent is running. Type 'exit' or 'quit' to stop.\n")
    
    # Add a 5-second delay before starting the chat
    # time.sleep(5)

    while True:
        time.sleep(4)
        user_input = input("You (type 'exit' to quit): ").strip()

        if user_input.lower() in ["exit", "quit"]:
            print("Shutting down the agent. Goodbye!")
            break

        with logfire.span("research-agent-query", question=user_input):
            try:
                response = research_agent.run_sync(user_input)
                print(f"\nAgent: {response}\n")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    chat_loop()
