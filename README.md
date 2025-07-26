# food-bridge
## To connect to RDS database
make sure you have foodbridge.pem downloaded
for each file, run this command: scp -i ~/.ssh/foodbridge.pem /path/file_name.py ec2-user@54.245.187.177:~/ (do this each time you edit a file)
then run: ssh -i ~/.ssh/foodbridge.pem ec2-user@54.245.187.177
in the ec2 terminal, run your code

# food-bridge

## Pitch
Food Bridge is an intelligent web application that connects food
banks with restaurants to optimize food distribution and reduce
waste. The platform leverages AI/LLM technology, geospatial 
analysis, and semantic search to create an efficient food 
sharing ecosystem.

## Project Overview
Food Bridge addresses a critical challenge in our food 
distribution system by leveraging artificial intelligence and 
geospatial technology to create meaningful connections between 
food providers and those in need.

The platform's strength lies in its intuitive approach to search
functionality. Rather than requiring users to navigate complex 
databases or rigid category systems, food banks can simply 
describe what they're looking for in natural language. When a 
coordinator types "we need fresh vegetables for our weekend 
distribution," the AI understands the context and intent, 
delivering relevant results that match their specific 
requirements.

What sets Food Bridge apart is its practical consideration of 
logistics. The system automatically prioritizes nearby 
restaurants and food providers, recognizing that proximity 
directly impacts the feasibility and cost-effectiveness of food 
recovery operations. This distance-based optimization ensures 
that food banks can make informed decisions about which 
donations are worth pursuing, ultimately maximizing their 
resources and impact.

The platform emerged from recognizing inefficiencies in current 
food redistribution methods. Many restaurants generate surplus 
food but lack streamlined channels to connect with food banks. 
Simultaneously, food assistance organizations often struggle to 
locate specific items needed for their programs, leading to time
-consuming searches and missed opportunities.

By combining semantic search capabilities with geographic 
intelligence, Food Bridge creates a more responsive and 
efficient ecosystem. The technology serves the practical needs 
of both food providers and recipients, facilitating connections 
that might otherwise never occur. This approach transforms food 
recovery from a cumbersome process into a streamlined operation 
that benefits communities while reducing waste.

The result is a platform that feels both sophisticated and 
accessible—one that harnesses advanced technology to solve real-
world problems in food security and sustainability.

## Key Features

### AI-Powered Search Agent
The platform includes an intelligent search agent that uses 
natural language processing to help food banks find relevant 
food donations that are in the vicinity.

### Database Architecture
The platform uses a PostgreSQL database.

## User Experience

### For Food Banks
1. Natural Language Search: "I need fresh produce for 50 
families"
2. AI-Powered Results: System returns semantically relevant food 
listings
3. Distance-Optimized: Results sorted by proximity for efficient 
pickup
4. Request Management: Track requests and coordinate with 
providers

### For Food Providers (Restaurants)
1. Easy Listing Creation: Add food items with descriptions and 
quantities
2. Request Management: View and manage incoming requests from 
food banks
3. Geographic Reach: Automatically connected with nearby food 
banks

## Tech Stack

### Backend
• **Python Flask**: Web framework
• **PostgreSQL**: database storage
• **Google Maps API**: Geocoding and distance calculations

### Frontend


### AI/ML Components

## Setup
setup virtual environment, then install all dependencies 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

database configuration: 

## Additional features we hope to further develop in the future

• **Multi-language Support**: Expand to support multiple 
languages
• **Dietary Restrictions**: AI understanding of dietary needs 
and restrictions
• **Demand Prediction**: ML models to predict food bank needs, depending on external context

### Enhanced Matching
• Real-time updates of food availability
• AI-driven automatic food bank-restaurant pairing
• Route optimization (such as multi-stop pickup route planning)

## Impact & Benefits

### For Food Banks
• **Reduced Search Time**: AI finds relevant food faster than 
manual browsing
• **Optimized Logistics**: Distance-based sorting minimizes 
transportation costs
• **Better Matching**: Semantic search finds food that meets 
specific needs

### For Restaurants
• **Simplified Donation Process**: Easy listing creation and 
management
• **Targeted Distribution**: Connect with food banks that need 
specific items
• **Waste Reduction**: Efficient redistribution of surplus food

### For Communities
• **Reduced Food Waste**: Intelligent matching prevents food 
from going to waste
• **Improved Food Security**: Better distribution reaches more 
people in need
• **Environmental Impact**: Reduced transportation through 
optimized routing

## Conclusion

Food Bridge represents a modern approach to food distribution, 
combining AI-powered search capabilities with geospatial 
optimization to create an efficient, user-friendly platform. The
integration of semantic search allows for natural language 
interaction, while the distance-based sorting ensures practical,
cost-effective food distribution. This technology-driven 
solution addresses real-world challenges in food security and 
waste reduction, making it easier for restaurants to donate 
surplus food and for food banks to find exactly what they need.
