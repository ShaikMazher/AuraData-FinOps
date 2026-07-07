import os
from google import genai
from google.genai import types
from mcp_server import query_financial_database

# 1. Initialize the Google GenAI Client
# (We will set the API key in the terminal in the next step)
client = genai.Client()

# 2. Define our Enterprise Agent's Persona & Guardrails
FINOPS_SYSTEM_INSTRUCTION = """
You are AuraData, an elite Enterprise FinOps AI Agent. 
Your job is to analyze corporate cloud infrastructure costs.
You have access to a secure financial database tool. 

Rules:
1. Always use the query_financial_database tool to fetch real data before answering.
2. If the data shows high costs, suggest specific infrastructure optimizations.
3. Be highly professional, concise, and format your output like an executive summary.
"""

def run_finops_analysis(user_prompt: str):
    print(f"\n[Manager]: Sending request to AuraData Agent...\n'{user_prompt}'\n")
    print("="*50)
    
    # 3. Create the Agent session with the Tool attached
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=FINOPS_SYSTEM_INSTRUCTION,
            tools=[query_financial_database], # Passing our MCP server tool!
            temperature=0.2, # Keep it highly analytical, less creative
        )
    )
    
    # 4. Print the Agent's Executive Report
    print("[AuraData FinOps Agent Output]:")
    return response.text
    print("="*50)

if __name__ == "__main__":
    # This is the test prompt we will use for the Kaggle Demo Video!
    demo_prompt = "Run a SELECT * query to get all our cloud costs. Which department is spending the most, and where can we cut costs?"
    
    try:
        run_finops_analysis(demo_prompt)
    except Exception as e:
        print(f"Agent Error: Make sure your GEMINI_API_KEY is set! Details: {e}")