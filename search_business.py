# Import des bibliotheques
import requests
import json
import pandas as pd

# Parametres pour la recherche de restaurants
number_of_businesses = 50
location = "Paris"

# Parametres API Yelp
API_KEY = 'U8fjDzj_dBkoH_bM_iY1fTjH92fsiKHoXjMctd-DmNrFupZlzQlPK9PHzQMScAjjGFmV1OxVdJE75fASMGXn_cLHTVi1CyZ3UA564pA5D92cSNMbphmaC32v6xK6ZXYx'
ENDPOINT_BUSINESSES = f"https://api.yelp.com/v3/businesses/search?sort_by=best_match&limit={number_of_businesses}"
HEADERS = {'Authorization': 'bearer %s' % API_KEY}
PARAMETERS_BUSINESSES = {'location': location}

# RECOLTE DE RESTAURANTS SELON LES PARAMETRES INDIQUES
# Requete API
response = requests.get(url=ENDPOINT_BUSINESSES,
                        params=PARAMETERS_BUSINESSES,
                        headers=HEADERS)

# Conversion du JSON
businesses_data = response.json()

# print(json.dumps(businesses_data, indent=3))

# Mise en forme du dataframe de restaurants
df_businesses = pd.json_normalize(businesses_data['businesses'],
                       meta=['id', 'name', 'text', 'review_count', 'rating'])

df_businesses.rename(columns={'id': 'business_id'}, inplace=True)
df_businesses.drop(columns=['alias', 'image_url', 'is_closed', 'categories', 'transactions', 'phone', 'display_phone',
                 'coordinates.latitude', 'coordinates.longitude', 'location.address1', 'location.address2',
                 'location.address3', 'location.state', 'price', 'url', 'location.display_address', 'distance'], inplace=True)

# Sauvegarde des restaurants sous forme de CSV
df_businesses.to_csv('yelp_Paris_businesses.csv', sep=';', index=False)

# RECOLTE DES REVIEWS POUR LES RESTAURANTS PRECEDEMMENTS COLLECTES
list_businesses = df_businesses['business_id'].tolist()
df_reviews = pd.DataFrame()

PARAMETERS_BUSINESS = {'limit': 50,
                       'offset': 50}

# Boucle sur les ids de restaurants pour la recolte de reviews
for business in list_businesses:
    business_id = business
    ENDPOINT_REVIEWS = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(business_id)

    response = requests.get(url=ENDPOINT_REVIEWS,
                            params=PARAMETERS_BUSINESS,
                            headers=HEADERS)

    business_data = response.json()

    df_business = pd.json_normalize(business_data['reviews'],
                                    meta=['id', 'url', 'text', 'rating', 'time_created',
                                          ['user', 'id'], ['user', 'profile_url'], ['user', 'image_url'],
                                          ['user', 'name']])
    df_business.drop(columns=['url', 'time_created', 'user.profile_url', 'user.image_url', 'user.name'], inplace=True)
    df_business.columns = ['review_id', 'text', 'stars', 'user_id']
    df_business['business_id'] = business_id
    df_reviews = pd.concat([df_reviews, df_business])

# Sauvegarde des reviews sous forme de CSV
df_reviews.to_csv('yelp_reviews.csv', sep=';', index=False)

