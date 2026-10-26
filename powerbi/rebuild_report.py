from build_powerbi import *
from build_powerbi import PROJECT_ROOT
import sys, ast, numpy as np
from sklearn.model_selection import train_test_split
from scipy.stats import ks_2samp, chi2_contingency

def cliente():
 repo='Cliente360-Predictive-Insight';r=Report(repo,'Cliente360','30.000 clientes del dataset del proyecto · LTV estimado · exportación sin nombres, teléfono ni correo')
 p=PROJECT_ROOT/'data/processed';df=pd.read_csv(p/'customers_with_clusters.csv');cols=['ciudad_residencia','edad','genero','grupo_edad','cluster_nombre','ingresos_mensuales','promedio_gasto_comida','ltv_anual','engagement_score','frecuencia_categoria','membresia_premium']
 r.table('Clientes',df[cols],metrics('Clientes',[('Clientes','COUNTROWS(Clientes)'),('Ingreso','AVERAGE(Clientes[ingresos_mensuales])'),('LTV','SUM(Clientes[ltv_anual])'),('Engagement','AVERAGE(Clientes[engagement_score])'),('Gasto','AVERAGE(Clientes[promedio_gasto_comida])')]))
 r.table('Restaurantes',pd.read_csv(p/'yelp_clean.csv').drop_duplicates('id')[['name','city','price','rating','review_count']],metrics('Restaurantes',[('Restaurantes','COUNTROWS(Restaurantes)'),('Rating','AVERAGE(Restaurantes[rating])'),('Reviews','SUM(Restaurantes[review_count])')]))
 r.table('Importancia',pd.read_csv(p/'feature_importance.csv'),metrics('Importancia',[('Importancia','MAX(Importancia[Importancia])')]))
 fil=[('Clientes','ciudad_residencia'),('Clientes','cluster_nombre'),('Clientes','grupo_edad')]
 for name,label,c1,m1,c2,m2 in [('resumen','01 · Resumen ejecutivo','ciudad_residencia','KPI_Clientes','cluster_nombre','KPI_LTV'),('perfil','02 · Perfil de clientes','grupo_edad','KPI_Clientes','genero','KPI_Gasto'),('segmentos','03 · Segmentación y valor','cluster_nombre','KPI_Engagement','frecuencia_categoria','KPI_LTV')]:
  r.page(name,label,fil);r.cards('Clientes',['KPI_Clientes','KPI_Ingreso','KPI_LTV','KPI_Engagement']);r.chart('Clientes',c1,m1,c1,30,270);r.chart('Clientes',c2,m2,c2,650,270);r.tablevisual('Clientes',[c1,c2,'KPI_Clientes','KPI_Gasto','KPI_LTV','KPI_Engagement'],'Detalle agregado · selecciona categorías para explorar',30,570,1220,260)
 r.page('restaurantes','04 · Restaurantes de Miami',[('Restaurantes','price')],note='Yelp cubre Miami únicamente. 200 restaurantes únicos; no comparar oferta con ciudades sin cobertura.')
 r.cards('Restaurantes',list(r.measures['Restaurantes']));r.chart('Restaurantes','price','KPI_Rating','Rating por nivel de precio',30,270);r.tablevisual('Restaurantes',list(r.tables['Restaurantes']),'Restaurantes únicos · cobertura local',650,270,600,550)
 r.page('modelo','05 · Variables del modelo',[('Importancia','En_KBest')],note='Importancias exportadas del proyecto; no son efecto causal ni precisión de predicción. Entrenamiento e inferencia permanecen en Python.')
 r.chart('Importancia','Feature','KPI_Importancia','Importancia de variables · Random Forest',30,160,1220,380);r.tablevisual('Importancia',list(r.tables['Importancia'].columns),'Ranking y selección KBest',30,570,1220,260)
 return r.finish('Este proyecto no contiene una app Streamlit. La estructura se basa en sus notebooks y tablas procesadas: resumen, perfil, segmentación, restaurantes únicos de Miami y variables del modelo. Se elimina la comparación oferta/demanda entre ciudades sin cobertura Yelp. Se omiten datos de contacto. No se inventan resultados de predicción ni precisión.')
if __name__=='__main__':
    print(cliente())
