#!/usr/bin/env python
"""

algoritmo.py by Jorge Mauricio, 2016-02-15
This program calculate the Degrees Days of a database file.


"""

### Library
import math
import pandas as pd
import numpy as np

### Functions

#	Metodo residual

def metodoResidual(tmax, tmin, tbase):
	'''
	Genera los GDD por medio del Método Residual
	param: tmax: temperatura máxima
	param: tmin: temperatura mínima
	param: tbase: temperatura base del cultivo
	'''
	if (tmax > umbralSuperior):
		tmax = umbralSuperior
	else:
		tmax = tmax
	if (tmin < umbralInferior):
		tmin = umbralInferior
	else:
		tmin = tmin
	gdd = ((tmax + tmin) / 2.0) - tbase

	if (gdd < 0):
		gdd = 0.0
	return gdd

# 	Metodo triangulo simple
def metodoTrianguloSimple(tmax, tmin):
	'''
	Genera los GDD por medio del Método Triángulo Simple
	param: tmax: temperatura máxima
	param: tmin: temperatura mínima
	'''
	if (tmin > umbralSuperior and tmax > umbralSuperior):
		return umbralSuperior - umbralInferior
	elif (tmax < umbralInferior and tmin < umbralInferior):
		return 0.0
	elif (tmin >= umbralInferior and tmax <= umbralSuperior):
		return ((6 * (tmax + tmin - 2.0 * umbralInferior)) / 12)
	elif (tmin < umbralInferior and tmax > umbralSuperior):
		dti = tmax - umbralInferior
		dts = tmax - umbralSuperior
		dt = tmax - tmin
		return ((6 * pow(dti, 2.0) / dt) - ((6 * pow(dts, 2.0)) / dt)) / 12
	elif (tmin < umbralInferior and tmax > umbralInferior and tmax < umbralSuperior):
		dti = tmax - umbralInferior
		dt = tmax - tmin
		return ((6 * (pow(dti, 2.0)) / dt)) / 12
	elif (tmin > umbralInferior and tmin < umbralSuperior and tmax > umbralSuperior):
		dt = tmax - tmin
		dts = tmax - umbralSuperior
		return ((6 * (tmax + tmin - 2.0 * umbralInferior)) / 12) - (((6 * pow(dts, 2.0)) / dt) / 12)
	else:
		return 0.0

# 	Metodo seno simple

# 	Subrutina para metodo del seno simple
def sinec(suma, diff, temp1):
	'''
	Genera los GDD de acuerdo al comportamiento del ángulo
	param: suma:
	param: diff:
	param: temp1:
	'''
	twopi = 6.2834
	pihlf = 1.5708
	d2 = temp1 - suma
	d3 = diff * diff
	d4 = d2 * d2
	d5 = math.sqrt(d3 - d4)
	theta = math.atan2(d2, d5)
	if (d2 < 0 and theta > 0):
		theta = theta - 3.1416
	return (diff * math.cos(theta) - d2 * (pihlf - theta)) / twopi

def metodoSenoSimple(tmax, tmin):
	'''
	Genera los GDD por medio del Método Seno Simple
	param: tmax: temperatura máxima
	param: tmin: temperatura mínima
	'''
	gdd = 0.0
	if (tmin > umbralSuperior):
		return umbralSuperior - umbralInferior
	else:
		if (tmax <= umbralInferior):
			return 0.0
		else:
			temp1 = 2 * umbralInferior
			diff = tmax - tmin
			suma = tmax + tmin
			if (tmin >= umbralInferior):
				gdd = (suma - temp1) / 2
			else:
				gdd = sinec(suma, diff, temp1)
			if (tmax > umbralSuperior):
				temp1 = 2 * umbralSuperior
				gdd2 = gdd
				gdd = sinec(suma, diff, temp1)
				return gdd2 - gdd
	return gdd

#%% 	Leer archivo .csv
data = pd.read_csv('data/datos.csv')

#%% 	Desplegar el menú
print ("*************************************************************")
print ("*****      Programa para calcular grados-dias en Python *****")
print ("*****      Metodos:                                     *****")
print ("*****      + Residual                                   *****")
print ("*****      + Triangulo Simple                           *****")
print ("*****      + Metodo Seno Simple                         *****")
print ("*************************************************************")

# 	Preguntar al usuario los límites
umbralInferiorText = input("Introduce el umbral inferior: ")
umbralSuperiorText = input("Introduce el umbral superior: ")
tbaseText = input("Introduce la temperatura base: ")
umbralSuperior = float(umbralSuperiorText)
umbralInferior = float(umbralInferiorText)
tbase = int(tbaseText)

#%% variables

gddTS = 0.0
gddTD = 0.0
gddSS = 0.0

#%%	validacion de umbrales
if (umbralSuperior >= umbralInferior):
	data['GDDR'] = data.apply(lambda row: metodoResidual(row['tmax'], row['tmin'], tbase), axis=1)
	data['GDDTS'] = data.apply(lambda row: metodoTrianguloSimple(row['tmax'], row['tmin']), axis=1)
	data['GDDSS'] = data.apply(lambda row: metodoSenoSimple(row['tmax'], row['tmin']), axis=1)
	data.to_csv('data/datos_procesados.csv', sep=',')
else:
	print ("Error \nLimite inferior mayor al superior")	