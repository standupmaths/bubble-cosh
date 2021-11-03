import math as maths

inf = 1000000000000 #stupid big error

def error_get(a,b,d,l):
    # assume everything is already a float
    # I've worked this out from the end conditions
    try:
        x1 = 0
        y1 = d/2
        e1 = a*maths.cosh((x1-b)/a) - y1
        x2 = l
        y2 = d/2
        e2 = a*maths.cosh((x2-b)/a) - y2
        error = abs(e1)+abs(e2)
        return error
    except:
        return inf

def a_b_finder(d,l):
    d *= 1.0
    l *= 1.0
    #takes the diameter of the hoop and distance apart to give a and b
    prec = 0.0000001   #target precision
    step = 0.1   # I will start moving in milimetres on the scale of metres
    error = inf 
    a=1.0
    b=1.0
    #print([a,b])
    while error > prec:
        more_work_to_do = 1
        best_error = error
        new_best_a = a
        new_best_b = b
        while more_work_to_do == 1:
            old_error = best_error
            a_s = [a-step,a,a+step]
            b_s = [b-step,b,b+step]
            for disa in a_s:
                for disb in b_s:
                    dis_error = error_get(disa,disb,d,l)
                    #print("a:{0} b:{1} e:{2}".format(disa,disb,dis_error,best_error))
                    if dis_error < best_error:
                        #print("best")
                        best_error = dis_error
                        new_best_a = disa
                        new_best_b = disb
            if best_error == old_error:    #then there was no improvement
                more_work_to_do = 0
            else:
                a = new_best_a
                b = new_best_b
        error = best_error
        step /= 10.0
        if step < prec:
            #print(error)
            error = 0
        #print("STEP CHANGE: {0}".format(step))
    #print(error)
    #return best_error
    return[a,b]

def total_area(a,b,d,l):
    return maths.pi*(a**2)*(maths.sinh(l/a)+(l/a))


d = 1.068
l = 0.6

these_values = a_b_finder(d,l)
a = these_values[0]
b = these_values[1]

print("for diameters of {0} and length of {1}".format(d,l))
print(these_values)

mid_radius = a*maths.cosh(((l/2)-b)/a)

print("Area of {0}".format(total_area(a,b,d,l)))
print("mid dip of {0}".format((d/2)-mid_radius))
print("mid gap of {0}".format(mid_radius*2))
"""

# saving out errors only
# need to change a_b_finder to return best_error
d = 1.0
l=0.01
while l <= d:
    e = a_b_finder(d,l)
    print("{0}\t{1}".format(l,e))
    l += 0.01

"""