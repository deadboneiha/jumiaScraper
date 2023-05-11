import requests
import json
import re
from bs4 import BeautifulSoup
from jinja2 import Template


def get_products(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    target_script = soup.find('script', text=lambda t:'window.__STORE__' in t)
    json_text = re.search(r'^\s*window\.__STORE__\s*=\s*({.*?})\s*;\s*$', 
                        target_script.string, flags=re.DOTALL | re.MULTILINE).group(1)
    # Parse the JSON
    data = json.loads(json_text)
    # list of products
    products = data["products"]
    return products

# telegram bot funnction to send notifications
def send_telegram_message(message: str, chat_id,  api_key: str):
    url = f"https://api.telegram.org/bot{api_key}/sendMessage?chat_id={chat_id}&text={message}"
    # Create json link with message
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML',
         }
    # POST the message
    requests.post(url, data)
       
BOT_TOKEN = "your bot token"
CHAT_ID = "your chat/group/channel id"
# telegram bot funnction to send notifications
def main():
    url = "https://www.jumia.co.ke/flash-sales/"
    products = get_products(url)

    for product in products:
        try:
            name = product["displayName"]
            brand = product["brand"]
            ksh_price = product["prices"]["price"]
            try:
                discount = product["prices"]["discount"]
            except:
                discount = "0"
            rating = product["rating"]["totalRatings"]
            image = product["image"]
            try:
                prod_url = product["url"]
            except:
                prod_url = "/"

            # Define an HTML template
            
            html_template = '''
<a href="{{image}}"> </a>
💥<strong>{{name}}</strong>💥

    ✅ <b>Brand:</b> {{brand}}   
    💲 <b>Price:</b> {{price}}  
    🏹 <b>Discount: </b>{{discount}}
    📊 <b>Rating: </b>{{rating}}

  <tg-emoji emoji-id="5368324170671202286">🛒 </tg-emoji> <a href="https://jumia.co.ke{{prod_url}}"><span class="tg-spoiler">GET IT</span></a>
            '''
            
            template = Template(html_template)
            # Render the template with the parsed JSON object
            
            html_output = template.render(
                name=name,
                rating=rating,
                brand=brand,
                price=ksh_price,
                discount=discount,
                prod_url=prod_url,
                image=image,
                )
                # send
            send_telegram_message(html_output, CHAT_ID, BOT_TOKEN)
        except:
            pass
        

if __name__ == "__main__":
    main()
