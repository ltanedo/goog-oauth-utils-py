import googauth
from utils import sheets

googauth.rest.REDIRECT_URI = "http://localhost"
googauth.rest.CLIENT_ID    = "*********************************************.apps.googleusercontent.com"
googauth.rest.CLIENT_SECRET= "******-*******-********-_**********"


scopes = googauth.scopes.drive + googauth.scopes.sheets + googauth.scopes.bigquery
link = googauth.rest.get_link(scopes, credentials="lloydtan.json")
print(link)

url_result = 'http://localhost/?...............'
credentials = googauth.rest.init(url_result)
print(credentials)

refresh_token = '<REFRESH_TOKEN_FROM_CREDENTIALS_ABOVE>'
print( googauth.rest.refresh(refresh_token) )

