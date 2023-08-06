"""A set of functions aiding in math for ProgModX"""
from numpy import arange
import numpy as np
from math import sin, cos, tan, pi
import random

def construct(expression, var="x"):
    """Returns a function computing the given expression"""
    def f(x):
        return eval(expression.replace("^", "**").replace(var, "x"))
    return f

def advConstruct(expression, *args, constants = {}):
    """Returns a function computing the given expression. The variable names need to be listed as individual string arguments.
    Constants is an optional argument with the name and value of constants in the expression"""
    #Setup a string for the definition of the resulting function
    string = """def func({}):
    return {}""".format(", ".join(args), expression.replace("^", "**")) #Join all arguments in the function call
    #Define the function using exec on the string
    exec(string, constants)
    return constants["func"]

def computeLists(function, low, high, step=1):
    """Returns a touple of two lists containing x values inbetween low and high, and the computed results for y.
    In the format of (x_list, y_list)"""
    #Constructs functions from the griven expressions if the expression is a string
    if type(function) == type(str()):
        function = construct(function)
    return (arange(low, high+1, step), [function(i) for i in arange(low, high+1, step)])

def newton(function, derivative, low, high, tolerance=1e-8, rounding = 3, iterations = 1000):
    """Uses Newtons way of finding the root of a function using the function and its derivative, within the given limits.
    Returns None if it can't find a solution that satisfies the tolerance after the defined number of terations"""
    xn = random.random()*(high-low)             #Seed       #Uses random seed
    TOL = tolerance                             #Tolerance
    N = iterations                              #Itterations
    i = 0                                       #Countingvar

    #Constructs functions from the griven expressions if the expression is a string
    if type(function) == type(str()):
        function = construct(function)
    if type(derivative) == type(str()):
        derivative = construct(derivative)
    
    #Beginning of Newtonian solution
    while i <= N and abs(function(xn)) >= TOL:
        xn = xn - function(xn)/derivative(xn)
        i += 1
    #Chech if the found value for x gives a y value within the tolerance
    if (abs(function(xn)) <= TOL) and (isInbetween(xn, low, high)):
        return round(xn, rounding)
    else:
        return None

def isInbetween(number, low, high):
    """Returns True if number is inbetween low and high, returns False otherwise"""
    if low <= number <= high:
        return True
    else:
        return False

def rectangleIntegral(function, low, high, n):
    """Returns the numerically calculated integral of the function f inbetween low and high using n rectangles"""
    #Constructs functions from the griven expressions if the expression is a string
    if type(function) == type(str()):
        function = construct(function)

    total = 0.0
    h = (high-low)/n

    for i in range(0, n):
        total += function( low+(i*h) )
    return total * h

def trapezoidIntegral(function, low, high, n):
    """Returns the numerically calculated integral of the function inbetween low and high using n trapezoids"""
    #Constructs functions from the griven expressions if the expression is a string
    if type(function) == type(str()):
        function = construct(function)

    total = (function(low)+function(high))/2.0
    h = (high-low)/n

    for i in range (1, n) :
        total += function(low+(i*h))
    return total * h

def simpsonIntegral(function, low, high, n):
    """Returns the numerically calculated integral of the function inbetween low and high using n quadratic splines"""
    #Constructs functions from the griven expressions if the expression is a string
    if type(function) == type(str()):
        function = construct(function)
    h = (high-low)/n

    sumOne = 0
    for i in range(2, n, 2):
        sumOne += function(low+i*h)

    sumTwo = 0
    for i in range(1, n, 2):
        sumTwo += function(low+i*h)

    total = function(low) + function(high) + 2*sumOne + 4*sumTwo
    return total * (h/3)

def euler(functionDerivative, low, high, y0, n):
    """Returns a numpy array x, containing the x values of the function, and an array F, containing the computed values for the antiderivative function of the given function functionDerivative inbetween low and high with N steps
    
    Only supports functions with one variable"""
    if type(functionDerivative) == type(str()):
        functionDerivative = construct(functionDerivative)
    h = (high-low)/(n-1)

    x = np.linspace(low, high, n)
    x[0] = low
    F = np.zeros(n)
    F[0] = y0

    #Eulers method
    for i in range(n-1):
        F[i+1] = F[i] + functionDerivative(x[i]) * h
        
    return x, F