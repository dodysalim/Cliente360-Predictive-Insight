# Cliente360 · Power BI

Exportación agregada del CSV procesado del proyecto. LTV es una estimación del modelo, no ingresos realizados.

Datos: 20 filas en la exportación. El CSV omite nombres, teléfonos y correos.

Abra `Analytics.pbip` en Power BI Desktop y cambie el parámetro `DataFolder` a la ruta absoluta de `powerbi/data/` (con separador final). Luego actualice los datos. Alternativamente ejecute `python configure_data.py` para configurar la ruta.

Incluye modelo TMDL, Power Query, medidas DAX explícitas, tarjetas y tabla de detalle. Los archivos JSON y las referencias se verificaron por código; apertura, actualización y renderizado en Power BI Desktop pendientes. No se afirma equivalencia funcional completa con la aplicación Python.

La exportación se reconstruye con `build_powerbi.py` durante la preparación del portafolio. La fuente original permanece en este repositorio.
