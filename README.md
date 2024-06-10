
# HandGestureRecognizer

**HandGestureRecognizer** es un proyecto desarrollado por Chambi Tapia Kevin, Humana Chaquira Luciana, Quispe Rojas Javier, y Sumare Josue. Este proyecto utiliza OpenCV para detectar y reconocer gestos de la mano basándose en la cantidad de dedos visibles. Es capaz de identificar gestos como "Piedra", "Like", "Tijera", "OK", "Saludo" y "Stop".

## Características

- **Detección de dedos:** Detecta la cantidad de dedos visibles.
- **Reconocimiento de gestos:** Identifica gestos específicos basados en la cantidad de dedos.
- **Visualización:** Dibuja los resultados en tiempo real en el cuadro de video.
- **Configuración HSV:** Permite configurar los rangos de color para la detección de la piel de la mano.
- **Ajustes en tiempo real:** Ajusta los valores HSV utilizando una interfaz de usuario interactiva con trackbars.

## Instalación

1. Clona este repositorio.
2. Instala las dependencias necesarias:
   ```bash
   pip install opencv-python numpy
   ```
3. Asegúrate de tener un archivo `gloveHSV.txt` con los rangos HSV configurados correctamente.

## Uso

Para ejecutar el detector de gestos, utiliza el siguiente comando:

```bash
python hand.py
```

El archivo `hand.py` debe contener el siguiente código para inicializar y ejecutar el proyecto:

```python
import cv2
from HandPanel import HandPanel

if __name__ == "__main__":
    hand_panel = HandPanel()
    hand_panel.run()
```

## Explicación del Proyecto

**HandGestureRecognizer** se compone de varias partes clave:

### HandDetector

Esta clase se encarga de detectar los gestos de la mano en base a la cantidad de dedos visibles. Utiliza OpenCV para procesar cuadros de video y aplicar filtros de color HSV, encontrar contornos y reconocer los gestos.

`HandDetector.py`

### JMFCapture

Esta clase se encarga de capturar video en tiempo real desde la cámara utilizando OpenCV.

`JMFCapture.py`

### HandPanel

Esta clase utiliza `HandDetector` y `JMFCapture` para procesar y mostrar gestos de la mano en tiempo real.

`HandPanel.py`

### Handy

Esta clase ejecuta el procesamiento de gestos de la mano, además de proporcionar una interfaz para ajustar los valores HSV en tiempo real.

`Handy.py`

### Videos de Ejemplo

Para ver ejemplos de cómo se ejecuta el proyecto y los gestos que identifica, consulta los siguientes videos:

- [Video 1: Identificación de "Piedra"](link_al_video)
- [Video 2: Identificación de "Like"](link_al_video)
- [Video 3: Identificación de "Tijera"](link_al_video)
- [Video 4: Identificación de "OK"](link_al_video)
- [Video 5: Identificación de "Saludo"](link_al_video)
- [Video 6: Identificación de "Stop"](link_al_video)

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cualquier cambio que te gustaría realizar.

## Licencia

Este proyecto está bajo la Licencia MIT.

## Autores

- Chambi Tapia Kevin
- Humana Chaquira Luciana
- Quispe Rojas Javier
- Sumare Josue
