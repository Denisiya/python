import pygame

pygame.init()

painting = []
timer = pygame.time.Clock()
fps = 60
activeColor = (0, 0, 0)
activeShape = 0
W, H = 800, 600

screen = pygame.display.set_mode([W, H])
pygame.display.set_caption("Paint")

def drawDisplay():
    pygame.draw.rect(screen, (229, 255, 204), [0, 0, W, 86])
    pygame.draw.line(screen, 'gray', [0, 85], [W, 85])

    shapes = []

    # Квадрат
    square = [pygame.draw.rect(screen, (96, 96, 96), [10, 10, 70, 70]), 2]
    pygame.draw.rect(screen, 'white', [20, 20, 50, 50])
    shapes.append(square)

    # Круг
    circ = [pygame.draw.rect(screen, (96, 96, 96), [100, 10, 70, 70]), 1]
    pygame.draw.circle(screen, 'white', [135, 45], 30)
    shapes.append(circ)

    # Прямоугольный треугольник
    right_triangle = [pygame.draw.rect(screen, (96, 96, 96), [190, 10, 70, 70]), 3]
    pygame.draw.polygon(screen, 'white', [(195, 75), (230, 20), (265, 75)])
    shapes.append(right_triangle)

    # Равносторонний треугольник
    equilateral_triangle = [pygame.draw.rect(screen, (96, 96, 96), [280, 10, 70, 70]), 4]
    pygame.draw.polygon(screen, 'white', [(315, 20), (280, 75), (350, 75)])
    shapes.append(equilateral_triangle)

    # Ромб
    rhombus = [pygame.draw.rect(screen, (96, 96, 96), [370, 10, 70, 70]), 5]
    pygame.draw.polygon(screen, 'white', [(405, 45), (370, 75), (405, 105), (440, 75)])
    shapes.append(rhombus)

    # Кнопка ластика после ромба
    eraser = [pygame.draw.rect(screen, (255, 255, 255), [470, 10, 70, 70]), 6]
    pygame.draw.rect(screen, 'gray', [485, 25, 40, 40])
    shapes.append(eraser)

    colors = []
    blue = [pygame.draw.rect(screen, (0, 0, 255), [W - 35, 10, 25, 25]), (0, 0, 255)]
    red = [pygame.draw.rect(screen, (255, 0, 0), [W - 35, 35, 25, 25]), (255, 0, 0)]
    green = [pygame.draw.rect(screen, (0, 255, 0), [W - 60, 10, 25, 25]), (0, 255, 0)]
    yellow = [pygame.draw.rect(screen, (255, 255, 0), [W - 60, 35, 25, 25]), (255, 255, 0)]
    black = [pygame.draw.rect(screen, (0, 0, 0), [W - 85, 10, 25, 25]), (0, 0, 0)]
    purple = [pygame.draw.rect(screen, (255, 0, 255), [W - 85, 35, 25, 25]), (255, 0, 255)]

    colors += [blue, red, green, yellow, black, purple]

    return colors, shapes

def drawPaint(paints):
    for paint in paints:
        color, position, shape_id = paint
        if shape_id == 0:
            pygame.draw.rect(screen, color, [position[0] - 15, position[1] - 15, 30, 30])
        elif shape_id == 1:
            pygame.draw.circle(screen, color, position, 15)
        elif shape_id == 2:
            drawSquare(color, position)
        elif shape_id == 3:
            drawRightTriangle(color, position)
        elif shape_id == 4:
            drawEquilateralTriangle(color, position)
        elif shape_id == 5:
            drawRhombus(color, position)
        elif shape_id == 6:
            # Ластик стирает содержимое
            pygame.draw.rect(screen, (255, 255, 255), [position[0] - 15, position[1] - 15, 30, 30])

def drawSquare(color, position):
    size = 30
    pygame.draw.rect(screen, color, [position[0] - size // 2, position[1] - size // 2, size, size])

def drawRightTriangle(color, position):
    size = 30
    points = [(position[0], position[1]), (position[0] + size, position[1]), (position[0], position[1] + size)]
    pygame.draw.polygon(screen, color, points)

def drawEquilateralTriangle(color, position):
    size = 30
    height = size * (3 ** 0.5) / 2
    points = [(position[0], position[1] - height / 2), (position[0] - size / 2, position[1] + height / 2), (position[0] + size / 2, position[1] + height / 2)]
    pygame.draw.polygon(screen, color, points)

def drawRhombus(color, position):
    size = 30
    points = [(position[0], position[1] - size // 2), (position[0] + size // 2, position[1]), (position[0], position[1] + size // 2), (position[0] - size // 2, position[1])]
    pygame.draw.polygon(screen, color, points)

def draw():
    global activeColor, activeShape, mouse
    if mouse[1] > 100:
        if activeShape == 0:
            pygame.draw.rect(screen, activeColor, [mouse[0] - 15, mouse[1] - 15, 30, 30])
        elif activeShape == 1:
            pygame.draw.circle(screen, activeColor, mouse, 15)
        elif activeShape == 2:
            drawSquare(activeColor, mouse)
        elif activeShape == 3:
            drawRightTriangle(activeColor, mouse)
        elif activeShape == 4:
            drawEquilateralTriangle(activeColor, mouse)
        elif activeShape == 5:
            drawRhombus(activeColor, mouse)
        elif activeShape == 6:
            # Ластик стирает содержимое
            pygame.draw.rect(screen, (255, 255, 255), [mouse[0] - 15, mouse[1] - 15, 30, 30])

run = True
while run:
    timer.tick(fps)
    screen.fill('white')
    colors, shapes = drawDisplay()

    mouse = pygame.mouse.get_pos()
    draw()
    click = pygame.mouse.get_pressed()[0]
    if click and mouse[1] > 100:
        painting.append((activeColor, mouse, activeShape))
    drawPaint(painting)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                painting = []
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in colors:
                if i[0].collidepoint(event.pos):
                    activeColor = i[1]
            for i in shapes:
                if i[0].collidepoint(event.pos):
                    activeShape = i[1]

    pygame.display.flip()
pygame.quit()
