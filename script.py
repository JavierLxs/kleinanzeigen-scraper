import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from redmail import EmailSender
from function import *

# ------------------------------------------------------------
# Section 1: Create list of URLs
# ------------------------------------------------------------

# Alfa Romeo GTV:
url_gtv = ("https://www.kleinanzeigen.de/s-autos/anzeige:angebote/preis:200:4000/gtv"
           "/k0c216+autos.ez_i:1974%2C1986+autos.marke_s:alfa_romeo+autos.power_i:130%2C")

# MG TF:
url_mg_tf = ("https://www.kleinanzeigen.de/s-autos/anzeige:angebote/preis:200:3000/mg-tf"
             "/k0c216+autos.material_innenausstattung_s:volleder")

# Saab 900:
url_900 = ("https://www.kleinanzeigen.de/s-autos/anzeige:angebote/preis:200:5000"
           "/c216+autos.anzahl_tueren_s:2_3+autos.ez_i:%2C1993+autos.marke_s:saab"
           "+autos.model_s:900+autos.power_i:140%2C+autos.shift_s:manuell")

# House in Mecklenburg Vorpommern:
url_haus = ("https://www.kleinanzeigen.de/s-haus-kaufen/bungalow,einfamilienhaus,villa"
            "/mecklenburg-vorpommern/anbieter:privat/anzeige:angebote/preis::50000"
            "/c208l61+haus_kaufen.grundstuecksflaeche_d:100%2C+haus_kaufen.haustyp_s:einfamilienhaus"
            "+haus_kaufen.qm_d:100%2C+haus_kaufen.zimmer_d:2%2C")

# List with all variables starting with "url_" (commented variables will not be added)
urls = [value for key, value in globals().items() if key.startswith('url_')]

# ------------------------------------------------------------
# Section 2: Extract data
# ------------------------------------------------------------

all_ads_heute = []

# Loop through URLs and extend the list with the ads from each URL
for url in urls:
    all_ads_heute.extend(kleinanzeigen_heute(url))

# ------------------------------------------------------------
# Section 3: Send e-mail with results
# ------------------------------------------------------------

# Configure your email server settings:
email = EmailSender(
    host='smtp.gmail.com',
    port=587,
    username='sender@gmail.com', #email address from which the message will be sent
    password='sender_mail_pwd', #16-character gmail app password for sender@gmail.com
                                #or equivalent for other email providers
    use_starttls=True
)

# Check if ads_heute list is not empty:
if all_ads_heute:

    # Transform list into string format:
    urls_html = "".join(f'<li><a href="{url}">{title}</a></li>' for title, url in all_ads_heute)

    # Specify the email details and send:
    email.send(
        subject="Kleinanzeigen Results",
        sender="sender@gmail.com",
        receivers=["receiver@gmail.com"], #email address to which the message will be sent
        html=f"<h1>The following ads have been found today:</h1><ul>{urls_html}</ul>"
    )

    print("Email sent successfully.")

else:
    print("No ads found for today, no email sent.")
