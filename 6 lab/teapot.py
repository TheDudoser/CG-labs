from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def drawFunc():
    # Очистить предыдущий экран
    glClear(GL_COLOR_BUFFER_BIT)
    glRotatef(0.1, 5, 5, 0)  # (Угол, х, у, г)
    glutWireTeapot(0.5)
    # Обновить дисплей
    glFlush()


# Используйте перенасыщение для инициализации OpenGL
glutInit()
# Режим отображения: прямое отображение GLUT_SINGLE без буфера | GLUT_RGBA использует RGB (не альфа)
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGBA)
# Положение и размер окна
glutInitWindowPosition(0, 0)
glutInitWindowSize(400, 400)
glutCreateWindow(b"first")
# Вызовите функцию, чтобы нарисовать изображение
glutDisplayFunc(drawFunc)
glutIdleFunc(drawFunc)

# glEnable(GL_COLOR_MATERIAL)
glEnable(GL_NORMALIZE)
# Основной цикл
glutMainLoop()