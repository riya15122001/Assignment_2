import streamlit as st
from streamlit_option_menu import option_menu
import os
import json
import pandas as pd
import mysql.connector
import plotly.express as px
import requests



#Dataframe creation
mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database= "Phonepe_data"
            )
cursor = mydb.cursor()
#agg_insurance_df
cursor.execute("SELECT * FROM aggre_insurance_table")

table1= cursor.fetchall()

agg_insurance=pd.DataFrame(table1, columns=("States", "Years", "Quarter" , "Transaction_Type" , "Transaction_Count" , "Transaction_Amount"))

#aggre_transaction_df
cursor.execute("SELECT * FROM aggre_transaction_table")

table2= cursor.fetchall()

aggre_transaction=pd.DataFrame(table2, columns=("States", "Years", "Quarter" , "Transaction_Type" , "Transaction_Count" , "Transaction_Amount"))

#aggre_user_df
cursor.execute("SELECT * FROM aggre_user_table")

table3= cursor.fetchall()

agge_User=pd.DataFrame(table3, columns=("States", "Years", "Quarter" , "Brands" , "Transaction_Count" , "Percentage"))

#map_insurance_df
cursor.execute("SELECT * FROM map_insurance_table")

table4= cursor.fetchall()

map_insurance=pd.DataFrame(table4, columns=("States", "Years", "Quarter" , "District" , "Transaction_Count" , "Transaction_Amount"))

#map_transaction_df
cursor.execute("SELECT * FROM map_transaction_table")

table5= cursor.fetchall()

map_tran=pd.DataFrame(table5, columns=("States", "Years", "Quarter" , "District" , "Transaction_Count" , "Transaction_Amount"))

#map_users_df
cursor.execute("SELECT * FROM map_users_table")

table6= cursor.fetchall()

map_users=pd.DataFrame(table6, columns=("States", "Years", "Quarter" , "District" , "RegisteredUsers" , "AppOpens"))

#top_Insurance_df
cursor.execute("SELECT * FROM top_insurance_table")

table7= cursor.fetchall()

top_Insurance=pd.DataFrame(table7, columns=("States", "Years", "Quarter" , "Pincodes" , "Transaction_Count" , "Transaction_Amount"))

#top_Transaction_df
cursor.execute("SELECT * FROM top_transaction_table")

table8= cursor.fetchall()

top_Transaction=pd.DataFrame(table8, columns=("States", "Years", "Quarter" , "Pincodes" , "Transaction_Count" , "Transaction_Amount"))

#top_Users_df
cursor.execute("SELECT * FROM top_users_table")

table9= cursor.fetchall()

top_Users=pd.DataFrame(table9, columns=("States", "Years", "Quarter" , "Pincodes" , "RegisteredUsers"))

 
def Aggre_insurance_Y(df,year):
    aiy= df[df["Years"] == year]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum()
    aiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(aiyg, x="States", y= "Transaction_Amount",title= f"{year} TRANSACTION AMOUNT",
                           width=550, height= 650, color_discrete_sequence=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(aiyg, x="States", y= "Transaction_Count",title= f"{year} TRANSACTION COUNT",
                          width=550, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        

        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_Amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_Amount"].min(),aiyg["Transaction_Amount"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =550, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_Count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_Count"].min(),aiyg["Transaction_Count"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =550, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)

    return aiy


def Aggre_insurance_Y_Q(df,quarter):
    aiyq= df[df["Quarter"] == quarter]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(aiyqg, x= "States", y= "Transaction_Amount", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",width= 550, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(aiyqg, x= "States", y= "Transaction_Count", 
                            title= f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",width= 550, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_Amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_Amount"].min(),aiyqg["Transaction_Amount"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =550, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)
    with col2:

        fig_india_2= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_Count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_Count"].min(),aiyqg["Transaction_Count"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} TRANSACTION COUNT",
                                 fitbounds= "locations",width =550, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)
    
    return aiyq

def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= True)

    agttg= df_state.groupby("Transaction_Type")[["Transaction_Count", "Transaction_Amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_Count", y= "Transaction_Type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Aggrnyl, width= 550, 
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_Amount", y= "Transaction_Type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 550,
                        title= f"{state.upper()} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)
        
def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_Count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_Count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=950,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Transaction_Count", hover_data= "Percentage",
                      width=950,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_Count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_Count", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)

def map_insure_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("District")[["Transaction_Count","Transaction_Amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Transaction_Amount",
                              width=550, height=500, title= f"{state.upper()} DISTRICT TRANSACTION AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "District", y= "Transaction_Count",
                              width=550, height= 500, title= f"{state.upper()} DISTRICT TRANSACTION COUNT",
                              color_discrete_sequence= px.colors.sequential.Mint)
        
        st.plotly_chart(fig_map_bar_1)

def map_insure_plot_2(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("District")[["Transaction_Count","Transaction_Amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(miysg, names= "District", values= "Transaction_Amount",
                              width=550, height=500, title= f"{state.upper()} DISTRICT TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(miysg, names= "District", values= "Transaction_Count",
                              width=550, height= 500, title= f"{state.upper()} DISTRICT TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)

def map_user_plot_1(df, year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyg, x= "States", y= ["RegisteredUsers","AppOpens"], markers= True,
                                width=950,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["RegisteredUsers","AppOpens"], markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 950,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("District")[["RegisteredUsers", "AppOpens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "RegisteredUsers",y= "District",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "AppOpens", y= "District",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)

def top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "RegisteredUsers", barmode= "group", color= "Quarter",
                            width=950, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["RegisteredUsers"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quarter", y= "RegisteredUsers",barmode= "group",
                           width=950, height= 800,color= "RegisteredUsers",hover_data="Pincodes",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)

def ques1():
    brand= agge_User[["Brands","Transaction_Count"]]
    brand1= brand.groupby("Brands")["Transaction_Count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_Count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_Count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= aggre_transaction[["States", "Transaction_Amount"]]
    lt1= lt.groupby("States")["Transaction_Amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_Amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= map_tran[["District", "Transaction_Amount"]]
    htd1= htd.groupby("District")["Transaction_Amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_Amount", names= "District", title="TOP 10 DISTRICT OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= map_tran[["District", "Transaction_Amount"]]
    htd1= htd.groupby("District")["Transaction_Amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_Amount", names= "District", title="TOP 10 DISTRICT OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= map_users[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= map_users[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= aggre_transaction[["States", "Transaction_Count"]]
    stc1= stc.groupby("States")["Transaction_Count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_Count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= aggre_transaction[["States", "Transaction_Count"]]
    stc1= stc.groupby("States")["Transaction_Count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_Count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)


def ques9():
    ht= aggre_transaction[["States", "Transaction_Amount"]]
    ht1= ht.groupby("States")["Transaction_Amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_Amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)
def ques10():
    dt= map_tran[["District", "Transaction_Amount"]]
    dt1= dt.groupby("District")["Transaction_Amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "District", y= "Transaction_Amount", title= "DISTRICT WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)

#Streamlit part

st.set_page_config(layout= "wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")
st.write("")

with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts"])


if select == "Home":

    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("C:\\Users\\Priyadharshini Mohan\\Downloads\\Phonepe.mp4")
        

    col3,col4= st.columns(2)
    
    with col3:
        st.video("C:\\Users\\Priyadharshini Mohan\\Downloads\\video.mp4")
        

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.video("C:\\Users\\Priyadharshini Mohan\\Downloads\\upi.mp4")


if select == "Data Exploration":
    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("**Select the Analysis Method**",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("**Select the Year**", agg_insurance["Years"].min(), agg_insurance["Years"].max(),agg_insurance["Years"].min())

            df_agg_insur_Y= Aggre_insurance_Y(agg_insurance,years)
            
            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("**Select the Quarter**", df_agg_insur_Y["Quarter"].min(), df_agg_insur_Y["Quarter"].max(),df_agg_insur_Y["Quarter"].min())

            Aggre_insurance_Y_Q(df_agg_insur_Y, quarters)

            
        elif method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_at= st.slider("**Select the Year**", aggre_transaction["Years"].min(), aggre_transaction["Years"].max(),aggre_transaction["Years"].min())

            df_agg_tran_Y= Aggre_insurance_Y(aggre_transaction,years_at)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at= st.slider("**Select the Quarter**", df_agg_tran_Y["Quarter"].min(), df_agg_tran_Y["Quarter"].max(),df_agg_tran_Y["Quarter"].min())

            df_agg_tran_Y_Q= Aggre_insurance_Y_Q(df_agg_tran_Y, quarters_at)
            
            #Select the State for Analyse the Transaction type
            state_Y_Q= st.selectbox("**Select the State**",df_agg_tran_Y_Q["States"].unique())

            Aggre_Transaction_type(df_agg_tran_Y_Q,state_Y_Q)


        elif method == "User Analysis":
            year_au= st.selectbox("Select the Year_AU",agge_User["Years"].unique())
            agg_user_Y= Aggre_user_plot_1(agge_User,year_au)

            quarter_au= st.selectbox("Select the Quarter_AU",agg_user_Y["Quarter"].unique())
            agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State_AU**",agg_user_Y["States"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)

    with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

        if method_map == "Map Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m1= st.slider("**Select the Year_mi**", map_insurance["Years"].min(), map_insurance["Years"].max(),map_insurance["Years"].min())

            df_map_insur_Y= Aggre_insurance_Y(map_insurance,years_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m1= st.selectbox("Select the State_mi", df_map_insur_Y["States"].unique())

            map_insure_plot_1(df_map_insur_Y,state_m1)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m1= st.slider("**Select the Quarter_mi**", df_map_insur_Y["Quarter"].min(), df_map_insur_Y["Quarter"].max(),df_map_insur_Y["Quarter"].min())

            df_map_insur_Y_Q= Aggre_insurance_Y_Q(df_map_insur_Y, quarters_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m2= st.selectbox("Select the State_miy", df_map_insur_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_insur_Y_Q, state_m2)

        elif method_map == "Map Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m2= st.slider("**Select the Year_mi**", map_tran["Years"].min(), map_tran["Years"].max(),map_tran["Years"].min())

            df_map_tran_Y= Aggre_insurance_Y(map_tran, years_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m3= st.selectbox("Select the State_mi", df_map_tran_Y["States"].unique())

            map_insure_plot_1(df_map_tran_Y,state_m3)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m2= st.slider("**Select the Quarter_mi**", df_map_tran_Y["Quarter"].min(), df_map_tran_Y["Quarter"].max(),df_map_tran_Y["Quarter"].min())

            df_map_tran_Y_Q= Aggre_insurance_Y_Q(df_map_tran_Y, quarters_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m4= st.selectbox("Select the State_miy", df_map_tran_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_tran_Y_Q, state_m4)

        elif method_map == "Map User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("**Select the Year_mu**",map_users["Years"].unique())
            map_user_Y= map_user_plot_1(map_users, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu1= st.selectbox("**Select the Quarter_mu**",map_user_Y["Quarter"].unique())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarter_mu1)

            col1,col2= st.columns(2)
            with col1:
                state_mu1= st.selectbox("**Select the State_mu**",map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, state_mu1)

    with tab3:
        method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_top == "Top Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.slider("**Select the Year_ti**", top_Insurance["Years"].min(), top_Insurance["Years"].max(),top_Insurance["Years"].min())
 
            df_top_insur_Y= Aggre_insurance_Y(top_Insurance,years_t1)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t1= st.slider("**Select the Quarter_ti**", df_top_insur_Y["Quarter"].min(), df_top_insur_Y["Quarter"].max(),df_top_insur_Y["Quarter"].min())

            df_top_insur_Y_Q= Aggre_insurance_Y_Q(df_top_insur_Y, quarters_t1)

        
        elif method_top == "Top Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t2= st.slider("**Select the Year_tt**", top_Transaction["Years"].min(), top_Transaction["Years"].max(), top_Transaction["Years"].min())
 
            df_top_tran_Y= Aggre_insurance_Y(top_Transaction,years_t2)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t2= st.slider("**Select the Quarter_tt**", df_top_tran_Y["Quarter"].min(), df_top_tran_Y["Quarter"].max(),df_top_tran_Y["Quarter"].min())

            df_top_tran_Y_Q= Aggre_insurance_Y_Q(df_top_tran_Y, quarters_t2)

        elif method_top == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t3= st.selectbox("**Select the Year_tu**", top_Users["Years"].unique())

            df_top_user_Y= top_user_plot_1(top_Users,years_t3)

            col1,col2= st.columns(2)
            with col1:
                state_t3= st.selectbox("**Select the State_tu**", df_top_user_Y["States"].unique())

            df_top_user_Y_S= top_user_plot_2(df_top_user_Y,state_t3)


if select == "Top Charts":

    ques= st.selectbox("**Select the Question**",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                  'District With Highest Transaction Amount','Top 10 District With Lowest Transaction Amount',
                                  'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                 'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                 'Top 50 District With Lowest Transaction Amount'))
    
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="District With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 District With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 District With Lowest Transaction Amount":
        ques10()
# def Transaction_Amount_Count_Y(df, year):
    
    
#     tacy=df[df["Years"]== year]
#     tacy.reset_index(drop = True,inplace= True)

#     tacyg=tacy.groupby("States")[["Transaction_Count", "Transaction_Amount"]].sum()
#     tacyg.reset_index(inplace= True)
    
#     col1,col2=st.columns(2)
#     with col1:  

#         fig_amount= px.bar(tacyg, x="States", y="Transaction_Amount", title=f"{year} TRANSACTION AMOUNT",
#                         color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width=600)
#         st.plotly_chart(fig_amount)
#     with col2: 
#         fig_count= px.bar(tacyg, x="States", y="Transaction_Count", title=f"{year} TRANSACTION COUNT",
#                         color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650,width=600)
#         st.plotly_chart(fig_count)
    
    
# #streamlit Part

# st.set_page_config(layout="wide")
# st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

# with st.sidebar:
#     select= option_menu("Main Menu",["HOME", "DATA EXPLORATION", "TOP CHARTS"])

# if select=="HOME":
#     pass
# elif select=="DATA EXPLORATION":    
    
#     tab1,tab2,tab3=st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])
    
#     with tab1:
        
#         method = st.radio("Select The Method",["Insurance Analysis","Transaction Analysis", "User Analysis"])
        
#         if method == "Insurance Analysis":
            
#             col1,col2=st.columns(2)
#             with col1:
                
#              years=st.slider("Select The Year", agg_insurance["Years"].min(),agg_insurance["Years"].max(),agg_insurance["Years"].min())
#             Transaction_Amount_Count_Y(agg_insurance, years)
            
            
#         elif method =="Transaction Analysis":
#             pass
#         elif method =="User Analysis":
#             pass
#     with tab2:
        
#         method_2 = st.radio("Select The Method",["Map Insurance Analysis","Map Transaction Analysis", "Map User Analysis"])
        
#         if method_2 == "Map Insurance Analysis":
#             pass
#         elif method_2 =="Map Transaction Analysis":
#             pass
#         elif method_2 =="Map User Analysis":
#             pass   
#     with tab3:
        
#         method_3 = st.radio("Select The Method",["Top Insurance Analysis","Top Transaction Analysis", "Top User Analysis"])
        
#         if method_3 == "Top Insurance Analysis":
#             pass
#         elif method_3 =="Top Transaction Analysis":
#             pass
#         elif method_3 =="Top User Analysis":
#             pass  
# elif select =="TOP CHARTS":
#     pass           
        
    
