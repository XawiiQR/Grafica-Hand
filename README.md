
# HandGestureRecognizer

**HandGestureRecognizer** es un proyecto que utiliza OpenCV para detectar y reconocer gestos de la mano basándose en la cantidad de dedos visibles. Es capaz de identificar gestos como "Piedra", "Like", "Tijera", "OK", "Saludo" y "Stop".

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

```python
import cv2
from hand_gesture_recognizer import HandDetector, JMFCapture, HandPanel, Handy

# Para ejecutar el detector de gestos
handy = Handy()
handy.run()
```

## Código de Ejemplo

### `HandDetector.py`
```python
import cv2
import numpy as np

class HandDetector:
    # Código proporcionado anteriormente
```

### `JMFCapture.py`
```python
import cv2

class JMFCapture:
    # Código proporcionado anteriormente
```

### `HandPanel.py`
```python
import cv2
from HandDetector import HandDetector
from JMFCapture import JMFCapture

class HandPanel:
    # Código proporcionado anteriormente
```

### `Handy.py`
```python
import cv2
from HandPanel import HandPanel
from HandDetector import HandDetector

def nothing(x):
    pass

class Handy:
    # Código proporcionado anteriormente
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cualquier cambio que te gustaría realizar.

## Licencia

Este proyecto está bajo la Licencia MIT.

## Autores

- [Tu Nombre]
