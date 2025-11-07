Restaurant Finder Web App.

This application is built with Streamlit.
It uses the IP address of the user to detect the location.
After detecting the location, depending on the input for the city field, the API is given a call for the resstaurants in that city.
Next, a KMeans model is fitted on the data collected using the API.
The model is used the predict in which cluster will the user's coordinates will belong to, and hence all the restaurants in that cluster are made visible.

As the number of clusters increase, the data points belonging in it will decrease, and so as the number of clusters increase, only the data points near to the user's data point will be shown.


Tech Used:
Streamlit
Pandas
Plotly
Scikit-learn
Overpy
Requests

How to run:
pip install -r requirements.txt
streamlit run make_app.py
