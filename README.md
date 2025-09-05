## 📊 Generador de Datos Sintéticos de E-commerce
Este proyecto contiene un script de Python (`synthetic_data_generator.py`) diseñado para crear datasets de ejemplo para e-commerce. Utiliza **Ollama** y el modelo **Mistral** para generar nombres de productos y reseñas de clientes realistas, lo que lo hace ideal para pruebas de software, análisis de datos, demostraciones de bases de datos y machine learning.
### ✨ Características
- **Generación Inteligente**: Utiliza un modelo de lenguaje (**Mistral**) para generar nombres de productos, descripciones y reseñas que parecen auténticos y coherentes.
- **Datasets Coherentes**: Genera datos interrelacionados para productos y reseñas, incluyendo campos como `product_id`, `category`, `price`, `rating`, `review_text` y `review_date`.
- **Salidas Versátiles**: Los datos se guardan en múltiples formatos: **JSON** para una fácil manipulación y **CSV** para análisis de datos.
- **Estadísticas en Tiempo Real**: Muestra un resumen de los datos generados, incluyendo el número de productos y reseñas, y la distribución por categoría.
- **Modo 'Append'**: Permite añadir nuevos datos a los archivos existentes, lo que es útil para simular el crecimiento de un dataset a lo largo del tiempo.
- **Altamente Personalizable**: Permite configurar el número de productos y el rango de reseñas por producto para ajustar el tamaño del dataset.
### 🚀 Requisitos
- **Python 3.6+**
- **Ollama**: Asegúrate de tener Ollama instalado y ejecutándose en tu máquina.
- **Modelo Mistral**: El script asume que el modelo `mistral` ya está descargado y disponible en tu instancia de Ollama. Si no lo tienes, puedes descargarlo fácilmente desde tu terminal con el comando: `ollama run mistral` (luego puedes cancelar la ejecución).
### 🛠️ Uso
#### 1. Configuración Inicial
Asegúrate de tener los requisitos instalados. El script se conectará automáticamente a la URL por defecto de Ollama (`http://localhost:11434`).
#### 2. Generar un Nuevo Dataset
Ejecuta el script para generar un dataset completamente nuevo. Esto creará archivos con un timestamp único en sus nombres (por ejemplo, `products_20250905_154100.csv`).

`python synthetic_data_generator.py`

Puedes ajustar el número de productos y reseñas en la llamada a la función generate_dataset. Por ejemplo, para generar 50 productos y entre 1 y 8 reseñas por producto, usa el siguiente código:

`generator = SyntheticDataGenerator()`

`products, reviews = generator.generate_dataset(num_products=50, reviews_per_product=(1, 8))`

`generator.save_data(products, reviews)`

### 📂 Estructura de los Datos
El script genera dos tipos de archivos, cada uno disponible en formato JSON y CSV.

`products.json` / `products.csv`
| Campo | Tipo | Descripción | Ejemplo |
|:---|:---|:---|:---|
| `product_id` | `str` | Identificador único del producto. | `PROD_a1b2c3d4` |
| `category` | `str` | Categoría del producto. | `Electronics` |
| `brand` | `str` | Marca del producto. | `TechFlow` |
| `name` | `str` | Nombre generado por la IA. | `Wireless Mechanical Keyboard` |
| `description`| `str` | Descripción generada por la IA. | `A high-performance keyboard with customizable RGB lighting...`|
| `price` | `float`| Precio del producto. | `129.99` |
| `stock` | `int` | Número de unidades en stock. | `150` |
| `rating` | `float`| Puntuación promedio inicial. | `4.7` |
| `created_date`| `str` | Fecha de creación del registro. | `2025-09-05T15:41:00`|

`reviews.json` / `reviews.csv`
| Campo | Tipo | Descripción | Ejemplo |
|:---|:---|:---|:---|
| `review_id` | `str` | Identificador único de la reseña. | `uuid4` |
| `product_id` | `str` | `ID` del producto al que pertenece la reseña. | `PROD_a1b2c3d4` |
| `reviewer_name`| `str` | Nombre aleatorio del reseñador. | `Emily C.` |
| `rating` | `int` | Puntuación de la reseña (1 a 5). | `5` |
| `review_text` | `str` | Texto de la reseña generado por la IA. | `Excellent product! Exceeded my expectations.` |
| `review_date` | `str` | Fecha en la que se creó la reseña. | `2025-08-20T10:30:00`|
| `verified_purchase`| `bool` | Indica si la compra fue verificada. | `True` |

## 👏 Agradecimientos y Contacto

Este proyecto es una herramienta para simplificar la creación de datos de prueba y análisis. Fue posible gracias a la flexibilidad de [Ollama](https://ollama.com/) y al poder del modelo [Mistral](https://mistral.ai/).

Si tienes alguna pregunta, sugerencia o encuentras algún problema, no dudes en abrir un *issue* en este repositorio. ¡Gracias por usar el generador!
