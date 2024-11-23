import requests
from bs4 import BeautifulSoup
import time
from telegram import Bot

# Telegram instellingen
TELEGRAM_API_TOKEN = '7826115707:AAFZSMaITChD_KJifuhvepcVuBub5kUrmxs'
CHAT_ID = '1940095586'

# URL van de Pararius-huurwoningenpagina voor Zwolle
URL = "https://www.pararius.nl/huurwoningen/zwolle"

# Functie om de website te scrapen
def get_new_listings():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # De woningen bevinden zich in een div met de class 'listing-search-item'
    listings = soup.find_all('a', class_='listing-search-item__link listing-search-item__link--title')


    # Maak een lijst van de woningtitels en links
    new_listings = []
    for listing in listings:
        title = listing.get_text(strip=True)  # No need to check for None here
        link = "https://www.pararius.nl" + listing.get('href')  # Access href attribute directly
        new_listings.append(f"{title}: {link}")
     
    
    return new_listings



# Functie om een Telegram-bericht te sturen
def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_API_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

# Functie om nieuwe woningen te controleren en berichten te sturen
def check_for_new_listings():
    previous_listings = []

    while True:
        print("Checking for new listings...")
        
        # Verkrijg de huidige lijst van woningen
        current_listings = get_new_listings()
        
        # Vergelijk met de vorige lijst
        new_entries = set(current_listings) - set(previous_listings)


        if new_entries:
            for new_entry in new_entries:
                send_telegram_message(f"Nieuwe woning gevonden: {new_entry}")
        
        # Update de vorige lijst
        previous_listings = current_listings

        # Wacht 10 minuten voordat je opnieuw controleert
        time.sleep(30)  # 600 seconden = 10 minuten

if __name__ == "__main__":
    check_for_new_listings()
