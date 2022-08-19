#!/usr/bin/env python
# coding: utf-8

# In[1]:
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff

st.title("Welcome to the EDA Web-app")
try:
    uploaded_file = st.file_uploader("Choose a file",type=["csv"])
    df=pd.read_csv(uploaded_file)
    st.dataframe(df.head())  # printing head of the dataframe

    #data types of each feature
    if st.checkbox("Data_types"):
      st.dataframe(df.dtypes.astype(str)) #printing the data types



    #checking the no of null values
    if st.checkbox("Null values check"):
      st.write(df.isna().sum())  # checking null values

    #describing the dataset

    if st.checkbox("Describing the data"):
      st.write(df.describe())   # describing the dataset

    #identifying the numerical and categorical (object) columns
    columns=df.columns
    num_vars=df.select_dtypes(include=[np.number]) .columns  #numerical variables
    cat_vars=df.select_dtypes(include=[np.object]) .columns#categorical variables

    #selecting column to be viewed
    st.write("\n\n")
    cb_selcol=st.multiselect("Select the columns to be viewed:",list(df.columns)) 
    if cb_selcol is not None: #viewing multiple columns at a time
      st.write(df[cb_selcol])

    #for discrete numerical features
    num_cat=[]
    for i in list(num_vars):
      if (len(df[i].unique())<=15):  #numerical features with finite values
        num_cat.append(i) 


    num_cat=num_cat+list(cat_vars) #num_cat contains all the categorical (object) as well as discrete numerical features
    st.write("\n\n")
    #finding unique categories

    feas=[]
    if st.checkbox("Finding unique categories"):
      for i in num_cat:
         if (len(df[i].unique())>15):

           st.write(i,"Column is not shown because it has more than 15 unique categories")
           st.markdown("**-------------------------------------------------------------------------------------------------**")
           pass
         else:
           st.write("Unique categories in ",i,"column:",df[i].unique())
           st.write("\n","\n")
           st.write("Value counts for unique categories in ",i,"column:")
           st.write(df[i].value_counts())

           st.markdown("**-------------------------------------------------------------------------------------------------**")
    #some categorical(object) features like name, brand name .... can have a lot of unique values, here we take only 
    #the features with not more than 15 unique categories
    for i in num_cat:  
         if (len(df[i].unique())<=15): #feas contains all the features (both numeric and categorical) with not more than 
                feas.append(i)          #  15 unique categories        

    #to plot hist and bar graph we want everything except the categorical (object) features with more than 15 categories
    #we can get count for the finite categorical and numerical features.
    num_feas_cat=list(num_vars)+feas  #num_feas_cat is used for hist plots
    lim_num=[]
    for i in num_vars:   #numerical features with finite values (repeated as i tampered with the variable above)
        if (len(df[i].unique())<=15):
           lim_num.append(i)

    num_feas_cat_lim=feas+lim_num # for pie charts we can have only finite numerical and categorical values
    st.write("\n\n")
    #container 1

    viz1= st.expander("Click here for Histogram and heatmap Visualisations")
    cont1=viz1.container()
    cont1.write("Histogram plotting")
    selection1 = cont1.selectbox("",options =list(set(num_feas_cat)))
    hist = px.histogram(df, x=selection1)
    cont1.plotly_chart(hist)
    cont1.write("\n")

    cont1.write("Barchart plotting")
    selections = cont1.selectbox("barchart input",options =list(set(num_feas_cat)))
    none1=[None]
    colors1=cont1.selectbox("Select the feature for hue:",options=list(set(none1+feas)))
    try:
        bar=px.bar(df,x=selections,color=colors1)
        cont1.plotly_chart(bar)
    except KeyError:
        st.error("This column hue cannot be displayed because it contains NaN values")
   
    cont1.write("\n")
    
    cont1.write("Heat Map")
    hmap = px.imshow(df.corr())
    cont1.plotly_chart(hmap)
    
    st.write("\n")

    #container 2

    viz2= st.expander("Click here for Pie Chart, box and violin chart Visualisations")
    cont2=viz2.container()
     
    cont2.write("Pie chart plotting")
    selection2 = cont2.selectbox("",options =num_feas_cat_lim)
    pie = px.pie(df, names=selection2)
    cont2.plotly_chart(pie)
    cont2.write("\n")
    
    cont2.write("Box_Plot")
    selection_x=cont2.selectbox("Select x coordinate (categorical):",options=feas)
    selection_y=cont2.selectbox("Select y coordinate (numerical):",options=list(set(list(num_vars)).difference(feas)))
    box=px.box(df,x=selection_x,y=selection_y)   #list(set(list(num_vars)).difference(feas)) is used to get  
    #features with more than 15 unique categories in numerical y coordinate
    cont2.plotly_chart(box)
    

    cont2.write("\n")

    cont2.write("Violin_Plot")
    selection_x1=cont2.selectbox("Select x1 coordinate (categorical):",options=feas)
    selection_y1=cont2.selectbox("Select y1 coordinate (numerical):",options=list(set(list(num_vars)).difference(feas)))
    violin=px.violin(df,x=selection_x1,y=selection_y1,points="all")
    cont2.plotly_chart(violin)
    

    st.write("\n")


    #container 3
    # numeric vs numeric viz for scatterplots
    viz3= st.expander("Click here for Scatter Visualisations")
    cont3=viz3.container()
    cont3.write("Scatter plotting")
    selection_x2=cont3.selectbox("Select x2 coordinate (numerical):",options=list(set(list(num_vars)).difference(feas)))
    selection_y2=cont3.selectbox("Select y2 coordinate (numerical):",options=list(set(list(num_vars)).difference(feas)))
    none=[None]
    colors3=cont3.selectbox("Select the features for hue:",options=none+feas)

    try:
        scat=px.scatter(df,x=selection_x2,y=selection_y2,color=colors3)
        cont3.plotly_chart(scat)
    except KeyError:
        st.error("This column hue cannot be displayed because it contains NaN values")
    
    cont3.write("\n\n")
    cont3.write("\nScatter 3D plotting")   
    selection3d_x2=cont3.selectbox("Select 3d x2 coordinate (numerical):",options=list(set(list(num_vars)).difference(feas)))
    selection3d_y2=cont3.selectbox("Select 3d y2 coordinate (numerical):",options=list(set(list(num_vars)).difference(feas)))
    selection3d_z2=cont3.selectbox("Select 3d z2 coordinate (numerical):",options=list(set(list(num_vars)).difference(feas)))
    none=[None]
    colors3d=cont3.selectbox("Select the features for 3d hue:",options=none+feas)

    try:
        scat_3d=px.scatter_3d(df,x=selection3d_x2,y=selection3d_y2,z=selection3d_z2,color=colors3d)
        cont3.plotly_chart(scat_3d)
    except KeyError:
        st.error("This column hue cannot be displayed because it contains NaN values")
   
    st.write("\n")     
        
   #container 4
    viz4=st.expander("Click here for Probability and dist plots")
    cont4=viz4.container()
    cont4.write("ECDF")
    none1=[None]
    selection_x4 = cont4.selectbox("ecdf",options=list(set(list(num_vars)).difference(feas)))
    colors4=cont4.selectbox("Select the feature for hue (ecdf):",options=list(set(none1+feas)))
    ecdf=px.ecdf(df,x=selection_x4,color=colors4)
    cont4.plotly_chart(ecdf)
    cont4.write("\n")

    cont4.write("Distplot with hist")
    selection_x5 = cont4.selectbox("dist",options=list(set(list(num_vars)).difference(feas)))
    dist=ff.create_distplot([df[selection_x5].values.tolist()],["Distribution"])
    cont4.plotly_chart(dist)
    cont4.write("\n")

    cont4.write("Distplot without hist")
    selection_x6 = cont4.selectbox("dist_his",options=list(set(list(num_vars)).difference(feas)))
    dist2=ff.create_distplot([df[selection_x6].values.tolist()],["no_hist_dist"],show_hist=False) #refer distplot docs in plotly
    cont4.plotly_chart(dist2)
    cont4.write("\n")
    
except ValueError:
    st.warning("Upload the dataset")


# In[ ]:




