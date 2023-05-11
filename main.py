import turtle
import random
import time

BOX_SIZE = 10
MAX_FOOD = 3
NORMAL_FOOD_TIMEOUT = 15
FOOD_INTERVAL = 5

def circle(xy, radius, color):
    turtle.up()
    # turtle.goto(xy + turtle.Vec2D(BOX_SIZE, BOX_SIZE+ 5))
    turtle.goto(xy + turtle.Vec2D(BOX_SIZE // 2, BOX_SIZE //2))
    turtle.down()
    turtle.color(color)
    turtle.fillcolor(color)
    # turtle.begin_fill()
    # turtle.circle(radius)
    # turtle.end_fill()
    turtle.dot(radius * 2, color)
    turtle.up()

def rect(xy, width, height, color, fillColor = None, fill = True):
    x = xy[0]
    y = xy[1]
    turtle.up()
    turtle.goto(x, y)
    turtle.color(color)
    turtle.down()
    if fill:
        if fillColor is None:
            fillColor = 'grey'
        turtle.fillcolor(fillColor)
        turtle.begin_fill()
    turtle.goto(x + width, y)
    turtle.goto(x + width, y - height)
    turtle.goto(x, y - height)
    turtle.goto(x, y)
    if fill:
        turtle.end_fill()
    turtle.up()


class Snake:
    def __init__(self, app, xy=None):
        self.app = app
        if xy is None:
            pos = turtle.Vec2D(
                # (turtle.window_width() // 2) // 10 * 10,
                # (turtle.window_height() // 2) // 10 * 10
                0, 0
            )
        else:
            pos = xy
        self.dir = turtle.Vec2D(BOX_SIZE, 0)
        self.tail = [pos]

    def reset(self):
        self.tail = [turtle.Vec2D(0, 0)]
        self.dir = turtle.Vec2D(BOX_SIZE, 0)

    def draw(self):
        colorStep = 1 / len(self.tail)
        r, b = 0, 1
        for body in self.tail:
            r += colorStep
            b -= colorStep
            circle(body, BOX_SIZE / 2, (r, 0, b))

    def update(self, grow=False):
        self.tail.append(self.tail[-1] + self.dir)
        if not grow:
            del self.tail[0]

    def switchDir(self, direction):
        d= self.dir
        if direction == 'up' and d != turtle.Vec2D(0, -BOX_SIZE):
            self.dir = turtle.Vec2D(0, BOX_SIZE)
        if direction == 'down' and d != turtle.Vec2D(0, BOX_SIZE):
            self.dir = turtle.Vec2D(0, -BOX_SIZE)
        if direction == 'left' and d != turtle.Vec2D(BOX_SIZE, 0):
            self.dir = turtle.Vec2D(-BOX_SIZE, 0)
        if direction == 'right' and d != turtle.Vec2D(-BOX_SIZE, 0):
            self.dir = turtle.Vec2D(BOX_SIZE, 0)

    def inColision(self) -> bool:
        for i in range(len(self.tail) - 1):
            if self.tail[-1] == self.tail[i]:
                return True
        xy = self.tail[-1]
        if xy[0] < self.app.left:
            return True
        if xy[0] + BOX_SIZE> self.app.right:
            return True
        if xy[1] - BOX_SIZE< self.app.bottom:
            return True
        if xy[1] + BOX_SIZE > self.app.top:
            return True
        return False


class Food:
    def __init__(self, app, xy = None, foodType = 'normal'):
        self.app = app
        self.type = foodType
        if xy is None:
            self.pos = turtle.Vec2D(
                random.randint(self.app.left, self.app.right) // 10 * 10,
                random.randint(self.app.bottom, self.app.top) // 10 * 10
            )
        else:
            self.pos = xy
        self.color = "green"
        self.timeout = NORMAL_FOOD_TIMEOUT
        self.visible = True

    def draw(self):
        if self.visible:
            circle(self.pos, BOX_SIZE / 2, self.color)

    def hide(self):
        self.visible = False

    def show(self):
        self.visible = True


class Foods:
    def __init__(self, app, max=MAX_FOOD, foodInterval=FOOD_INTERVAL):
        self.list = []
        self.app = app
        self.max = max
        self.score = 0
        self.foodInterval = foodInterval

    def reset(self):
        self.list = []
        self.score = 0

    def addFood(self, food=None):
        if len(self.list) < self.max:
            if food is None:
                f = Food(self.app)
            else:
                f = food
            self.list.append(f)
            turtle.ontimer(lambda: self.delFood(f), f.timeout * 1000)

    def delFood(self, food):
        if food in self.list:
            food.hide()
            self.list.remove(food)

    def draw(self):
        for f in self.list:
            f.draw()

    def eaten(self, snake):
        for f in self.list:
            if snake.tail[-1] == f.pos:
                t = f.type
                self.delFood(f)
                self.addFood(Food(self.app, foodType=t))
                self.score += 1
                return True
        return False


class App:
    def __init__(self):
        turtle.setup(640, 480, 0, 0)
        turtle.hideturtle()
        turtle.tracer(False)
        self.top = turtle.window_height() // 2 - BOX_SIZE
        self.bottom = -(turtle.window_height() // 2) + BOX_SIZE
        self.left = -(turtle.window_width() // 2 - BOX_SIZE)
        self.right = turtle.window_width() // 2 - BOX_SIZE * 2
        self.snake = Snake(self)
        self.foods = Foods(self)
        self.beginTime = None
        self.inGame = False
        # self.drawWall()
        turtle.clear()
        turtle.listen()
        turtle.onkey(lambda: self.snake.switchDir('up'), "Up")
        turtle.onkey(lambda: self.snake.switchDir('down'), "Down")
        turtle.onkey(lambda: self.snake.switchDir('left'), "Left")
        turtle.onkey(lambda: self.snake.switchDir('right'), "Right")
        turtle.onkey(lambda: self.setupGame(True), "space")
        self.setupGame()

    def setupGame(self, run=False):
        if self.inGame:
            return 
        self.snake.reset()
        turtle.clear()
        self.foods.reset()
        self.setFood()
        self.beginTime = None
        if run:
            self.run()

    def setFood(self, time = FOOD_INTERVAL):
        self.foods.addFood()
        turtle.ontimer(lambda: self.setFood(time), FOOD_INTERVAL * 1000)

    def drawWall(self):
        top = turtle.window_height() // 2
        bottom = -(turtle.window_height() // 2) + BOX_SIZE * 2
        left = -(turtle.window_width() // 2)
        right = turtle.window_width() // 2 - BOX_SIZE * 2
        for y in range(bottom, top + 1, BOX_SIZE):
            rect(turtle.Vec2D(left, y), BOX_SIZE, BOX_SIZE, 'black', 'grey', True)
            rect(turtle.Vec2D(left + 2, y -2), BOX_SIZE -2, BOX_SIZE - 2, 'grey', 'black', True)
            rect(turtle.Vec2D(right, y), BOX_SIZE, BOX_SIZE, 'black', 'grey', True)
            rect(turtle.Vec2D(right + 2, y -2), BOX_SIZE -2, BOX_SIZE - 2, 'grey', 'black', True)

        for x in range(left, right + 1, BOX_SIZE):
            rect(turtle.Vec2D(x, top), BOX_SIZE, BOX_SIZE, 'black', 'grey', True)
            rect(turtle.Vec2D(x + 2, top - 2), BOX_SIZE - 2, BOX_SIZE - 2, 'grey', 'black', True)
            rect(turtle.Vec2D(x, bottom), BOX_SIZE, BOX_SIZE, 'black', 'grey', True)
            rect(turtle.Vec2D(x + 2, bottom - 2), BOX_SIZE - 2, BOX_SIZE - 2, 'grey', 'black', True)


    def showGameOverText(self):
        turtle.up()
        turtle.color('green')
        turtle.goto(0, 0)
        turtle.write(f"Game Over! You picked up {self.foods.score} balls", False, align="center")
        turtle.goto(0, -200)
        turtle.write(f"Press SPACE to start over!", False, align="center")

    def run(self):
        if self.beginTime is None:
            self.beginTime = time.time()
            self.inGame = True
        if not self.inGame:
            return
        turtle.clear()
        self.drawWall()
        # self.snake.draw()
        # self.foods.draw()

        if self.foods.eaten(self.snake):
            self.snake.update(True)
        else:
            self.snake.update()
        self.snake.draw()
        self.foods.draw()

        if self.snake.inColision():
            self.inGame = False
            self.showGameOverText()
            return

        turtle.update()
        turtle.ontimer(lambda: self.run(), 100)


app = App()
app.run()
turtle.exitonclick()

