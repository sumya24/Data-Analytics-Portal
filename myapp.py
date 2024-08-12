# import libraries
import pandas as pd 
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title = "Analyatics Portal",
    page_icon = "📊"
)
#title
st.title(":rainbow[Data Analytics Portal]")
st.subheader(":gray[Explore Data In Easy Way...]",divider="rainbow")

file = st.file_uploader("Upload CSV or Excel File", type = ["csv","xlsx"])
if(file!=None):
    if(file.name.endswith("csv")):
        data = pd.read_csv(file)
    else:
        data = pd.read_excel(file)
    
    st. dataframe(data)
    st.info("File is Successfully Uploaded", icon="🚨" ) 

    st.subheader(":rainbow[Basic Information Of The Dataset]",divider = "rainbow")
    tab1, tab2, tab3, tab4 = st.tabs(["Summary","Top and Bottom Rows","Data Types","Columns"]) 

    with tab1:
        st.write(f"There Are {data.shape[0]} Rows in the Dataset and {data.shape[1]} Columns in the Dataset")
        st.subheader("Here Is Statistical Summary Of The Dataset")
        st.dataframe(data.describe())
    with tab2:
        st.subheader(":gray[Top Rows]")
        toprows = st.slider("Number Of Rows You Want",1,data.shape[0],key = "topslider")
        st.dataframe(data.head(toprows))
        st.subheader(":gray[Bottom Rows]")
        botttomrows = st.slider("Number Of Rows You Want",1,data.shape[0], key = "bottomslider")
        st.dataframe(data.tail(botttomrows))
    with tab3:
        st.subheader(":gray[Data Type Of Column]")
        st.dataframe(data.dtypes)
    with tab4:
        st.subheader("Column Name In Dataset")
        st.write(list(data.columns))
    
    st.subheader(":rainbow[Column Values TO Count]", divider="rainbow")
    with st.expander("Value Count"):
        col1, col2 = st.columns(2)
        with col1:
            column = st.selectbox("Choose Column Name", options=list(data.columns))
        with col2:    
            toprows = st.number_input("Top Rows",min_value=1,step=1)
        

        count = st.button("Count")
        if(count==True):
            result = data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader("Visualization", divider="rainbow")
            fig = px.bar(data_frame=result, x=column,y="count", text = "count", template = "plotly_white")
            st.plotly_chart(fig)
            fig = px.line(data_frame=result, x=column,y="count", text = "count", template = "plotly_white")
            st.plotly_chart(fig)
            fig = px.pie(data_frame=result, names=column, values="count")
            st.plotly_chart(fig)

    st.subheader(":rainbow[Groupby : Simplify Your Data Analysis In Easier Way]",divider="rainbow")
    st.write("The Groupby lets You Summmerize Data By Specific Categories And Gropups")
    with st.expander("Group By Your Columns"):
        col1, col2, col3 = st.columns(3)
        with col1:
            groupby_cols = st.multiselect("Choose Your Column To Gropuby", options = list(data.columns))
        with col2:
            operaction_col = st.selectbox("Choose Ypur Column For Operaction", options = list(data.columns))
        with col3:
            operaction = st.selectbox("Choose Your Operaction To Perform", options = ["sum","max","min","mean","median","count"])
        

        if(groupby_cols):
            result = data.groupby(groupby_cols).agg(new_col = (operaction_col,operaction)).reset_index()
            st.dataframe(result)

            st.subheader(":gray[Data Visualization]", divider="gray")
            graphs = st.selectbox("Choose Your Graph", options = ["line","bar","scatter","pie","sunburst"])
            if(graphs=="line"):
                x_axix = st.selectbox("Choose Your X axis", options=list(result.columns))
                y_axix = st.selectbox("Choose Y axis", options=list(result.columns))
                color = st.selectbox("Color Information", options=[None]+ list(result.columns))
                fig = px.line(data_frame=result,x=x_axix, y=y_axix , color=color, markers = "o")
                st.plotly_chart(fig)
            elif(graphs=="bar"):
                x_axix = st.selectbox("Choose Your X axis", options=list(result.columns))
                y_axix = st.selectbox("Choose Y axis", options=list(result.columns))
                color = st.selectbox("Color Information", options=[None]+ list(result.columns))
                facet_col = st.selectbox("Column Information", options=[None]+ list(result.columns))
                fig = px.bar(data_frame=result,x=x_axix, y=y_axix , color=color, facet_col = facet_col, barmode = "group")
                st.plotly_chart(fig)
            elif(graphs=="scatter"):
                x_axix = st.selectbox("Choose Your X axis", options=list(result.columns))
                y_axix = st.selectbox("Choose Y axis", options=list(result.columns))
                color = st.selectbox("Color Information", options=[None]+ list(result.columns))
                size = st.selectbox("Size Column", options=[None]+ list(result.columns))
                fig = px.scatter(data_frame=result,x=x_axix, y=y_axix , color=color, size = size)
                st.plotly_chart(fig)
            elif(graphs=="pie"):
                values = st.selectbox("Choose Numerical Values", options=list(result.columns))
                names = st.selectbox("Choose Lables", options=list(result.columns))
                fig = px.pie(data_frame = result, values = values, names = names)
                st.plotly_chart(fig)
            elif(graphs=="sunburst"):
                path = st.multiselect("Choose Your Path", options=list(result.columns))
                fig = px.sunburst(data_frame = result, path= path, values = "new_col")
                st.plotly_chart(fig)




    
