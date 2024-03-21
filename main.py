
# Business Search      URL -- 'https://api.yelp.com/v3/businesses/search'
# Business Match       URL -- 'https://api.yelp.com/v3/businesses/matches'
# Phone Search         URL -- 'https://api.yelp.com/v3/businesses/search/phone'

# Business Details     URL -- 'https://api.yelp.com/v3/businesses/{id}'
# Business Reviews     URL -- 'https://api.yelp.com/v3/businesses/{id}/reviews'

# Businesses, Total, Region

# Import the modules
import requests
import json
import pandas as pd
from pandas import json_normalize

# Define a business ID
# business_id = '4AErMBEoNzbk7Q8g45kKaQ'
business_id = '4AErMBEoNzbk7Q8g45kKaQ'
unix_time = 1546047836

# Define my API Key, My Endpoint, and My Header
API_KEY = ('U8fjDzj_dBkoH_bM_iY1fTjH92fsiKHoXjMctd-DmNrFupZlzQlPK9PHzQMScAjjGFmV1OxVdJE75fASMGXn_cLHTVi1CyZ3UA564pA5D92'
           'cSNMbphmaC32v6xK6ZXYx')
ENDPOINT = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(business_id)
# ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization': 'bearer %s' % API_KEY}

# Define my parameters of the search
# BUSINESS SEARCH PARAMETERS - EXAMPLE
# PARAMETERS = {'term': 'food',
#               'limit': 50,
#               'offset': 50,
#               'radius': 10000,
#               'location': 'San Diego'}

# BUSINESS MATCH PARAMETERS - EXAMPLE
# PARAMETERS = {'name': 'Peets Coffee & Tea',
#              'address1': '7845 Highland Village Pl',
#              'city': 'San Diego',
#              'state': 'CA',
#              'country': 'US'}

# BUSINESS REVIEWS PARAMETERS - EXAMPLE
PARAMETERS = {'limit': 50,
              'offset': 50}

# Make a request to the Yelp API
response = requests.get(url=ENDPOINT,
                        params=PARAMETERS,
                        headers=HEADERS)

# Convert the JSON String
business_data = response.json()

# print the response
print(json.dumps(business_data, indent=3))

df = pd.json_normalize(business_data['reviews'],
                     meta=['id', 'url', 'text', 'rating', 'time_created',
                           ['user', 'id'], ['user', 'profile_url'], ['user', 'image_url'], ['user', 'name']])

df.drop(columns=['url', 'time_created', 'user.profile_url', 'user.image_url', 'user.name'], inplace=True)

df.columns = ['review_id', 'text', 'stars', 'user_id']
df['business_id'] = business_id

print(df)


df.to_csv('yelp_reviews.csv', sep=';', index=False)