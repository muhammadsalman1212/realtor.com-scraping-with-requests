
import requests
from bs4 import BeautifulSoup
import json
import csv

for i in range(95, 109):
    print(f"Scraping page {i}...")
    url = f'https://www.realtor.com/realestateagents/Indianapolis_IN/pg-{i}'
    print(url)

    # User-Agent header add karna
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:99.0) Gecko/20100101 Firefox/99.0",
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
                with open('3rd-withsold-agents_info.csv', 'a+', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)

                    # Writing headers to CSV file
                    writer.writerow(
                        ["count_of_recentsell", 'agent_address', 'city', 'description', 'name', 'photo_url', 'phone1', 'phone2', 'phone3'])

                    for agent in agents:
                        agent_address = agent.get('address', {}).get('line')
                        city = agent.get('address', {}).get('city')
                        description = agent.get('description')
                        phones = agent.get('phones')
                        name = agent.get('person_name')
                        photo = agent.get('photo')
                        photo_url = photo.get('href') if photo else None
                        count_of_recentsell = agent.get('recently_sold', {}).get('count')


                        # Store the agent information in a row
                        row = [count_of_recentsell, agent_address, city, description, name, photo_url]
                        if phones:
                            row.extend([phone.get('number') for phone in phones])
                        else:
                            row.extend([''] * 3)  # If phone numbers are not present, fill empty strings
                        writer.writerow(row)
                        print("Agent info stored in CSV:", row)

            else:
                print("No agents found.")
        else:
            print("Required script tag not found.")
    else:
        print(f'Failed to retrieve the')
