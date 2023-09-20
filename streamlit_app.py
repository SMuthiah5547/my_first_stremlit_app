import streamlit as st
import pandas as pd
import requests as rq
import snowflake.connector
from urllib.error import URLError

st.title ("My Mom's New Healthy Diner")
st.header("Breakfast Menu")
st.text("🥣 Omega 3 & Blueberry Oatmeal")
st.text("🥗 Kale, Spinach & Rocket Smoothie")
st.text("🐔 Hard Boiled free-range Egg")
st.text("🥑🍞 Avocado Toast")
st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

st.dataframe(fruits_to_show)

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

st.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select the fruit to get information.")
  else:
    back_from_response = get_fruityvice_data(fruit_choice)
    #fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    st.dataframe(back_from_response)
except URLError as e:
  st.error()


st.header("The Fruit list contains:")
# snowflake related function
def get_fruit_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
    return my_cur.fetchall()

# Add button to load fruit list
if st.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_list()
  my_cnx.close()
  st.dataframe(my_data_rows)

# Allow the end user to add fruit to the list
def insert_row_sf(new_fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('" + new_fruit +"')")
    return "Thanks for adding: " + new_fruit

# Add button to add fruit to fruit list table
add_my_fruit = st.text_input('What fruit you would like to add:','')
if st.button('Add a Fruit to the list'):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  back_from_function = insert_row_sf(add_my_fruit)
  st.text(back_from_function)
  my_cnx.close()
  
st.stop()

# st.write('The user entered ', fruit_choice)
# fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# st.text(fruityvice_response.json())
# write your own comment - what does the next line do? - json_normalize() converts the nested dictionaries into separate columns for each key. 
# By default, the nested parts have column names in the format <parent key>.
# fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# write your own comment - Output the json output as table
# st.dataframe(fruityvice_normalized)

#my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
#my_cur = my_cnx.cursor()

#my_cur.execute("select * from pc_rivery_db.public.fruit_load_list")
#my_data_rows = my_cur.fetchall()
#st.header("The Fruit list contains:")
#st.dataframe(my_data_rows)


#add_my_fruit = st.text_input('What fruit you would like to add:','')
#st.write('Thanks for adding ', add_my_fruit)
#my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from Streamlit')")
