import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# import pandas as pd
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# Add pick list for users to pick the items
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table
streamlit.dataframe(fruits_to_show)


# New section to display fruitvice api response

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
      fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)      
      fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
      streamlit.dataframe(fruityvice_normalized)
 except URLError as e:
      streamlit.error()
# import requests

streamlit.text(fruityvice_response.json())



# don't run anything past this line as it is broken!
streamlit.stop()
# import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
# my_data_row = my_cur.fetchone()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
# streamlit.text("Hello from Snowflake:")
streamlit.dataframe(my_data_rows)
# Fruit to add
streamlit.header("What Fruit would you like to add?")
fruit_entered = streamlit.text_input('What fruit would you like information about?')
streamlit.write('Thanks for adding ', fruit_entered)

# This will not work correctly but just go with it for now
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
