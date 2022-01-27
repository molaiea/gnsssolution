import georinex as gr
from math import sin, abs, atan, sqrt, cos
import numpy as np


def satellite_position(file_name, sat_name):
    #Extraction des paramètes
    #--------------------------------------------------
    nav = gr.load(file_name)
    M0 = nav.sel(sv=sat_name)['M0']
    e = nav.sel(sv=sat_name)['Eccentricity']
    sqrtA = nav.sel(sv=sat_name)['sqrtA']
    Omega0 = nav.sel(sv=sat_name)['Omega0']
    Io = nav.sel(sv=sat_name)['Io']
    omega = nav.sel(sv=sat_name)['omega']
    DeltaN = nav.sel(sv=sat_name)['DeltaN']
    cuc = nav.sel(sv=sat_name)['Cuc']
    cus = nav.sel(sv=sat_name)['Cus']
    crc = nav.sel(sv=sat_name)['Crc']
    crs = nav.sel(sv=sat_name)['Crs']
    cis = nav.sel(sv=sat_name)['Cis']
    cic = nav.sel(sv=sat_name)['Cic']
    OmegaDot = nav.sel(sv=sat_name)['OmegaDot']
    IDOT = nav.sel(sv=sat_name)['IDOT']
    toe = nav.sel(sv=sat_name)['Toe']
    t_h = int(str(nav.sel(sv='G08').coords['time'][0].values).split('T')[1].split(':')[0])*3600
    t_min = int(str(nav.sel(sv='G08').coords['time'][0].values).split('T')[1].split(':')[1])*60
    t_s = int(str(nav.sel(sv='G08').coords['time'][0].values).split('T')[1].split(':')[2])
    t = t_h + t_min + t_s
    #--------------------------------------------------
    #Calculs
    t_k = t-toe
    u = 1
    if t_k>302400 :
        t_k = t_k - 604800
    elif t_k<-302400 :
        t_k = t_k + 604800
    #Caclul de l'anomalie moyenne pour t_k
    M_k = M0 + ((u/sqrtA**3)+DeltaN)*t_k
    #Calcul de l'anomalie excentrique
    E0 = M_k
    E_k = E0 + e*sin(E0)
    while abs(E0-E_k)<0.000001 :
        E0 = E_k
        E_k = E0 + e*sin(E0)
    
    #Calcul de l'anomalie vraie
    v_k = atan((sqrt(1-e**2)*sin(E_k))/(cos(E_k)-e))
    #Calcul de l'arg de la latitude Uk
    u_k = omega + v_k + cuc*cos(2*(omega+v_k)) + cus*sin(2*(omega+v_k))
    #Calcul de la distance radiale rk
    r_k = (sqrtA**2)*(1-e*cos(E_k)) + crc*cos(2*(omega+v_k)) + crs*sin(2*(omega+v_k))
    #Calcul de l'inclinaison ik du plan orbital
    i_k = Io + IDOT*t_k + cic*cos(2*(omega+v_k)) + cis*sin(2*(omega+v_k))
    #Calcul de la longitude du noeud ascendant lambda_k
    lambda_k = Omega0 + (OmegaDot - omega)*t_k - omega*toe
    #Matrices de rotation
    R3lambda = np.array(((cos(-lambda_k), -sin(-lambda_k), 0), (sin(-lambda_k), cos(-lambda_k), 0), (0,0,1)))
    R3uk = np.array(((cos(-u_k), -sin(-u_k), 0), (sin(-u_k), cos(-u_k), 0), (0,0,1)))
    R1ik = np.array(((1,0,0), (0, cos(-i_k), -sin(-i_k)), (0, sin(-i_k), cos(-i_k))))
    #Calcul des coordonnées dans le référentiel CTS
    dotproduct = np.dot(np.dot(R3lambda, R1lambda), R3uk)
    vector = np.array(((r_k), (0), (0)))
    coords = np.dot(dotproduct, vector)
    return coords







