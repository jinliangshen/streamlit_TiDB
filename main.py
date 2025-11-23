import streamlit as st
from server.queryDB import InitConnectionDB
import numpy as np
import pandas as pd


# --- 2. 读取数据 (Read) ---
# ttl=5 表示数据缓存5秒，5秒后再次查询会重新去数据库拉取
@st.cache_data(ttl=5)
def query_vehicle_data(vin_filter=None, date_filter=None,Column:list=None):
    conn = InitConnectionDB()
    # 提交事务以刷新连接状态，确保读取到最新数据 (MySQL 默认的可重复读隔离级别会导致复用连接时看不到新数据)
    if conn:
        conn.commit()
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

def main()->None:
    dataColumn = dataColumn = ['DTC','Node','Velocity','Torque','Speed','Miles']
    dataQuery = st.button("showDBData",key = 'ShowData')
    # data = query_vehicle_data(Column=dataColumn)
    if dataQuery:
        data = query_vehicle_data(Column=dataColumn)
    else:
        lista = [None for ele in range(len(dataColumn))]
        data = pd.DataFrame(np.array(lista).reshape(-1,6),columns=dataColumn)
    
    st.dataframe(data)

    print("aaa")

if __name__ == "__main__":
    main()