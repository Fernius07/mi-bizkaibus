# Mi Bizkaibus 🚌

Aplicación web en tiempo real para visualizar la ubicación de los autobuses de Bizkaibus en un mapa interactivo, con información de paradas y horarios basados en datos GTFS.

## 🌟 Características

- **Mapa en tiempo real**: Visualiza la posición actual de todos los autobuses de Bizkaibus
- **Paradas interactivas**: Haz clic en cualquier parada para ver los próximos autobuses
- **Horarios GTFS**: Muestra los tiempos de llegada basados en el calendario oficial
- **Búsqueda**: Filtra autobuses por línea o número de vehículo
- **Actualización automática**: Los datos se refrescan cada 20 segundos

## 🚀 Uso

### Opción 1: Abrir directamente (datos pre-generados)

Si los datos GTFS ya están procesados en la carpeta `data/`:

1. Abre `index.html` en tu navegador
2. ¡Listo! El mapa se cargará automáticamente

### Opción 2: Procesar datos GTFS desde cero

Si necesitas actualizar los datos GTFS:

1. Coloca los archivos GTFS en la carpeta `gtfs/`
2. Ejecuta el script de procesamiento:
   ```bash
   python build_data.py
   ```
3. Abre `index.html` en tu navegador

## 📁 Estructura del Proyecto

```
Bizkaibus/
├── index.html          # Aplicación web principal
├── build_data.py       # Script para procesar datos GTFS
├── gtfs/              # Archivos GTFS originales
│   ├── stops.txt
│   ├── routes.txt
│   ├── trips.txt
│   ├── stop_times.txt
│   ├── calendar.txt
│   └── calendar_dates.txt
└── data/              # Datos procesados (generados por build_data.py)
    ├── stops.json
    ├── services.json
    └── stops/
        └── [stop_id].json
```

## 🔧 Tecnologías

- **Frontend**: HTML, CSS, JavaScript
- **Mapas**: Leaflet.js
- **Datos**: GTFS (General Transit Feed Specification)
- **API en tiempo real**: SIRI XML (Bizkaibus)
- **Procesamiento**: Python 3

## 📝 Notas

- Los datos de horarios se calculan automáticamente según el día actual
- La aplicación funciona completamente del lado del cliente (GitHub Pages compatible)
- Los datos GTFS deben actualizarse periódicamente ejecutando `build_data.py`

## 🌐 Despliegue en GitHub Pages

Este proyecto está listo para desplegarse en GitHub Pages:

1. Ve a Settings → Pages
2. Selecciona la rama `main` como fuente
3. La aplicación estará disponible en `https://[tu-usuario].github.io/mi-bzkaibus`

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

---

Desarrollado con ❤️ para la comunidad de Bizkaia
