import requests
import json
from bs4 import BeautifulSoup

def find_first_paragraph(html_code):
    # Create a BeautifulSoup object to parse the HTML code
    soup = BeautifulSoup(html_code, 'html.parser')

    # Find the first <p> tag
    first_p = soup.find('p')

    # Extract the text from the <p> tag
    if first_p:
        text = first_p.get_text().strip()
        return text
    else:
        return "notfind"
if __name__ == '__main__':
    with open('korokguides.txt', 'w') as f:

        for i in range(0,900):
            url = f'https://www.zeldadungeon.net/wiki/api.php?format=json&action=parse&page=Map%3ATears%20of%20the%20Kingdom%2FKorok{str(i).zfill(4)}'
            r = requests.get(url)
            if r.status_code == 200:
                print(i)
                data= json.loads(r.text)
                html= data['parse']['text']['*']
                line= find_first_paragraph(html)
                f.write( f'{{{i},{{\"{line}\",\'\'}}}},\n')
