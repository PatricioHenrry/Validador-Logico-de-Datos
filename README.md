**🔍 Validador Lógico de Registros 🔍**

Validador de datos desarrollado en Python que verifica la integridad y consistencia de registros de usuarios según reglas de negocio predefinidas.

📋 **Características**

- Validación completa de campos: DNI, edad, sexo y plan de salud

- Detección de duplicados en campo DNI

- Múltiples modos de entrada: teclado o dataset de ejemplo

- Exportación automática con numeración incremental

- Mensajes descriptivos de error para cada registro

- Normalización inteligente de datos de entrada

📋 **Campos Validados**

- DNI	en formato numérico (7-8 dígitos) con prevención de duplicados
- Edad	en rango válido (0-100 años)
- Sexo	en valores aceptados: H/Hombre, M/Mujer
- Plan de Salud	en valores: "basico" o "premium"

🛠️ **Tecnologías Utilizadas**

- Python 3.x

- Pandas - Manipulación de datos

- Pathlib - Manejo de archivos

- Re - Expresiones regulares

📋 **Instalación**

- Clona el repositorio:

`````bash`````
        `````git clone https://github.com/tu-usuario/validador-registros.git`````
         `````   cd validador-registros`````
            
- Instala las dependencias:

`````bash`````
         `````   pip install pandas`````
            
💻 **Uso**

- Ejecución básica:
- 
`````bash`````
           ````` python validador.py`````



 📋 **Funcionalidades Principales**
 
-  Formato y longitud de DNI

-  Rango de edad permitido

-  Categorías de sexo válidas

- Planes de salud aceptados
  
-  Detección de DNIs duplicados

 📋 **Características Adicionales**

-  Manejo robusto de errores

-  Guardado automático con prevención de sobreescritura

-  Normalización de texto y categorías

-  Interfaz interactiva por consola

