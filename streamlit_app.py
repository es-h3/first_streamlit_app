import streamlit
import pandas as pd
import requests
import snowflake.connector
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
streamlit.header("Fruityvice Fruit Advice")
fruit_choice=streamlit.text_input("What fruit would you like information about?","orange")
streamlit.text(f"The user entered:{fruit_choice}")
fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruityvice_response.json())
fruityvice_normalized=pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur=my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_row=my_cur.fetchall()
column_names = [desc[0] for desc in my_cur.description]
df=pd.DataFrame(my_data_row,columns=column_names)
streamlit.subheader(f"The fruit load list contains:{type(my_data_row)}")
streamlit.dataframe(df)
fruit_choice2=streamlit.text_input("What fruit would you like to add:")
if isinstance(fruit_choice2, list):
     streamlit.text(", ".join(fruit_choice2)) 
else:
  streamlit.text=fruit_choice2
   
                   
