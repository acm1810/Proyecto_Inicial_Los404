# Valparaíso Oculto - Proyecto Inicial IWG400 (USM)
Página web desarrollada para el curso de Proyecto Inicial (Universidad Técnica Federico Santa María), cuyo objetivo es reunir en un solo lugar información sobre atractivos turísticos secundarios, comercio local y alojamientos de la Región de Valparaíso, promoviendo una distribución equitativa del turismo.

Carrera: Ingeniería Civil Informática  
Paralelo 11 | Grupo 07 "Los 404"

# Descripción
Este proyecto busca visibilizar y redistribuir el turismo en la Región de Valparaíso, enfocándose en destinos secundarios y menos conocidos.  
La propuesta consiste en una plataforma web que centraliza información de atractivos turísticos, permitiendo a los visitantes descubrir rutas alternativas y planificar sus viajes.

# Objetivo
Reducir la concentración turística en los cerros y sectores más populares, promoviendo experiencias en barrios, cerros y valles con baja visibilidad.

# Funcionalidades principales
- Catálogo interactivo de la Región de Valparaíso dividido por zonas (provincias).
- Filtrado dinámico por categorías de servicios y atractivos turísticos.
- Fichas detalladas de cada lugar con fotografías, descripciones y datos prácticos 
- Buscador contextual por palabras clave y comunas.

# Prototipo en Canva
- https://www.canva.com/design/DAHWzLyL2V0/LwoZ_RdiCF6ZNGmivJAATA/view?mode=prototype

# Integrantes
- Diego Fuentes  
- Alex Castillo  
- Estefania Salinas  
- Yutong Sun

# Tecnologías utilizadas
* Python 3.13.14
* Django 6.1.2
* Pillow 13.0.0
* asgiref 3.12.1
* sqlparse 0.6.0
* tzdata 2026.5

# Instalación y Ejecución Local

### 1. Prerrequisitos y Dependencias
- Tener instalado Python
- Clonar el repositorio
- Configurar/Crear un entorno virtual (Para crear: python -m venv venv. Para activar: .\venv\Scripts\activate)
Instalar dependencias necesarias del proyecto (pip install -r requirements.txt)

### 2. Sincronizar el código desde github usando una nueva terminal
Abrir una nueva terminal y agregar: 
- git fetch origin
- git checkout main
- git pull origin main

### 3. Probar datos iniciales
- python manage.py loaddata datos.json
    
### 4. Iniciar el Servidor de Desarrollo
- python manage.py runserver 
- Una vez iniciado, con ctrl + click entrar a http://127.0.0.1:8000/
