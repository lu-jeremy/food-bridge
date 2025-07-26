# food-bridge
## To connect to RDS database
make sure you have foodbridge.pem downloaded
for each file, run this command: scp -i ~/.ssh/foodbridge.pem /path/file_name.py ec2-user@54.245.187.177:~/ (do this each time you edit a file)
then run: ssh -i ~/.ssh/foodbridge.pem ec2-user@54.245.187.177
in the ec2 terminal, run your code

## Pitch
Food Bridge is an intelligent web application that connects food
banks with restaurants to optimize food distribution and reduce
waste. The platform leverages AI, geospatial 
analysis, and semantic search to create an efficient food 
sharing ecosystem.

## Project Overview
Food Bridge addresses a notable challenge in our food 
distribution system by leveraging artificial intelligence and 
geospatial technology to create meaningful connections between 
food providers and those in need.

The platform's strength lies in its intuitive approach to search
functionality. Rather than requiring users to navigate complex 
databases or rigid category systems, food banks can simply 
describe what they're looking for in natural language.  

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
that might otherwise never occur.  

## Key Features

### AI-Powered Search Agent
The platform includes an intelligent search agent that uses 
natural language processing to help food banks find relevant 
food donations that are in the vicinity.

### Database Architecture
The platform uses a PostgreSQL database.

## User Experience

### For Food Banks
Food banks benefit from an intuitive search experience that 
mirrors natural conversation, allowing coordinators to simply 
state their needs. The AI-
powered search engine processes these requests to deliver relevant 
food listings that match specific requirements. Results are 
automatically sorted by geographic proximity, enabling food 
banks to prioritize nearby donations for more efficient pickup 
routes and reduced transportation costs. The platform also 
provides comprehensive request management tools, allowing 
organizations to track their submissions and maintain clear 
communication channels with food providers throughout the 
coordination process.

### For Food Providers (such as restaurants, bakeries, cafes)
Food providers enjoy a streamlined listing process that allows 
them to quickly add available food items with detailed 
descriptions and quantities, makign it a stress free process. The platform's request 
management system provides restaurants with clear visibility 
into incoming requests from food banks, enabling them to review,
approve, and coordinate pickups efficiently. Through automatic 
geographic matching, restaurants are connected with 
nearby food banks within their service area, ensuring that 
surplus food reaches organizations that can realistically 
collect it while maximizing the impact of their donations within
the local community.

## Tech Stack

### Backend
python, PostgreSQL 

### Frontend
streamlit

### AI/ML Components

## Setup
setup virtual environment, then install all dependencies 
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

database configuration: 

## Additional features we hope to further develop in the future

Future development plans include expanding the platform's 
accessibility through multi-language support, enabling food 
banks and restaurants from diverse communities to participate 
more effectively in the food recovery network. The system will 
incorporate advanced AI capabilities to understand and match 
dietary restrictions and special nutritional requirements, 
ensuring that food donations align with the specific needs of 
different populations served by food banks. Additionally, 
machine learning models will be developed to predict food bank 
demand patterns based on external factors such as seasonal 
variations, community events, and socioeconomic indicators, 
allowing for more proactive food distribution planning and 
improved resource allocation across the network.

### Enhanced Matching
• Real-time updates of food availability
• AI-driven automatic food bank-restaurant pairing
• Route optimization (such as multi-stop pickup route planning)

## Impact & Benefits

For Food Banks: The platform significantly reduces the time 
coordinators spend searching for suitable donations by 
leveraging AI to quickly identify relevant food items, 
eliminating the need for manual browsing through extensive 
listings. Distance-based sorting optimizes logistics operations 
by prioritizing nearby food sources, directly reducing 
transportation costs and enabling more efficient resource 
allocation. The semantic search functionality ensures better 
matching between available donations and specific organizational
needs, helping food banks secure exactly the types of food 
required for their programs and communities.

For Restaurants: Food providers benefit from a simplified 
donation process that streamlines listing creation and ongoing 
management, removing traditional barriers to participation in 
food recovery initiatives. The platform enables targeted 
distribution by connecting restaurants with food banks that 
specifically need their available items, ensuring donations 
reach organizations where they will have maximum impact. This 
efficient redistribution system helps restaurants significantly 
reduce food waste by creating reliable pathways for surplus 
inventory to reach those in need rather than ending up in 
landfills.

For Communities: The intelligent matching system substantially 
reduces overall food waste by ensuring surplus food finds 
appropriate recipients before spoiling, creating a more 
sustainable local food ecosystem. Improved food security results
from better distribution networks that help nutritious meals 
reach more people in need throughout the community. The platform
's optimized routing capabilities generate positive 
environmental impact by minimizing unnecessary transportation, 
reducing carbon emissions while maximizing the efficiency of 
food recovery operations across the region.

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
