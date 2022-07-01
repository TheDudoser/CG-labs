# Импортируем все необходимые библиотеки:
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys

# Объявляем все глобальные переменные
global xrot  # Величина вращения по оси x
global yrot  # Величина вращения по оси y
global ambient  # рассеянное освещение
global color  # Цвет торов
global lightpos  # Положение источника освещения

# Торы
torus = (0.2, 0.5, 15, 15)
wire_torus = (0.2, 0.5, 15, 15)


def draw_axis() -> None:
    axis_length = 2.0
    glPushMatrix()
    glBegin(GL_LINES)
    for i in range(3):
        glColor3f(*[1.0 if i == j else 0.0 for j in range(3)])
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(*[axis_length if i == j else 0.0 for j in range(3)])
    glEnd()
    glPopMatrix()


def spin_object() -> None:
    global xrot
    xrot += 1.0
    glutPostRedisplay()


# Процедура инициализации
def init():
    global xrot  # Величина вращения по оси x
    global yrot  # Величина вращения по оси y
    global ambient  # Рассеянное освещение
    global color  # Цвет елочных иголок
    global lightpos  # Положение источника освещения

    xrot = 0.0  # Величина вращения по оси x = 0
    yrot = 0.0  # Величина вращения по оси y = 0
    ambient = (1.0, 1.0, 1.0, 0.5)  # Первые три числа цвет в формате RGB, а последнее - яркость
    color = (1.0, 0.0, 0.0, 0.5)
    lightpos = (1.0, 1.0, 1.0)  # Положение источника освещения по осям xyz

    # Окрашиваем весь экран в серый цвет
    glClearColor(0.5, 0.5, 0.5, 1.0)
    # Определяем границы рисования по горизонтали и вертикали
    gluOrtho2D(-2.0, 2.0, -2.0, 2.0)

    # Повернуть камеру под нужным углом
    glRotatef(-60, 1.0, 0.0, 0.0)
    glRotatef(-135, 0.0, 0.0, 1.0)

    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, ambient)  # Определяем текущую модель освещения
    glEnable(GL_LIGHTING)  # Включаем освещение
    glEnable(GL_LIGHT0)  # Включаем один источник света

    # glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)


    # Определяем положение источника света
    glLightfv(GL_LIGHT0, GL_POSITION, lightpos)
    glShadeModel(GL_SMOOTH)


# Процедура обработки специальных клавиш
def specialkeys(key, _, __):
    global xrot
    global yrot
    # Обработчики для клавиш со стрелками
    if key == GLUT_KEY_UP:  # Клавиша вверх
        xrot -= 2.0  # Уменьшаем угол вращения по оси Х
    if key == GLUT_KEY_DOWN:  # Клавиша вниз
        xrot += 2.0  # Увеличиваем угол вращения по оси Х
    if key == GLUT_KEY_LEFT:  # Клавиша влево
        yrot -= 2.0  # Уменьшаем угол вращения по оси Y
    if key == GLUT_KEY_RIGHT:  # Клавиша вправо
        yrot += 2.0  # Увеличиваем угол вращения по оси Y

    glutPostRedisplay()  # Вызываем процедуру перерисовки


# Процедура перерисовки
def draw():
    global xrot
    global yrot
    global lightpos
    global color

    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT)  # Очищаем экран и заливаем серым цветом

    draw_axis()

    glPushMatrix()

    glRotatef(xrot, 1.0, 0.0, 0.0)  # Вращаем по оси X на величину xrot
    glRotatef(yrot, 0.0, 1.0, 0.0)  # Вращаем по оси Y на величину yrot

    # Рисуем торы
    # Устанавливаем материал: рисовать с 2 сторон, рассеянное освещение
    glMaterialfv(GL_FRONT, GL_DIFFUSE, color)

    glutSolidTorus(*torus)
    glTranslatef(0.0, 0.0, 0.5)
    glFlush()

    glutWireTorus(*wire_torus)
    glTranslatef(0.0, 0.0, 10.0)

    glutPostRedisplay()

    # Сдвинемся по оси Z на 0.2
    # Рисуем нижние ветки (конус) с радиусом 0.5, высотой 0.5
    # Последние два числа определяют количество полигонов

    # innerRadius, outerRadius, nsides, rings
    # Inner radius of the torus.
    # Outer radius of the torus.
    # Number of sides for each radial section.
    # Number of radial divisions for the torus.

    glPopMatrix()
    glutSwapBuffers()  # Выводим все нарисованное в памяти на экран


# Здесь начинается выполнение программы
# Использовать двойную буферизацию и цвета в формате RGB (Красный, Зеленый, Синий)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
# Указываем начальный размер окна (ширина, высота)
glutInitWindowSize(800, 800)
# Указываем начальное положение окна относительно левого верхнего угла экрана
glutInitWindowPosition(50, 50)
# Инициализация OpenGl
glutInit(sys.argv)
# Создаем окно с заголовком "Happy New Year!"
glutCreateWindow(b"Torus")
# Определяем процедуру, отвечающую за перерисовку
glutDisplayFunc(draw)

glutIdleFunc(spin_object)
# Определяем процедуру, отвечающую за обработку клавиш
glutSpecialFunc(specialkeys)
# Вызываем нашу функцию инициализации
init()
# Запускаем основной цикл
glutMainLoop()