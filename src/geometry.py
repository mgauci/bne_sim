import math

sign = lambda x: math.copysign(1, x)

class Vec(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vec(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vec(self.x - other.x, self.y - other.y)
    def __mul__(self, scalar):
        return Vec(float(scalar)*self.x, float(scalar)*self.y)
    __rmul__ = __mul__
    def __div__(self, scalar):
        return self.__mul__(1.0/scalar)
#   Dot product.
    def dot(self, other):
        return self.x*other.x + self.y*other.y
#   Euclidean norm.
    def norm(self):
        return math.sqrt(pow(self.x, 2) + pow(self.y, 2))
#   Conversion to string for debugging purposes.
    def __str__(self):
        return "[" + str(self. x) + ", " + str(self.y) + "]"

class Line(object):
#   The equation of a line is Ax + By + C = 0.
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C
#   Conversion to string for debugging purposes.
    def __str__(self):
        return str(self.A) + "x + " + \
               str(self.B) + "y + " + \
               str(self.C) + " = 0"
               
class LineGivenTwoPoints(object):
    def __init__(self, point_1, point_2):
        x_1 = point_1.x
        y_1 = point_1.y
        x_2 = point_2.x
        y_2 = point_2.y
        self.A = y_2 - y_1
        self.B = x_1 - x_2
        self.C = x_2*y_1 - x_1*y_2
    #   Conversion to string for debugging purposes.
    def __str__(self):
        return str(self.A) + "x + " + \
               str(self.B) + "y + " + \
               str(self.C) + " = 0"
        

class Circle(object):
    def __init__(self, pos, radius):
        self.pos = pos
        self.radius = radius
    def area(self):
        return math.pi*(self.radius**2.0)
    def perimiter(self):
        return 2.0*math.pi*self.radius

class Square(object):
    def __init__(self, bottom_left_corner, top_right_corner):
        self.BL = bottom_left_corner
        self.TL = Vec(bottom_left_corner.x, top_right_corner.y)
        self.BR = Vec(top_right_corner.x, bottom_left_corner.y)
        self.TR = top_right_corner
        
        self.top_line    = LineGivenTwoPoints(self.TL, self.TR)
        self.right_line  = LineGivenTwoPoints(self.BR, self.TR)
        self.left_line   = LineGivenTwoPoints(self.BL, self.TL)
        self.bottom_line = LineGivenTwoPoints(self.BL, self.BR)
    def shift(self, shift_vector):
        self.BL += shift_vector
        self.TL += shift_vector
        self.BR += shift_vector
        self.TR += shift_vector
        
        self.top_line    = LineGivenTwoPoints(self.TL, self.TR)
        self.right_line  = LineGivenTwoPoints(self.BR, self.TR)
        self.left_line   = LineGivenTwoPoints(self.BL, self.TL)
        self.bottom_line = LineGivenTwoPoints(self.BL, self.BR)        
        

#   Perpendicular distance from a line to a point.
def LineToPointDistance(line, point):
    x = point.x #
    y = point.y # I'm defining these local      
    A = line.A  # variables just to make the
    B = line.B  # equations less cluttered.
    C = line.C  #
    return math.fabs(A*x + B*y + C) / math.sqrt(A**2 + B**2)
           
#   Returns 0 if the point is on the line, and -1 or 1 otherwise
#   depending on which side of the line the point is on.
def SideOfLineOfPoint(line, point):
    x = point.x #
    y = point.y # I'm defining these local      
    A = line.A  # variables just to make the
    B = line.B  # equations less cluttered.
    C = line.C  #
    return sign(A*x + B*y + C)
    
#   Returns the closest point on a line to another point.
def ClosestPointOnLineToPoint(line, point):
    x = point.x #
    y = point.y # I'm defining these local      
    A = line.A  # variables just to make the
    B = line.B  # equations less cluttered.
    C = line.C  #
    x_result = (B*(B*x - A*y) - A*C)/(A**2 + B**2)
    y_result = (A*(A*y - B*x) - B*C)/(A**2 + B**2)
    return Vec(x_result, y_result)

#   Returns the normalized perpendicular (i.e. normal) vector
#   from a line to a point.
def LineToPointUnitNormal(line, point):
    normal = point - ClosestPointOnLineToPoint(line, point)
    return normal/normal.norm()

def LineToCircleUnitNormal(line, circle):
    return LineToPointUnitNormal(line, circle.pos)
    
def CircleToCircleUnitNormal(circle_1, circle_2):
    normal = circle_2.pos - circle_1.pos
    return normal/normal.norm()

def CircleLinePenetration(circle, line):
    line_to_center_distance = LineToPointDistance(line, circle.pos)
    return max(circle.radius - line_to_center_distance, 0.0)
    
def CircleLineIntersection(circle, line):
    return CircleLinePenetration(circle, line) != 0

def CircleCirclePenetration(circle_1, circle_2):
    distance_between_centers = (circle_2.pos - circle_1.pos).norm()
    sum_of_radii = (circle_1.radius + circle_2.radius)
    return max(sum_of_radii - distance_between_centers, 0.0)
    
def CircleCircleIntersection(circle_1, circle_2):
    return CircleCirclePenetration(circle_1, circle_2) != 0
