import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError 
my_fruit_list=pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index("Fruit")

streamlit.header('Breakfast Favorites')
streamlit.write('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.write('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.write('🐔 Hard-Boiled Free-Range Egg')
streamlit.write('🥑Avocado Toast')
streamlit.write('Dette er en test')
streamlit.write("Dette var gøy")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
sel=streamlit.multiselect("Pick som fruits:",list(my_fruit_list.index),["Avocado","Strawberries"])

selec=', '.join(sel)
#streamlit.text(type(sel))
if len(sel)>0:
  streamlit.dataframe(my_fruit_list.loc[sel])


def get_fruityvice_data(this_fruit_choice):
    fruityvice_response=requests.get("https://fruityvice.com/api/fruit/"+this_fruit_choice)
    #streamlit.text(fruityvice_response.json())
    fruityvice_normalized=pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  

streamlit.header("Fruityvice Fruit Advice")
try:
  fruit_choice=streamlit.text_input("What fruit would you like information about?")
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  #streamlit.write(f"The user entered:{fruit_choice}")
  else:
    streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
  streamlit.error()

#streamlit.stop()

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list") 
    return my_cur,my_cur.fetchall()


streamlit.subheader(f"The fruit load list contains")

if streamlit.button("Get Fruit Load List"):
  
  my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_cur,my_data_rows=get_fruit_load_list()
  column_names = [desc[0] for desc in my_cur.description]
  df=pd.DataFrame(my_data_rows,columns=column_names)
  streamlit.dataframe(df)
    
  


#my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur=my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_cur.execute("SELECT * FROM fruit_load_list")
#my_data_row=my_cur.fetchall()
#column_names = [desc[0] for desc in my_cur.description]
#df=pd.DataFrame(my_data_row,columns=column_names)

def insert_row_snowflake(new_fruit):
  try:
    my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur=my_cnx.cursor()
    my_cur.execute(f"insert into fruit_load_list values ('{new_fruit}')")
    return f"Thank you for adding {new_fruit}" 
  except Exception as e:
    return f"Error when writing to Snowflake: {e}"
  

#streamlit.stop()
#my_cnx=snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur=my_cnx.cursor()
fruit_choice2=streamlit.text_input("What fruit would you like to add:")
if streamlit.button("Add fruit"):
  status=insert_row_snowflake(fruit_choice2)
  streamlit.write(status)

#if isinstance(fruit_choice2, list):
#   streamlit.write(f"Thank you for selecting"+ " ,".join(fruit_choice2))
#else:
#  streamlit.write(f"Thank you for selecting {fruit_choice2}")
#my_cur.execute(f"insert into fruit_load_list values ('from streamlit')") 



 
   
                   
