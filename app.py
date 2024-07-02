import pandas as pd
import plotly.express as px
import streamlit as st


#car_data = pd.read_csv("C:/Users/braya/Documents/mio/notas cursos/tripleten/proyecto/Proyecto_sprint_6/vehicles_us.csv")
car_data = pd.read_csv('vehicles_us.csv') 
car_data['date_posted'] = pd.to_datetime(car_data['date_posted'],format="%Y-%m-%d")
car_data['model_year'] = car_data['model_year'].fillna(1000)
car_data['model_year'] = car_data['model_year'].astype(int)
car_data['odometer'] = car_data['odometer'].fillna(111111).astype(int)
car_data['cylinders'] = car_data['cylinders'].fillna(0).astype(int)
car_data['is_4wd'] = car_data['is_4wd'].fillna(0).astype(int)
car_data['post_year'] = car_data['date_posted'].dt.year
car_data['post_month'] = car_data['date_posted'].dt.month

#filtros
post_2018 = car_data[car_data['post_year']==2018]['post_month'].value_counts().reset_index(name='month_count').sort_values(by='post_month')
post_2019 = car_data[car_data['post_year']==2019]['post_month'].value_counts().reset_index(name='month_count').sort_values(by='post_month')


st.set_page_config(layout='wide')
st.title('Exploración de datos sobre anuncios de coches', )
col1,col2 = st.columns(2)

with col1 :
    
    hist_button = st.button('Construir histograma')
        
    if hist_button: 
        st.write('Creación de un histograma del precio de los vehiculos') 
        fig = px.histogram(car_data, x="price")
        st.plotly_chart(fig, use_container_width=True)
    
    dispersion_button = st.button('Construir Gráfico de dispersión')

    if dispersion_button:
        st.write('Gráfico de dispersión precio en relación con el odómetro(kilometraje)')
        #fig = px.scatter(car_data, x='model_year', y='price' )
        fig = px.scatter(car_data, x='odometer',y='price',color='type')
        st.plotly_chart(fig,use_container_width=True)
    
    barras_button = st.button('Construir grafico de barras')   
    if barras_button:
        st.write('Gráfico de barras del tipo de vehiculo y su condición')
        filter2 = car_data.groupby(['type','condition'])['condition'].count().reset_index(name='condition_count')
        fig = px.bar(filter2, x='condition_count', y='type', color='condition')
        st.plotly_chart(fig, use_container_width=True)
        
        
        
with col2:    
         
    build_histogram = st.checkbox('crear grafico de barras')

    if build_histogram: # al hacer clic en el botón
        st.write('Vehiculos posteados el 2018 ')
        fig = px.bar(post_2018, x="post_month",y='month_count',labels={"post_month":"meses",
                                                                       "month_count":"cantidad"})
        st.plotly_chart(fig, use_container_width=True)
        
       
        st.write('Vehiculos posteados el 2019')
        fig2 = px.bar(post_2019, x="post_month",y='month_count',labels={"post_month":"meses",
                                                                       "month_count":"cantidad"},color_discrete_sequence=['#FF5733']) 
        fig2.update_layout(
            xaxis=dict(
                tickmode='array',
                tickvals=[1,2,3,4],
                ticktext=[1,2,3,4]
            )
        )
        st.plotly_chart(fig2, use_container_width=True)


    build_bar = st.checkbox('crear barras') 
    if build_bar:
        st.write('Gráfico circular precio por tipo de vehiculo')
       
        fig = px.pie(car_data, values='price', names='type')
        st.plotly_chart(fig, use_container_width=True)
    