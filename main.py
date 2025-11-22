import streamlit as st
from server.queryDB import query_vehicle_data
import numpy as np
import pandas as pd



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

if __name__ == "__main__":
    main()