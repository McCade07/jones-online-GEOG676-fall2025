#Create classes
class Shape():
    def __init__(self):
        pass

class Rectangle(Shape):
    def __init__(self, l, w):
        self.length = l
        self.width = w
    def GetArea(self):
        return self.length * self.width
    
class Circle(Shape):
    def __init__(self, r):
        self.radius = r
    def GetArea(self):
        return 3.14 * self.radius * self.radius
    
class Triangle(Shape):
    def __init__(self, b, h):
        self.base = b
        self.height = h
    def GetArea(self):
        return 0.5 * self.base * self.height
    
#Read in text file
file = open(r"C:/COLLEGE/GEOG_676/LABS/Lab3/shape.txt", "r")
lines = file.readlines()
file.close()

for line in lines:
    components = line.split(",")
    shape = components[0]

    if shape == "Rectangle":
        rect = Rectangle(int(components[1]), int(components[2]))
        print("Area of the Rectangle is: ", rect.GetArea())

    elif shape == "Circle":
        cir = Circle(int(components[1]))
        print("The area of the Circle is: ", cir.GetArea())

    elif shape == "Triangle":
        tri = Triangle(int(components[1]), int(components[2]))
        print("The area of the Triangle is: ", tri.GetArea())

    else:
        pass