from math import sqrt
def get_Percentage(Max, Value):
    fraction = float(Value) / Max
    return fraction

def get_Distance(v1, v2):
    x = v1[0] - v2[0]
    y = v1[1] - v2[1]
    return sqrt(x**2 + y**2)

class Timer(object):
    
