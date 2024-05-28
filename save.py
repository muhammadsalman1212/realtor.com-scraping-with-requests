import requests
from bs4 import BeautifulSoup
import json

url = 'https://www.realtor.com/realestateagents/Indianapolis_IN/pg-5'

# User-Agent header add karna
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/99.0.9999.99 Safari/537.36",
}

# Webpage content ko request karke get karna
response = requests.get(url, headers=headers)

# Agar request successful ho toh aage badhna
if response.status_code == 200:
    page_content = response.content

    # BeautifulSoup object mein content parse karna
    soup = BeautifulSoup(page_content, 'html.parser')

    # <script> tag ko find karna jisme id="__NEXT_DATA__" aur type="application/json" hai
    script_tag = soup.find('script', id='__NEXT_DATA__', type='application/json')

    # Script tag ka content extract karna
    if script_tag:
        json_data = json.loads(script_tag.string)

        # Required numbers ko extract karna
        agents = json_data.get('props', {}).get('pageProps', {}).get('pageData', {}).get('agents')

        # Checking if agents is not None
        if agents:
            for agent in agents:
                agent_address = agent.get('address', {}).get('line')
                city = agent.get('address', {}).get('city')
                if agent_address:
                    print("Agent Address:", agent_address)
                else:
                    print("Address not found for agent.")
                if city:
                    print("Agent city:", city)
                else:
                    print("city not found for agent.")
                description = agent.get('description')
                if description:
                    print("Description:", description)
                else:
                    print("Description not found.")
                phones = agent.get('phones')
                Phone_numbers_list = []
                if phones:
                    for phone in phones:
                        print("Phone:", phone.get('number'))
                        # store all nuber in a list
                        Phone_numbers_list.append(phone.get('number'))
                    print("Phone Numbers List:", Phone_numbers_list)
                else:
                    print("Phone not found.")
                # person name
                name = agent.get('person_name')
                if name:
                    print("Name:", name)
                else:
                    print("Name not found.")

                #photo
                photo = agent.get('photo')
                photo_url = photo.get('href')
                if photo_url:
                    print("Photo URL:", photo_url)
                else:
                    print("Photo not found.")
                # recent sell

                recent_sales = agent.get('recently_sold', {}).get('count')
                if recent_sales:
                    print("Recent Sales:", recent_sales)
                else:
                    print("Recent Sales not found.")







        else:
            print("No agents found.")
    else:
        print("Required script tag not found.")
else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
