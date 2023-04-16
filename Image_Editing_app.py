import streamlit as st
import psycopg2

# Connect to PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="myusername",
    password="mypassword"
)

# Execute SELECT query
cur = conn.cursor()
cur.execute("SELECT * FROM mytable")
rows = cur.fetchall()

# Display data in Streamlit
st.write("Data from mytable:")
for row in rows:
    st.write(row)

# Close database connection
cur.close()
conn.close()
