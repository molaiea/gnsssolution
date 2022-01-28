import georinex as gr
from math import sin, atan, sqrt, cos
import numpy as np

def extract_params(file_name, sat_name, epoch):
    nav = gr.load(file_name)
    M0 = nav.sel(sv=sat_name)['M0'].values[epoch]
    e = nav.sel(sv=sat_name)['Eccentricity'].values[epoch]
    sqrtA = nav.sel(sv=sat_name)['sqrtA'].values[epoch]
    Omega0 = nav.sel(sv=sat_name)['Omega0'].values[epoch]
    Io = nav.sel(sv=sat_name)['Io'].values[epoch]
    omega = nav.sel(sv=sat_name)['omega'].values[epoch]
    DeltaN = nav.sel(sv=sat_name)['DeltaN'].values[epoch]
    cuc = nav.sel(sv=sat_name)['Cuc'].values[epoch]
    cus = nav.sel(sv=sat_name)['Cus'].values[epoch]
    crc = nav.sel(sv=sat_name)['Crc'].values[epoch]
    crs = nav.sel(sv=sat_name)['Crs'].values[epoch]
    cis = nav.sel(sv=sat_name)['Cis'].values[epoch]
    cic = nav.sel(sv=sat_name)['Cic'].values[epoch]
    OmegaDot = nav.sel(sv=sat_name)['OmegaDot'].values[epoch]
    IDOT = nav.sel(sv=sat_name)['IDOT'].values[epoch]
    toe = nav.sel(sv=sat_name)['Toe'].values[epoch]
    t_h = float(str(nav.sel(sv='G08').coords['time'][epoch].values).split('T')[1].split(':')[0])*3600
    t_min = float(str(nav.sel(sv='G08').coords['time'][epoch].values).split('T')[1].split(':')[1])*60
    t_s = float(str(nav.sel(sv='G08').coords['time'][epoch].values).split('T')[1].split(':')[2])
    t = t_h + t_min + t_s
    return M0, e, sqrtA, Omega0, Io, omega, DeltaN, cuc, cus, crc, crs, cis, cic, OmegaDot, IDOT, toe, t

def satellite_position(file_name, sat_name, epoch):
    #Extraction des paramètes
    #--------------------------------------------------
    M0, e, sqrtA, Omega0, Io, omega, DeltaN, cuc, cus, crc, crs, cis, cic, OmegaDot, IDOT, toe, t = extract_params(file_name, sat_name, epoch)
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
        E_k = M_k + e*sin(E0)
    
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
    dotproduct = np.dot(np.dot(R3lambda, R1ik), R3uk)
    vector = np.array(((r_k), (0), (0)))
    coords = np.dot(dotproduct, vector)
    return coords

# print(satellite_position("rabt3320.19n","G08",0))

def app_coords(X, Y, Z, D):
    # X Y Z D are respectively arrays of 4 coordinates and distances of the first 4 satellites, their purpose is to calculate the approximate coords 
    B=np.array([[X[0]-X[1],Y[0]-Y[1],Z[0]-Z[1]],[X[1]-X[2],Y[1]-Y[2],Z[1]-Z[2]],[X[2]-X[3],Y[2]-Y[3],Z[2]-Z[3]]])
    C=np.array([[D[1]**2-D[0]**2-(X[1]**2+Y[1]**2+Z[1]**2)+(X[0]**2+Y[0]**2+Z[0]**2)],[D[2]**2-D[1]**2-(X[2]**2+Y[2]**2+Z[2]**2)+(X[1]**2+Y[1]**2+Z[1]**2)],[D[3]**2-D[2]**2-(X[3]**2+Y[3]**2+Z[3]**2)+(X[2]**2+Y[2]**2+Z[2]**2)]])*0.5
    X0=np.dot(np.linalg.inv(B),C)
    return X0

# X0 = app_coords(X,Y,Z,D)

# Xa = np.array((221122,112233,221113,312342,661122,332233,991113,392342))
# Ya = np.array((621122,712233,621113,712342,721122,912233,821113,212342))
# Za = np.array((921122,812233,921113,912342,821122,512233,621113,412342))
# Da = np.array((21121122,11222233,22331113,31442342,28921122,15222233,22661113,31322342))
def jacobienne(X, Y, Z, D, X0):
    # X Y Z D are respectively arrays of all coordinates and distances of the all the satellites, X0 are the app coords of the station
    A=np.zeros((len(X), 3), dtype=float)
    W=np.zeros((len(X), 1), dtype=float)
    for i in range(len(D)):
        E=sqrt((X0[0][0]-X[i])**2+(X0[1][0]-Y[i])**2+(X0[2][0]-Z[i])**2)
        A[i][0]=(X0[0][0]-X[i])/E
        A[i][1]=(X0[1][0]-Y[i])/E
        A[i][2]=(X0[2][0]-Z[i])/E
        W[i][0]=E-D[i]
    return A, W
# A, W = jacobienne(Xa, Ya, Za, Da, X0)

def minimos_cuadrados(A, W, X0):
    N=np.dot(A.transpose(),A)
    U=np.dot(A.transpose(),W)
    X=np.dot(np.linalg.inv(N),U)
    Xcorr=X0-X
    return Xcorr


