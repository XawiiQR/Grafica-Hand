
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


### HandDetector.py

#### Constructor (`__init__`)

```python
class HandDetector:
    def __init__(self, hsv_file, width, height):
        self.scale = 2
        self.smallest_area = 1000.0
        self.min_finger_depth = 20
        self.max_finger_angle = 60

        self.cog_pt = None
        self.contour_axis_angle = None
        self.finger_tips = []
        self.current_gesture = ""

        self.hue_lower, self.hue_upper, self.sat_lower, self.sat_upper, self.val_lower, self.val_upper = self.read_hsv_ranges(hsv_file)
        self.width, self.height = width // self.scale, height // self.scale
```

**Propósito:** Inicializa la clase `HandDetector` con los parámetros de rango HSV y las dimensiones del cuadro de video. Define las variables necesarias para la detección de gestos y establece los valores predeterminados.

#### `read_hsv_ranges`

```python
def read_hsv_ranges(self, file):
    with open(file) as f:
        lines = f.readlines()
        hue_lower, hue_upper = map(int, lines[0].split()[1:])
        sat_lower, sat_upper = map(int, lines[1].split()[1:])
        val_lower, val_upper = map(int, lines[2].split()[1:])
    return hue_lower, hue_upper, sat_lower, sat_upper, val_lower, val_upper
```

**Propósito:** Lee los rangos HSV desde un archivo.

#### `update`

```python
def update(self, frame):
    frame_resized = cv2.resize(frame, (self.width, self.height))
    hsv_img = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2HSV)

    # filtro Gaussiano
    hsv_img = cv2.GaussianBlur(hsv_img, (5, 5), 0)

    mask = cv2.inRange(hsv_img, (self.hue_lower, self.sat_lower, self.val_lower),
                       (self.hue_upper, self.sat_upper, self.val_upper))

    mask = cv2.erode(mask, None, iterations=3)
    mask = cv2.dilate(mask, None, iterations=3)

    cv2.imshow("Mask", mask)  # Mostrar la máscara para depuración

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        self.current_gesture = "Piedra"
        return

    big_contour = max(contours, key=cv2.contourArea)
    if cv2.contourArea(big_contour) < self.smallest_area:
        self.current_gesture = "Piedra"
        return

    self.extract_contour_info(big_contour, self.scale)
    self.find_finger_tips(big_contour, self.scale)
    self.recognize_gesture()
```

**Propósito:** Procesa un cuadro de video, aplica filtros, encuentra contornos, y llama a otras funciones para extraer información del contorno y reconocer gestos.

#### `extract_contour_info`

```python
def extract_contour_info(self, contour, scale):
    moments = cv2.moments(contour)
    if moments['m00'] != 0:
        x_center = int(moments['m10'] / moments['m00']) * scale
        y_center = int(moments['m01'] / moments['m00']) * scale
        self.cog_pt = (x_center, y_center)

    self.contour_axis_angle = self.calculate_tilt(moments)
```

**Propósito:** Extrae el centro de gravedad y el ángulo del eje del contorno.

#### `calculate_tilt`

```python
def calculate_tilt(self, moments):
    m11 = moments['mu11']
    m20 = moments['mu20']
    m02 = moments['mu02']

    diff = m20 - m02
    if diff == 0:
        return 45 if m11 != 0 else 0

    theta = 0.5 * np.arctan2(2 * m11, diff)
    tilt = np.degrees(theta)

    if diff > 0 and m11 == 0:
        return 0
    if diff < 0 and m11 == 0:
        return -90
    if diff > 0 and m11 > 0:
        return tilt
    if diff > 0 and m11 < 0:
        return 180 + tilt
    if diff < 0 and m11 > 0:
        return tilt
    if diff < 0 and m11 < 0:
        return 180 + tilt

    return 0
```

**Propósito:** Calcula la inclinación del contorno usando momentos.

#### `find_finger_tips`

```python
def find_finger_tips(self, contour, scale):
    approx_contour = cv2.approxPolyDP(contour, 3, True)
    hull = cv2.convexHull(approx_contour, returnPoints=False)
    defects = cv2.convexityDefects(approx_contour, hull)

    if defects is None:
        return

    tip_pts = []
    fold_pts = []
    depths = []

    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(approx_contour[s][0] * scale)
        end = tuple(approx_contour[e][0] * scale)
        far = tuple(approx_contour[f][0] * scale)

        if d / 256 < self.min_finger_depth:
            continue

        tip_pts.append(start)
        fold_pts.append(far)
        depths.append(d / 256)

    self.reduce_tips(len(tip_pts), tip_pts, fold_pts, depths)
```

**Propósito:** Encuentra las puntas de los dedos y los pliegues en el contorno.

#### `reduce_tips`

```python
def reduce_tips(self, num_points, tip_pts, fold_pts, depths):
    self.finger_tips = []

    for i in range(num_points):
        if depths[i] < self.min_finger_depth:
            continue

        pdx = (i - 1) % num_points
        sdx = (i + 1) % num_points
        angle = self.angle_between(tip_pts[i], fold_pts[pdx], fold_pts[sdx])
        if angle >= self.max_finger_angle:
            continue

        self.finger_tips.append(tip_pts[i])

    # Ordenar las puntas de los dedos de izquierda a derecha
    self.finger_tips = sorted(self.finger_tips, key=lambda x: x[0])
```

**Propósito:** Reduce y ordena las puntas de los dedos.

#### `angle_between`

```python
def angle_between(self, tip, next_pt, prev_pt):
    return np.abs(np.degrees(np.arctan2(next_pt[1] - tip[1], next_pt[0] - tip[0]) -
                             np.arctan2(prev_pt[1] - tip[1], prev_pt[0] - tip[0])))
```

**Propósito:** Calcula el ángulo entre tres puntos.

#### `recognize_gesture`

```python
def recognize_gesture(self):
    finger_count = len(self.finger_tips)

    if finger_count == 0:
        self.current_gesture = "Piedra"
    elif finger_count == 1:
        self.current_gesture = "Like"
    elif finger_count == 2:
        self.current_gesture = "Tijera"
    elif finger_count == 3:
        self.current_gesture = "OK"
    elif finger_count == 4:
        self.current_gesture = "Saludo"
    elif finger_count == 5:
        self.current_gesture = "Stop"
    else:
        self.current_gesture = "Desconocido"
```

**Propósito:** Reconoce el gesto basado en la cantidad de dedos visibles.

#### `draw`

```python
def draw(self, frame):
    if not self.finger_tips and self.current_gesture != "Piedra":
        return

    # Contador de dedos
    finger_count = len(self.finger_tips)

    for pt in self.finger_tips:
        cv2.circle(frame, pt, 8, (0, 255, 0), 2)
        cv2.line(frame, self.cog_pt, pt, (0, 255, 0), 2)

    cv2.circle(frame, self.cog_pt, 8, (0, 0, 255), -1)

    # Mostrar el contador de dedos
    cv2.putText(frame, f'Dedos: {finger_count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Mostrar el gesto
    cv2.putText(frame, f'Gesto: {self.current_gesture}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
```

**Propósito:** Dibuja los resultados en el cuadro de video.


### JMFCapture

Esta clase se encarga de capturar video en tiempo real desde la cámara utilizando OpenCV.

`JMFCapture.py`

### HandPanel

Esta clase utiliza `HandDetector` y `JMFCapture` para procesar y mostrar gestos de la mano en tiempo real.

`HandPanel.py`

### Handy

Esta clase ejecuta el procesamiento de gestos de la mano, además de proporcionar una interfaz para ajustar los valores HSV en tiempo real.

`Handy.py`

## Videos de Ejemplo

Para ver ejemplos de cómo se ejecuta el proyecto y los gestos que identifica, consulta los siguientes GIFs:

### Piedra
![Piedra](https://github.com/XawiiQR/Grafica-Hand/blob/main/VideoManos/piedra.gif)

### Like
![Like](https://github.com/XawiiQR/Grafica-Hand/blob/main/VideoManos/like.gif)

### Tijera
![Tijera](https://github.com/XawiiQR/Grafica-Hand/blob/main/VideoManos/tijera.gif)

### OK
![OK](https://github.com/XawiiQR/Grafica-Hand/blob/main/VideoManos/OK.gif)

### Saludo
![Saludo](https://github.com/XawiiQR/Grafica-Hand/blob/main/VideoManos/saludo.gif)

### Stop
![Stop](https://github.com/XawiiQR/Grafica-Hand/blob/main/VideoManos/stop.gif)

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cualquier cambio que te gustaría realizar.

## Licencia

Este proyecto está bajo la Licencia MIT.

## Autores

- Chambi Tapia Kevin
- Humana Chaquira Luciana
- Quispe Rojas Javier
- Sumare Josue
