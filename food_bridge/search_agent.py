import boto3
import json
from .constants import SYSTEM_PROMPT, TOOL_CONFIG
from .google_search import GoogleSearcher


class SearchAgent:
    def __init__(self):
        self.bedrock_client = boto3.client(service_name="bedrock-runtime", region_name="us-west-2")
        self.google_searcher = GoogleSearcher()
        self.conversation_history = []
    
    def search_and_analyze(self, user_query: str) -> str:
        """Main method to search for restaurant info based on food needs or restaurant name"""
        # Determine if this is a food type query or restaurant name query
        food_keywords = ['sandwiches', 'pizza', 'burgers', 'salads', 'soup', 'bread', 'pastries', 'meals']
        quantity_keywords = ['100', '50', '200', 'bulk', 'large quantity']
        
        is_food_query = any(keyword in user_query.lower() for keyword in food_keywords + quantity_keywords)
        
        if is_food_query:
            initial_prompt = f"""
            I need to find restaurants that can provide: {user_query}
            
            Please search for restaurants that:
            - Serve this type of food
            - Could handle the requested quantity
            - Have food donation programs
            - Are accessible for food bank pickup
            
            Use the search tool to find relevant restaurants and their donation information.
            """
        else:
            initial_prompt = f"""
            I need information about: {user_query}
            
            Please search for relevant information about this restaurant including:
            - Official website and contact info
            - Food donation policies
            - Location and hours
            - Any food bank partnerships
            
            Use the search tool to gather this information.
            """
        
        return self._get_response_with_tools(initial_prompt)
    
    def _get_response_with_tools(self, prompt: str) -> str:
        """Get response from LLM with tool use capability"""
        messages = self.conversation_history + [{"role": "user", "content": prompt}]
        
        body = json.dumps({
            "max_tokens": 1000,
            "messages": messages,
            "system": SYSTEM_PROMPT,
            "anthropic_version": "bedrock-2023-05-31",
            "tools": TOOL_CONFIG["tools"]
        })

        model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        response = self.bedrock_client.invoke_model(body=body, modelId=model_id)
        
        body = json.loads(response["body"].read().decode("utf-8"))
        content_blocks = body["content"]
        
        text = ""
        tool_used = False
        
        for content_block in content_blocks:
            if content_block["type"] == "text":
                text += content_block["text"]
            elif content_block["type"] == "tool_use":
                tool_used = True
                print(f"Using tool: {content_block['name']}")
                tool_result = self._handle_tool_use(content_block)
                # Send tool result back to LLM for analysis
                analysis_prompt = f"""
                Based on this search information:
                
                {tool_result}
                
                Please analyze and summarize:
                1. Restaurants that match the food type/quantity requested
                2. Restaurant locations and contact information
                3. Food donation policies and procedures
                4. Feasibility for the requested quantity
                5. Pickup logistics and requirements
                """
                text += self._get_final_analysis(analysis_prompt)
        
        if not tool_used:
            print("No tool was used, forcing search...")
            # Force a search if no tool was used
            search_result = self._handle_tool_use({"name": "search", "input": {"query": prompt}})
            text += self._get_final_analysis(f"Based on this search: {search_result}")
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": prompt})
        self.conversation_history.append({"role": "assistant", "content": text})
        
        # Keep only last 10 messages to manage context window
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
        
        return text
    
    def _handle_tool_use(self, tool_use: dict) -> str:
        """Handle tool use requests"""
        if tool_use["name"] == "search":
            query = tool_use["input"]["query"]
            print(f"Searching for: {query}")
            urls = self.google_searcher.search(query)
            print(f"Found {len(urls)} URLs: {urls}")
            
            search_results = f"Search results for '{query}':\n\n"
            for url in urls[:5]:  # Limit to top 3 results
                print(f"Scraping: {url}")
                content = self.google_searcher.scrape_webpage(url)
                if content:
                    search_results += f"URL: {url}\nContent: {content}\n\n"
                else:
                    print(f"No content from {url}")
            
            print(f"Total search results length: {len(search_results)}")
            return search_results
        return ""
    
    def _get_final_analysis(self, prompt: str) -> str:
        """Get final analysis without tools"""
        body = json.dumps({
            "max_tokens": 800,
            "messages": [{"role": "user", "content": prompt}],
            "anthropic_version": "bedrock-2023-05-31"
        })

        model_id = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
        response = self.bedrock_client.invoke_model(body=body, modelId=model_id)
    
        body = json.loads(response["body"].read().decode("utf-8"))
        
        text = ""
        for content_block in body["content"]:
            if "text" in content_block:
                text += content_block["text"]

        return text