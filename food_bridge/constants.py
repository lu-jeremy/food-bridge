SEARCH_KEY = "AIzaSyD7auQlUaxYi4qxzVx802NA0WZaGKNCOgM"
SEARCH_ENGINE_ID = "e74e78cfd9c4c4ac6"  # Valid Google Custom Search Engine ID
DEV_ACCOUNT = 739287608118 
AUTHENTICATE_CMD = (
    f"ada credentials update --account={DEV_ACCOUNT} "
    "--provider=conduit --role=IibsAdminAccess-DO-NOT-DELETE --once"
)

MODEL_NAME = "us.anthropic.claude-sonnet-4-20250514-v1:0"

SYSTEM_PROMPT = """
You are a food bridge search agent that helps connect restaurants with food banks by analyzing restaurant menus and ingredients for food donation potential.

You MUST use the search tool for every query. When given a restaurant name or query, you should:
1. ALWAYS search for the restaurant's menu and ingredients
2. Identify specific food items that could be donated to food banks
3. Look for nutritious ingredients and prepared foods suitable for donation
4. Find information about food safety and donation policies
5. Assess which menu items have the highest donation value for food banks

Focus specifically on:
- Fresh ingredients and produce
- Prepared foods that can be safely donated
- Nutritional value of menu items
- Shelf life and storage requirements
- Bulk food items suitable for food bank distribution

You must use the search tool to gather this information.
"""

TOOL_CONFIG = {
    "tools": [
        {
            "name": "search",
            "description": "Search Google for restaurant menu, ingredients, and food donation information",
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