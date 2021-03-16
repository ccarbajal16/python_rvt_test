# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 20:20:03 2021

@author: carlos carbajal

referencia: https://rvt-py.readthedocs.io/en/latest/index.html
"""

import rvt.vis  # para generar las visualizaciones
import rvt.default  # para abrir y guardar nuestro ráster
import numpy as np

dem_path = r'raster/hh_cut_final.tif' # Definiendo la ruta de nuestro DEM
dict_dem = rvt.default.get_raster_arr(dem_path) # Genera un diccionario a partir del DEM
dem_arr = dict_dem["array"]  # nuestra matriz numpy del DEM
dem_resolution = dict_dem["resolution"]
dem_res_x = dem_resolution[0]  # resolución en la dirección X (0.5 para el ejemplo)
dem_res_y = dem_resolution[1]  # resolución en la dirección Y (0.5 para el ejemplo)
dem_no_data = dict_dem["no_data"] # definiendo los valores considerados "NoData"

# Generando el diccionario para generar las visualizacions de pendiente y aspecto
dict_slope_aspect = rvt.vis.slope_aspect(dem=dem_arr, resolution_x=dem_res_x,resolution_y=dem_res_y,
                                         output_units="degree", ve_factor=1, no_data=dem_no_data,
                                         fill_no_data=False, keep_original_no_data=False)

slope_arr = dict_slope_aspect['slope']
aspect_arr = dict_slope_aspect['aspect']

# Guardando la visualización de la pendiente
slope_path = r"outputs/hh_test_pendiente.tif"
rvt.default.save_raster(src_raster_path=dem_path, out_raster_path=slope_path, 
                        out_raster_arr=slope_arr, no_data=np.nan, e_type=6)

# Guardando la visualización del aspecto
aspect_path = r"outputs/hh_test_aspecto.tif"
rvt.default.save_raster(src_raster_path=dem_path, out_raster_path=aspect_path, 
                        out_raster_arr=aspect_arr, no_data=np.nan, e_type=6)

# Generar una visualización 'Hillshade'
sun_azimuth = 65 # ángulo del azimut solar (en el sentido de las agujas del reloj desde el norte) en grados 
sun_elevation = 45 # ángulo vertical solar (sobre el horizonte local del observador) en grados.
hillshade_arr = rvt.vis.hillshade(dem=dem_arr, resolution_x=dem_res_x, resolution_y=dem_res_y,
                                  sun_azimuth=sun_azimuth, sun_elevation=sun_elevation, ve_factor=1,
                                  no_data=dem_no_data, fill_no_data=False, keep_original_no_data=False)

# Para guardar nuestro mapa de sombras usamos:
hillshade_path = r"outputs/hh_test_sombreado.tif" # ruta de salida de nuestro resultado
rvt.default.save_raster(src_raster_path=dem_path, out_raster_path=hillshade_path, 
                        out_raster_arr=hillshade_arr, no_data=np.nan, e_type=6)

# Generar una visualización de sombreado multidireccional
nr_directions = 10  # número de direcciones que corresponde al número de ángulos de azimut solar (número de bandas). 
sun_elevation = 45  # ángulo vertical solar (sobre el horizonte) en grados.
multi_hillshade_arr = rvt.vis.multi_hillshade(dem=dem_arr, resolution_x=dem_res_x, resolution_y=dem_res_y, 
                                              nr_directions=nr_directions, sun_elevation=sun_elevation, ve_factor=1, 
                                              no_data=dem_no_data, fill_no_data=False, keep_original_no_data=False)

# Guardando la visualización del sombreado multidireccional
multi_hillshade_path = r"outputs/hh_test_sombreado_multidireccional.tif" # ruta de nuestro resultado
rvt.default.save_raster(src_raster_path=dem_path, out_raster_path=multi_hillshade_path, 
                        out_raster_arr=multi_hillshade_arr, no_data=np.nan, e_type=6)

# Generar una visualización de modelo de relieve local simple 
radius_cell = 15 # radio a considerar en píxeles (no en metros)
slrm_arr = rvt.vis.slrm(dem=dem_arr, radius_cell=radius_cell, ve_factor=1, 
                        no_data=dem_no_data, fill_no_data=False, keep_original_no_data=False)

# Guardando el modelo de relieve local simple
local_relief_path = r"outputs/hh_test_relieve_local.tif"
rvt.default.save_raster(src_raster_path=dem_path, out_raster_path=local_relief_path, 
                        out_raster_arr=slrm_arr, no_data=np.nan, e_type=6)

# Generar una visualización de Modelo de Relieve Multi-Escala
feature_min = 1 # Tamaño mínimo de la característica o razgo que desea detectar en metros.
feature_max = 5 # Tamaño máximo de la característica o razgo que desea detectar en metros.
scaling_factor = 3 # Factor de escala
msrm_arr = rvt.vis.msrm(dem=dem_arr, resolution=dem_res_x, feature_min=feature_min, 
                        feature_max=feature_max, scaling_factor=scaling_factor, ve_factor=1, 
                        no_data=dem_no_data, fill_no_data=False, keep_original_no_data=False)

# Guardando el modelo de relieve multi-scala
msrm_path = r"outputs/hh_test_relieve_multiescala.tif"
rvt.default.save_raster(src_raster_path=dem_path, out_raster_path=msrm_path, 
                        out_raster_arr=msrm_arr, no_data=np.nan, e_type=6)

# Parámetros del factor de vista del cielo (svf) que también se aplica para svf anisotrópico (asvf) y apertura (opns)
svf_n_dir = 16  # número de direcciones
svf_r_max = 10  # radio de búsqueda máximo en píxeles
# nivel de eliminación de ruido (0-no eliminar, 1-bajo, 2-medio, 3-alto)
svf_noise = 0
# Parámetros del svf anisotrópico
asvf_level = 1  # nivel de anisotropía (1-bajo, 2-alto)
asvf_dir = 315  # dirección de anisotropía en grados

# Genera un diccionario con claves 'svf', 'asvf' y 'opns'
dict_svf = rvt.vis.sky_view_factor(dem=dem_arr, resolution=dem_res_x, compute_svf=True,
                                   compute_asvf=True, compute_opns=True, svf_n_dir=svf_n_dir,
                                   svf_r_max=svf_r_max, svf_noise=svf_noise, asvf_level=asvf_level, asvf_dir=asvf_dir, no_data=dem_no_data, fill_no_data=False,
                                   keep_original_no_data=False)

svf_arr = dict_svf["svf"]  # factor de vista del cielo
asvf_arr = dict_svf["asvf"]  # factor de vista del cielo anisotrópico
opns_arr = dict_svf["opns"]  # apertura positiva

# Guarda los resultados para svf, asvf y opns
svf_path = r"outputs/hh_test_svf.tif"
rvt.default.save_raster(src_raster_path=dem_path, out_raster_path=svf_path,
                        out_raster_arr=svf_arr, no_data=np.nan, e_type=6)

asvf_path = r"outputs/hh_test_asvf.tif"
rvt.default.save_raster(src_raster_path=dem_path, out_raster_path=asvf_path,
                        out_raster_arr=asvf_arr, no_data=np.nan, e_type=6)

opns_path = r"outputs/hh_test_pos_opns.tif"
rvt.default.save_raster(src_raster_path=dem_path, out_raster_path=opns_path,
                        out_raster_arr=opns_arr, no_data=np.nan, e_type=6)

# Para la Apertura Negativa (neg-opns)
dem_arr_neg_opns = dem_arr * -1  # nuestro dem * -1
# No necesitamos calcular svf y asvf (compute_svf = False, compute_asvf = False)
dict_svf2 = rvt.vis.sky_view_factor(dem=dem_arr_neg_opns, resolution=dem_res_x,
                                    compute_svf=False, compute_asvf=False,
                                    compute_opns=True, svf_n_dir=svf_n_dir,
                                    svf_r_max=svf_r_max, svf_noise=svf_noise,
                                    no_data=dem_no_data, fill_no_data=False,
                                    keep_original_no_data=False)
neg_opns_arr = dict_svf2["opns"]

# Guarda los resultados
neg_opns_path = r"outputs/hh_test_neg_opns.tif"
rvt.default.save_raster(src_raster_path=dem_path, out_raster_path=neg_opns_path,
                        out_raster_arr=neg_opns_arr, no_data=np.nan, e_type=6)
