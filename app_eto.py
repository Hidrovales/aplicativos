#from Evapotranspiracao import Gera_Serie_Eto as gse
import streamlit as st
import numpy as np
import pandas as pd 
import math
import pmfao as gse
from datetime import date


st.write("""
## Estimativa de Evapotranspiração de Referência

""")

def eto_calc(dataset, metodo):
    latitude_graus = dataset.Latitude[0] #--em graus
    altitude = dataset.Altitude[0]  #--em metros
    latitude = math.pi/180 * latitude_graus #Converte a latitude de graus para radianos
    #: Solar constant [ MJ m-2 min-1]
    Gsc = 0.0820
    # Stefan Boltzmann constant [MJ K-4 m-2 dia-1]
    sigma = 0.000000004903
    if metodo == 'pmfao':
        eto = gse.gera_serie(dataset,altitude,latitude,Gsc,sigma)
    elif metodo == 'hg':
        eto = 0
    elif metodo == 'pmfaodf':
        eto = 0
    
    return eto

def imput_FAO():
    st.write("""
    ### Método de estimativa PM FAO:

    Descrever aqui o método!
    """)
    tmax = st.sidebar.text_input(label="Temperatura máxima", value= 30.0, key="na_lower")
    tmin = st.sidebar.text_input('Temperatura mínima', value= 15.0, key="na_lower")
    insol = st.sidebar.text_input('Insolação', value= 11.0, key="na_lower")
    tmean = (float(tmax) + float(tmin))/2
    ur = st.sidebar.text_input('Umidade Relativa', value= 60.0, key="na_lower")
    v = st.sidebar.text_input('Velocidade do vento', value= 2.0, key="na_lower")
    j = st.sidebar.date_input ('Dia do ano', date.today())
    dia = gse.calcula_dia(j)
    lat = st.sidebar.text_input('Latitude', value= -19.46, key="na_lower")
    alt = st.sidebar.text_input('Altitude', value= 732.00, key="na_lower")
    data = {
        'Dia': dia,
        'Latitude': float(lat),
        'Altitude': float(alt),
        'Tmax': float(tmax),
        'Tmin': float(tmin),
        'I': float(insol),
        'Tmedia': tmean,
        'UR': float(ur),
        'V': float(v)
    }
    features = pd.DataFrame(data, index = [0])
    eto = eto_calc(features, 'pmfao')

    st.subheader('Parâmetros escolhidos:')
    st.write(features)

    st.subheader('ETo estimada:')
    st.write(eto)
    return eto

def imput_HG():
    st.write("""
    ### Método de estimativa HG:

    Descrever aqui o método!
    """)
    tmax = st.sidebar.text_input(label="Temperatura máxima", value= 30.0, key="na_lower")
    tmin = st.sidebar.text_input('Temperatura mínima', value= 15.0, key="na_lower")
    j = st.sidebar.date_input ('Dia do ano', date.today())
    dia = gse.calcula_dia(j)
    lat = st.sidebar.text_input('Latitude', value= -19.46, key="na_lower")
    alt = st.sidebar.text_input('Altitude', value= 732.00, key="na_lower")
    data = {
        'Dia': dia,
        'Latitude': float(lat),
        'Altitude': float(alt),
        'Tmax': float(tmax),
        'Tmin': float(tmin),
    }
    features = pd.DataFrame(data, index = [0])
    eto = eto_calc(features, 'hg')

    st.subheader('Parâmetros escolhidos:')
    st.write(features)
    st.subheader('ETo estimada:')
    st.write(eto)
    return eto

def imput_FAODF():
    st.write("""
    ### Método de estimativa PM FAO com dados faltantes:

    Descrever aqui o método!
    """)
    tmax = st.sidebar.text_input(label="Temperatura máxima", value= 30.0, key="na_lower")
    tmin = st.sidebar.text_input('Temperatura mínima', value= 15.0, key="na_lower")
    j = st.sidebar.date_input ('Dia do ano', date.today())
    dia = gse.calcula_dia(j)
    lat = st.sidebar.text_input('Latitude', value= -19.46, key="na_lower")
    alt = st.sidebar.text_input('Altitude', value= 732.00, key="na_lower")
    data = {
        'Dia': dia,
        'Latitude': float(lat),
        'Altitude': float(alt),
        'Tmax': float(tmax),
        'Tmin': float(tmin),
    }
    features = pd.DataFrame(data, index = [0])
    eto = eto_calc(features, 'pmfaodf')
    st.subheader('ETo estimada:')
    st.write(eto)
    return 0

def imput():
    st.sidebar.header('Entrada de parâmetros')
    option_1 = st.sidebar.selectbox('Escolha como deseja gerar o valor de ETo:', ['<Selecione>','Gerar valor único', 'Gerar série temporal de ETo'])
    if option_1 == 'Gerar série temporal de ETo':
        estacao = st.sidebar.selectbox('Escolha a estação:', ['<Selecione>','Salinas', 'Taiobeiras', 'Rio Pardo de Minas'])
    option_2 = st.sidebar.selectbox('Escolha o método de estimativa:', ['<Selecione>','PM FAO', 'HG', 'HGDF'])
    if option_2 == 'PM FAO':
        eto = imput_FAO()
    elif option_2 == 'HG':
        eto = imput_HG()
    elif option_2 == 'HGDF':
        eto = imput_FAODF()
    pass


imput()



