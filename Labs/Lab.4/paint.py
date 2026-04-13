class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x= int(slope * y)
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))

    def __repr__(self):
        return f'paint.Canvas(width={self.width}, height={self.height})'

class Shape:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    def area(self):
        pass
    def perimeter(self):
        pass
    def get_x(self):
        return self.__x
    def get_y(self):
        return self.__y
    def get_per_points(self):
        pass
    def is_inside(self, x, y):
        pass
    def overlaps(self, other):
        for a, b in self.get_per_points():
            if other.is_inside(a, b):
                return True
        for a, b in other.get_per_points():
            if self.is_inside(a,b):
                return True
        return False

class Rectangle(Shape):
    def __init__(self, width, length, x, y):
        super().__init__(x,y)
        self.__width = abs(width)
        self.__length = abs(length)

    def area(self):
        return self.__width * self.__length
        
    def perimeter(self):
        return 2*(self.__width + self.__length)
        
    def get_length(self):
        return self.__length
    def get_width(self):
        return self.__width
        
    def get_per_points(self):
        x, y = self.get_x(), self.get_y()
        w, l = self.get_width(), self.get_length()
        return [
            (x,y),
            (x+w, y),
            (x+w, y+l),
            (x+w, y+l)
        ]
    def is_inside(self, a, b):
        x, y = self.get_x(), self.get_y()
        w, l = self.get_width(), self.get_length()
        return (x <= a <= x+w) and (y <= b <= y+l)
    def paint(self, canvas, char='o'):
        x, y = self.get_x(), self.get_y()
        w, l = self.get_width(), self.get_length()
        canvas.h_line(y, x, w, char=char)
        canvas.h_line(y+l-1,x,w, char=char)
        canvas.v_line(y, x, l, char=char)
        canvas.v_line(y,x+w-1,l, char=char)

    def __repr__(self):
        return "paint.Rectangle(" + repr(self.get_width()) + "," + repr(self.get_length()) + "," + repr(self.get_x()) + "," + repr(self.get_y()) + ")"
class Triangle(Shape):
    def __init__(self, a, b, c, x, y):
        super().__init__(x,y)
        self.__a = abs(a)
        self.__b = abs(b)
        self.__c = abs(c)

    def perimeter(self):
        return self.__a + self.__b + self.__c

    def area(self):
        area = self.perimeter() / 2
        return (area * (area - self.__a) * (area - self.__b) * (area - self.__c)) ** 0.5
    
    def get_a(self):
        return self.__a
    def get_b(self):
        return self.__b
    def get_c(self):
        return self.__c
    
    def get_per_points(self):
        x, y = self.get_x(), self.get_y()
        a, b, c = self.get_a(), self.get_b(), self.get_c()
        return [
            (x,y),
            (x+a, y),
            (x+(a/2), y+(b**2-(a/2)**2)**0.5)
        ]
    def is_inside(self, a, b):
        x1, y1 = self.get_x(), self.get_y()
        x2, y2 = x1 + self.get_a(), y1

        u = (self.__a **2 + self.__b**2 - self.__c**2) / (2 * self.__a)
        h_sq = self.__b**2 - u**2
        if h_sq < 0:
            return False
        h = h_sq ** 0.5
        x3, y3 = x1 + u, y1 + h
        denominator = ((y2 - y3)*(x1 - x3) + (x3 - x2)*(y1 -y3))
        if denominator == 0:
            return False
        a_weight = ((y2 - y3)*(a - x3) + (x3 - x2)*(b - y3)) / denominator
        b_weight = ((y3 - y1)*(a - x3) + (x1 - x3)*(b - y3)) / denominator
        c_weight = 1 - a_weight - b_weight
        return (0 <= a_weight <= 1) and (0 <= b_weight <= 1) and (0 <= c_weight <= 1)
    
    def paint(self, canvas, char='*'):
        for r in range(canvas.height):
            for c in range(canvas.width):
                if self.is_inside(c, r):
                    canvas.set_pixel(r, c, char)
    def __repr__(self):
        return "paint.Triangle(" + repr(self.get_a()) + "," + repr(self.get_b()) + "," + repr(self.get_c()) + "," + repr(self.get_x()) + "," + repr(self.get_y()) + ")"

class Circle(Shape):
    def __init__(self, radius, x, y):
        super().__init__(x,y)
        self.__radius = abs(radius)

    def area(self):
        return (355/113) * self.__radius**2
        
    def perimeter(self):
        return 2*(355/113)*self.__radius
        
    def get_radius(self):
        return self.__radius
    
    def get_per_points(self):
        x, y = self.get_x(), self.get_y()
        r = self.get_radius()
        
        diag = r * .707 #this trick I got from GeminiAI, it should return 8 points on the circle that includes diagonals. I want to add .707 is an approcimation of sin(45)
        return [
            (x + r, y), (x - r, y), (x, y + r), (x, y - r), # E, W, N, S
            (x + diag, y + diag), (x - diag, y + diag),    # NE, NW
            (x + diag, y - diag), (x - diag, y - diag)
        ]
    def is_inside(self, a, b):
        x, y = self.get_x(), self.get_y()
        r = self.get_radius()
        distance = (a -x)**2 + (b - y)**2
        return distance <= r**2
    
    def overlaps(self, other):  
        if isinstance(other, Circle):
            distance = (self.get_x() - other.get_x())**2 + (self.get_y() - other.get_y())**2
            return distance <= (self.get_radius() + other.get_radius())**2
        return False
    def paint(self, canvas, char='o'):
        for a, b in self.get_per_points():
            row, col = int(b), int(a)
            if 0 <= row < canvas.height and 0 <= col < canvas.width:
                canvas.set_pixel(row, col, char=char)
    def __repr__(self):
        return "paint.Circle(" + repr(self.get_radius()) + "," + repr(self.get_x()) + "," + repr(self.get_y()) + ")"