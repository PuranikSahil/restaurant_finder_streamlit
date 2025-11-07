import overpy
import requests
import plotly.express as px
import pandas as pd
from sklearn.cluster import KMeans
import streamlit as st


    #### APP TITLE###
st.title("Restaurant Finder 🍜🍛")
st.write("Find the restaurants near you!")

    ## Get user location and just save it for the rest of the time ##
@st.cache_data(show_spinner="Getting your location...")
def get_user_location():
    try:
        ### this uses the IP address to get the users location.###
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        loc = data['loc'].split(',')
        return float(loc[0]), float(loc[1])
    except Exception as e:
        st.error(f"Couldn't fetch your location due to error: {e}")
        return 18.4874 , 73.8197

    ## Get the restaurants in the given city##
@st.cache_data(show_spinner="Hold on! Looking for restaurants in your city..")
def get_restos(city):
    ###  This will list out all the hotels in the {city} ###
    api = overpy.Overpass()
    try:
        query = f"""
        [out:json];
        area["name"="{city}"]->.searchArea;
        node["amenity"="restaurant"](area.searchArea);
        out;
        """
        result = api.query(query)
        data = []
        for node in result.nodes:
            tags = node.tags
            data.append({
                "name": tags.get("name"),
                "street": tags.get("addr:street"),
                "city": tags.get("addr:city", city),  # fallback to entered city
                "cuisine": tags.get("cuisine"),
                "opening_hours": tags.get("opening_hours"),
                "phone": tags.get("phone"),
                "latitude": node.lat,
                "longitude": node.lon
            })

        df = pd.DataFrame(data)
        df = df.dropna(subset=['name'])
        return df
    except Exception as e:
        st.error(f"Error to get restaurants from your area..")
        return pd.DataFrame()



        ### ADDING INPUTS ###

city = st.text_input("Enter your city:")
how_close = st.slider("How close do you want the restaurant to be (number of clusters):", 3, 100, 40)

        ### Main Logic ##

        #user location#
latitude , longitude = get_user_location()

# add button for searching
if st.button("Find restaurants near you! 🏪"):
    if not city:
        st.warning("Please enter a city name! ")
    else:
        df = get_restos(city)

        if df.empty:
            st.warning(f"Sorry, no restaurants found for {city} city")
        else:
            ## Running the KMeans##
            coords = df[['latitude', 'longitude']]
            Model = KMeans(n_clusters=how_close )
            Model.fit(coords)
            df['region'] = Model.predict(df[['latitude', 'longitude']])
            my_cluster = Model.predict([[latitude, longitude]])[0]
            ### Restos nearby: ##
            near_restos = df[df['region'] == my_cluster]

        ### Restaurants plotted on the map ###

            fig = px.scatter_map(
                near_restos,
                lat='latitude',
                lon='longitude',
                hover_name='name',
                #hover_data=['street', 'city', 'opening_hours','phone'],
                zoom=13,
                height=600
            )
        ###Add user's location###

            fig.add_trace(
                px.scatter_map(
                    pd.DataFrame({'latitude': [latitude], 'longitude': [longitude], 'User': ["You"]}),
                    lat='latitude',
                    lon='longitude',
                    hover_name='User'
                ).data[0].update(marker_color='red', marker_size=10, name='You are here')
            )


            fig.update_layout(mapbox_style='carto-positron')
            fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0})

            ### Display the map in Streamlit###
            st.plotly_chart(fig, use_container_width=True)



