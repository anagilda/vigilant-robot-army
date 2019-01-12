import time

from bs4 import BeautifulSoup
from selenium import webdriver
from my_mail import send_email

# Download drivers from seleniumhq website
browser = webdriver.Chrome('./chromedriver')

# Allow less secure apps on sender's gmail settings
sender = 'email@gmail.com'
password = 'secretpassword'
receiver = 'email@email.com'
subject = 'Languages available'

# Example: Khan Academy language_picker 
url = 'https://www.khanacademy.org/'
select = 'language_picker'

prev = None

while True:
    try:
        browser.get(url)
        time.sleep(5) # Make sure the website loads completely (javascript included)
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')

        languages = soup.select('select[id='+ select +'] > option')

        if prev != languages:
            langsAvailable = 'Languages currently available:'
            for lang in languages[1:]:   # first option is usually disabled
                langsAvailable += '\n' + lang.text

            message = 'Hello! The language choice at our website has changed.\n\n' \
                + langsAvailable + '\n\nCreate an account: ' + url
            
            send_email(sender, password, receiver, subject, message)

            prev = languages

        time.sleep(300)
    
    except:
        print('Connection lost. Next try in 2 minutes.')
        time.sleep(120)

browser.quit()
