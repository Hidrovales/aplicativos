#from Evapotranspiracao import Gera_Serie_Eto as gse
import streamlit as st
import numpy as np
import pandas as pd 
import math
import pmfao as gse


st.write("""
### Evapotranspiração de Referência

Este aplicativos calcula a $ET_o$ usando a Equação de PM FAO.
""")


st.sidebar.header('Entrada de parâmetros')

def imput():
    option = st.sidebar.selectbox('Escolha o método de estimativa:', ['PM FAO', 'HG', 'Thornthwaite'], format_func=lambda x: 'Select an option' if x == '' else x)
    if option == 'PM FAO':
        tmax = st.sidebar.text_input(label="Temperatura máxima", value= 30.0, key="na_lower")
        tmin = st.sidebar.text_input('Temperatura mínima', value= 15.0, key="na_lower")
        insol = st.sidebar.text_input('Insolação', value= 11.0, key="na_lower")
        tmean = (float(tmax) + float(tmin))/2
        ur = st.sidebar.text_input('Umidade Relativa', value= 60.0, key="na_lower")
        v = st.sidebar.text_input('Velocidade do vento', value= 2.0, key="na_lower")
        j = st.sidebar.text_input('Dia do ano', value= 1, key="na_lower")
        lat = st.sidebar.text_input('Latitude', value= -19.46, key="na_lower")
        alt = st.sidebar.text_input('Altitude', value= 732.00, key="na_lower")
        data = {
            'Tmax': float(tmax),
            'Tmin': float(tmin),
            'I': float(insol),
            'Tmedia': tmean,
            'UR': float(ur),
            'V': float(v),
            'Dia': int(j),
            'Latitude': float(lat),
            'Altitude': float(alt)
        }
    elif option == 'HG':
        tmax = st.sidebar.text_input(label="Temperatura máxima", value= 30.0, key="na_lower")
        tmin = st.sidebar.text_input('Temperatura mínima', value= 15.0, key="na_lower")
        lat = st.sidebar.text_input('Latitude', value= -19.46, key="na_lower")
        alt = st.sidebar.text_input('Altitude', value= 732.00, key="na_lower")
        data = {
            'Tmax': float(tmax),
            'Tmin': float(tmin),
            'Latitude': float(lat),
            'Altitude': float(alt)
        }
    else:
        tmax = st.sidebar.text_input(label="Temperatura máxima", value= 30.0, key="na_lower")
        tmin = st.sidebar.text_input('Temperatura mínima', value= 15.0, key="na_lower")
        lat = st.sidebar.text_input('Latitude', value= -19.46, key="na_lower")
        alt = st.sidebar.text_input('Altitude', value= 732.00, key="na_lower")
        data = {
            'Tmax': float(tmax),
            'Tmin': float(tmin),
            'Latitude': float(lat),
            'Altitude': float(alt)
        }
    features = pd.DataFrame(data, index = [0])
    return features

def eto_calc(dataset):
    latitude_graus = dataset.Latitude[0] #--em graus
    altitude = dataset.Altitude[0]  #--em metros

    latitude = math.pi/180 * latitude_graus #Converte a latitude de graus para radianos

    #: Solar constant [ MJ m-2 min-1]
    Gsc = 0.0820

    # Stefan Boltzmann constant [MJ K-4 m-2 dia-1]
    sigma = 0.000000004903

    es = gse.Es_medio(dataset.Tmin[0],dataset.Tmax[0]) #------------> Pressão do vapor de saturação
    ea = gse.Ea(dataset.Tmin[0],dataset.Tmax[0],dataset.UR[0]) #--------> Pressão do vapor atual
    delta = gse.Delta(dataset.Tmedia[0]) #----------------------> Declividade da curva de pressão do vapor
    pressao_atm = gse.Pressao_atm(altitude) #-----------> Pressão atmosférica
    gamma = gse.psicrometrica(pressao_atm) #------------> Constante
    declinacao_sol = gse.Declinacao_sol(dataset.Dia[0]) #----> Declinação solar
    omega = gse.Omega(latitude, declinacao_sol) #-------> Ângulo horário pôr-do-sol
    dr = gse.Dr(dataset.Dia[0]) #----------------------------> Inverso da distância relativa da terra-sol
    ra = gse.Ra(latitude, declinacao_sol, omega, dr, Gsc) #--> Radiação extraterrestre para períodos diários
    N = gse.N_insolacao(omega) #------------------------> Duração máxima de insolação no dia
    rs = gse.Rs(N, dataset.I[0], ra, dataset.Tmax[0], dataset.Tmin[0]) #---------------------> Radiação solar
    rso = gse.Rso(altitude, ra) #-----------------------> Radiação solar de céu claro
    rns = gse.Rns(rs, albedo=0.23) #--------------------> Radiação de onda curta líquida
    rnl = gse.Rnl(dataset.Tmin[0],dataset.Tmax[0], rs, rso, ea, sigma) #---> Radiação de onda longa líquida
    rn = gse.Rn(rns,rnl) #------------------------------> Radiação líquida
    serie_eto = gse.fao56_penman_monteith(rn, dataset.Tmedia[0], dataset.V[0], es, ea, delta, gamma, 0) #---> Evapotranspiração
    return serie_eto

df = imput()

eto = eto_calc(df)

st.subheader('Entrada de parâmetros')
st.write(df)

st.subheader('ETo')
st.write(eto)