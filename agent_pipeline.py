"""
Agentic SPICE Pipeline using google-antigravity SDK.

This script initializes the Antigravity Agent with full local capabilities
so it can autonomously generate SPICE netlists, test them with ngspice,
and verify their waveforms.
"""
import asyncio
import os
import sys
from google.antigravity import Agent, LocalAgentConfig, CapabilitiesConfig
from google.antigravity.utils.interactive import run_interactive_loop

# Define the persona and rules for the agent
SYSTEM_PROMPT = """You are an expert Power Electronics and SPICE engineering agent. 
Your goal is to autonomously design, test, and verify SPICE netlists for power converters.

Rules:
1. When asked to design a converter, look at the reference netlists in the 'Circuit Library' directory in the current workspace.
2. Generate the appropriate `.cir` file for the new design.
3. Automatically run ngspice using your command line tools to verify the circuit works and meets the requirements.
4. DO NOT generate PNG plots via Python. Instead, when the circuit is fully verified and ready for the user, 
   ensure the `.cir` file has a `.control` block that plots the key waveforms (e.g., `plot v(out)`), 
   and use your `run_command` tool to launch `ngspice <filename.cir>` so the native plot window pops up on the user's screen.
"""

async def main():
    print("Initializing Antigravity SPICE Agent...")
    
    # Ensure API key is available
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("\n[!] GEMINI_API_KEY not found in environment.")
        api_key = input("Please enter your Gemini API key (it will not be saved): ").strip()
        if not api_key:
            print("Error: API key is required to use the Antigravity SDK.")
            sys.exit(1)
        os.environ["GEMINI_API_KEY"] = api_key
    
    # Configure the agent with capabilities to run commands and edit files
    config = LocalAgentConfig(
        system_instructions=SYSTEM_PROMPT,
        capabilities=CapabilitiesConfig(), # Grants filesystem and command execution permissions
        api_key=api_key,
    )

    try:
        print("\n" + "="*60)
        print("🚀 Agent is ready! Type your circuit requirements below.")
        print("Example: 'Design a Buck Converter using the examples in Circuit Library'")
        print("Press Ctrl+C or type 'quit' to exit.")
        print("="*60 + "\n")
        
        # Start the interactive chat loop (handles spawning internally)
        await run_interactive_loop(config)
            
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Fix Windows console encoding for emoji characters if necessary
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
        
    asyncio.run(main())
