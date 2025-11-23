import mysql.connector
import pandas as pd
import streamlit as st

# --- 1. 数据库连接 (使用 cache_resource 保证连接池复用) ---
@st.cache_resource
def InitConnectionDB():
    try:
        return mysql.connector.connect(**st.secrets["mysql"])
    except Exception as e:
        st.error(f"⚠️ DB Connection Failed: {e}")
        return None



# --- 3. 写入数据 (Write) ---
def insert_vehicle_log(id, dtc, node, voltgae, soc, speed, miles):
    conn = InitConnectionDB()
    cursor = conn.cursor()
    query = """
        INSERT INTO `Streamlit-Table` 
        (id, dtc, node, voltage, soc, speed, miles)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (id, dtc, node, voltgae, soc, speed, miles))
        conn.commit() # 提交事务
        st.toast("✅ Data uploaded successfully!", icon='🎉')
        # 清除读取缓存，以便立即看到新数据
        query_vehicle_data.clear()
    except Exception as e:
        st.error(f"Write Failed: {e}")









