import streamlit
import pandas as pd
import requests

my_fruit_list=pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index("Fruit")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑Avocado Toast')
streamlit.text('Dette er en test')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
sel=streamlit.multiselect("Pick som fruits:",list(my_fruit_list.index),["Avocado","Strawberries"])

selec=', '.join(sel)
#streamlit.text(type(sel))
if len(sel)>0:
  streamlit.dataframe(my_fruit_list.loc[sel])

fruityvice_service=requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.text(fruityvice_service)

