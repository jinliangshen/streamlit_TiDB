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

# --- 2. 读取数据 (Read) ---
# ttl=5 表示数据缓存5秒，5秒后再次查询会重新去数据库拉取
@st.cache_data(ttl=5)
def query_vehicle_data(vin_filter=None, date_filter=None,Column:list=None):
    conn = InitConnectionDB()
    cursor = conn.cursor()
    
    query = f"SELECT  dtc as {Column[0]}, node as {Column[1]}, voltage as {Column[2]}, soc as {Column[3]}, speed as {Column[4]}, miles as {Column[5]} FROM `Streamlit-Table`"
    params = []
    
    # 动态构建查询条件
    conditions = []
    if vin_filter:
        conditions.append("vin = %s")
        params.append(vin_filter)
    
    # 如果有过滤条件，拼接到 SQL 中
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY miles ASC LIMIT 100" # 只取最新的100条
    
    # 使用 pandas 直接读取 SQL，方便后续处理
    try:
        df = pd.read_sql(query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame() # 出错返回空表

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









