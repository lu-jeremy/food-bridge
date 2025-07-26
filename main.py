#!/usr/bin/env python3
import subprocess

from food_bridge import SearchAgent
from food_bridge.constants import AUTHENTICATE_CMD


def main():
    subprocess.run(AUTHENTICATE_CMD, check=True, shell=True)
    agent = SearchAgent()
    
    print("Food Bridge - Restaurant Search Agent")
    print("Enter restaurant names to search for food donation opportunities")
    print("Type 'quit' to exit\n")
    
    while True:
        restaurant_query = input("> ").strip()
        if restaurant_query.lower() in ['quit', 'exit', 'q']:
            break
        
        if not restaurant_query:
            continue
        
        print("-" * 50)
        
        try:
            result = agent.search_and_analyze(restaurant_query)
            print(result)
        except Exception as e:
            print(f"Error: {e}")
        
        print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    main()