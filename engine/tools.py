from pygame import Vector2

def repairVector(V2):
    return Vector2(V2.x, V2.y)
def removeuseless(V2):
    x = V2.x
    y = V2.y
    if x < 0.05:
        x = 0
    if y < 0.05:
        y = 0
    return Vector2(x,y)

