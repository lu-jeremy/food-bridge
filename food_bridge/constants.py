SEARCH_KEY = "AIzaSyD7auQlUaxYi4qxzVx802NA0WZaGKNCOgM"
SEARCH_ENGINE_ID = "e74e78cfd9c4c4ac6"  # Valid Google Custom Search Engine ID
DEV_ACCOUNT = 739287608118 
AUTHENTICATE_CMD = (
    f"ada credentials update --account={DEV_ACCOUNT} "
    "--provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --once"
)

MODEL_NAME = "us.anthropic.claude-sonnet-4-20250514-v1:0"

SYSTEM_PROMPT = """
You are a food bridge search agent that helps connect food banks with restaurants based on food needs and availability.

You MUST use the search tool for every query. When given:
- A specific restaurant name: Search for that restaurant's menu, donation policies, and contact info
- Food type and quantity (e.g. "100 sandwiches", "50 pizzas"): Search for restaurants that serve that food type and could potentially donate

For food type queries, search for:
1. Restaurants that serve the requested food type
2. Chain restaurants with multiple locations for bulk quantities
3. Local restaurants near food banks
4. Restaurant donation policies and contact information
5. Food safety requirements for donations
6. IMPORTANT: look for food banks nearby as well

Focus on:
- Matching food type to restaurant specialties
- Quantity feasibility for different restaurant sizes
- Nutritional value and shelf life
- Donation logistics and contact information
- Distance and accessibility for pickup
- Call multiple tools whenever possible

Always use the search tool to find relevant restaurants and information.
"""

TOOL_CONFIG = {
    "tools": [
        {
            "name": "search",
            "description": "Search for restaurants by food type or specific restaurant information",
            "input_schema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query for restaurant menu and ingredients"
                    }
                },
                "required": ["query"]
            }
        }
    ]
}