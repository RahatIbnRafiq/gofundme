import requests
from bs4 import BeautifulSoup
import re
import time



def get_all_urls():
    import json
    file_path = 'dataset/analysis_campaign_ML_cleaned.json'
    with open(file_path, 'r') as file:
        data = json.load(file)
    urls = []
    for campaign in data:
        urls.append(campaign["URL"])
    return urls

def get_amount_raised():
    urls = get_all_urls()
    urls = urls[19860:]
    f = open("raised_amounts_4.txt", "w")
    for i in range(len(urls)):
        try:
            print(f"extracting for {i}-th url now")
            if (i+1)%1000 == 0:
                print("sleeping for 200 seconds now......")
                time.sleep(5)
            response = requests.get(urls[i])
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, 'html.parser')
            progress_meter_divs = soup.find_all('div', class_=re.compile(r'^progress-meter'))
            progress_texts = []
            for div in progress_meter_divs:
                div_text = div.get_text(strip=True)
                if div_text not in progress_texts:
                    progress_texts.append(div_text)
            if progress_texts:
                f.write(urls[i]+", "+', '.join(progress_texts)+"\n")
            else:
                print(urls[i], 'Amount raised not found.')
        except Exception as e:
            print(urls[i], e)
    f.close()
        

# # Example usage
# url = 'https://www.gofundme.com/f/zz9rr6-massage-studio'
# amount_raised = get_amount_raised(url)
# print(f'Amount Raised: {amount_raised}')
get_amount_raised()