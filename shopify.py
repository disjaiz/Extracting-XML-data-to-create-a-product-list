import xml.etree.ElementTree as ET
import requests

# Below url contains xml data of all the shopify skincare products----

url= 'https://skinny.buywithai.shop/sitemap_products_1.xml?from=8301017759977&to=8420664934633'
response= requests.get(url)

root = ET.fromstring(response.content)
namespace = {
        'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'image': 'http://www.google.com/schemas/sitemap-image/1.1'
    }

urls = root.findall('ns:url', namespaces=namespace)[1:4]  
info = []

for url in urls:
    dic = {
        'product_link':" ",
        'image_link': "" ,
        "image_title" : " ",
        'bullet_points': ''
        }
    loc = url.find('ns:loc', namespaces=namespace)
    dic['product_link'] = loc.text

    images = url.findall('image:image', namespaces=namespace)
    for image in images:
        image_loc = image.find('image:loc', namespaces=namespace)
        image_title = image.find('image:title', namespaces=namespace) 
        dic["image_link"] = image_loc.text
        dic['image_title'] = image_title.text

    info.append(dic)
    
# # ================================= extracting product content from its page ===============================================================

from bs4 import BeautifulSoup

website_content_list = []

for products in info:
    url = products['product_link']
    
    website_content = ''
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Print the title of the page
        website_content += ("Page Title:"+ str(soup.title.string))

        # Print all paragraphs
        for paragraph in soup.find_all('p'):
            website_content += str(paragraph.text)
    else:
        print(f"Failed to retrieve the webpage: {response.status_code}")
    website_content_list.append(website_content)

# ============================================Generating bullet points ===================================================================  

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def generate_bullet_points(text):
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer() 

        # Generate three sentences
        summary = summarizer(parser.document, 3)  # 3 bullet points

        # Format the summary into bullet points
        bullet_points = [f"- {str(sentence)}" for sentence in summary]

        return bullet_points

for i in range(0, len(website_content_list)):

    if __name__ == "__main__":
        text_input = website_content_list[i]

        bullet_points = generate_bullet_points(text_input)
    
        info[i]['bullet_points'] = bullet_points

print(info)
