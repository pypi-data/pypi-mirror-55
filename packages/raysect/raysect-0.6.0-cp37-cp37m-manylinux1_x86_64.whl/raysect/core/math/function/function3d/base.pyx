# cython: language_level=3

# Copyright (c) 2014-2018, Dr Alex Meakins, Raysect Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#     3. Neither the name of the Raysect Project nor the names of its
#        contributors may be used to endorse or promote products derived from
#        this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import numbers
cimport cython
from libc.math cimport floor
from .autowrap cimport autowrap_function3d


cdef class Function3D:
    """
    Cython optimised class for representing an arbitrary 3D function.

    Using __call__() in cython is slow. This class provides an overloadable
    cython cdef evaluate() method which has much less overhead than a python
    function call.

    For use in cython code only, this class cannot be extended via python.

    To create a new function object, inherit this class and implement the
    evaluate() method. The new function object can then be used with any code
    that accepts a function object.
    """

    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        raise NotImplementedError("The evaluate() method has not been implemented.")

    def __call__(self, double x, double y, double z):
        """ Evaluate the function f(x, y, z)

        :param float x: function parameter x
        :param float y: function parameter y
        :param float y: function parameter z
        :rtype: float
        """
        return self.evaluate(x, y, z)

    def __add__(object a, object b):
        if isinstance(a, Function3D):
            if isinstance(b, Function3D):
                # a() + b()
                return AddFunction3D(<Function3D> a, <Function3D> b)
            elif isinstance(b, numbers.Real):
                # a() + B -> B + a()
                return AddScalar3D(<double> b, <Function3D> a)
        elif isinstance(a, numbers.Real):
            if isinstance(b, Function3D):
                # A + b()
                return AddScalar3D(<double> a, <Function3D> b)
        return NotImplemented

    def __sub__(object a, object b):
        if isinstance(a, Function3D):
            if isinstance(b, Function3D):
                # a() - b()
                return SubtractFunction3D(<Function3D> a, <Function3D> b)
            elif isinstance(b, numbers.Real):
                # a() - B -> -B + a()
                return AddScalar3D(-(<double> b), <Function3D> a)
        elif isinstance(a, numbers.Real):
            if isinstance(b, Function3D):
                # A - b()
                return SubtractScalar3D(<double> a, <Function3D> b)
        return NotImplemented

    def __mul__(object a, object b):
        if isinstance(a, Function3D):
            if isinstance(b, Function3D):
                # a() * b()
                return MultiplyFunction3D(<Function3D> a, <Function3D> b)
            elif isinstance(b, numbers.Real):
                # a() * B -> B * a()
                return MultiplyScalar3D(<double> b, <Function3D> a)
        elif isinstance(a, numbers.Real):
            if isinstance(b, Function3D):
                # A * b()
                return MultiplyScalar3D(<double> a, <Function3D> b)
        return NotImplemented

    @cython.cdivision(True)
    def __truediv__(object a, object b):
        cdef double v
        if isinstance(a, Function3D):
            if isinstance(b, Function3D):
                # a() / b()
                return DivideFunction3D(<Function3D> a, <Function3D> b)
            elif isinstance(b, numbers.Real):
                # a() / B -> 1/B * a()
                v = <double> b
                if v == 0.0:
                    raise ZeroDivisionError("Scalar used as the denominator of the division is zero valued.")
                return MultiplyScalar3D(1/v, <Function3D> a)
        elif isinstance(a, numbers.Real):
            if isinstance(b, Function3D):
                # A * b()
                return DivideScalar3D(<double> a, <Function3D> b)
        return NotImplemented

    def __mod__(object a, object b):
        cdef double v
        if isinstance(a, Function3D):
            if isinstance(b, Function3D):
                # a() % b()
                return ModuloFunction3D(<Function3D> a, <Function3D> b)
            elif isinstance(b, numbers.Real):
                # a() % B
                v = <double> b
                if v == 0.0:
                    raise ZeroDivisionError("Scalar used as the divisor of the division is zero valued.")
                return ModuloFunctionScalar3D(<Function3D> a, v)
        elif isinstance(a, numbers.Real):
            if isinstance(b, Function3D):
                # A % b()
                return ModuloScalarFunction3D(<double> a, <Function3D> b)
        return NotImplemented

    def __neg__(self):
        return MultiplyScalar3D(-1, self)

    def __pow__(object a, object b, object c):
        if c is not None:
            # Optimised implementation of pow(a, b, c) not available: fall back
            # to general implementation
            return (a ** b) % c
        if isinstance(a, Function3D):
            if isinstance(b, Function3D):
                # a() ** b()
                return PowFunction3D(<Function3D> a, <Function3D> b)
            elif isinstance(b, numbers.Real):
                # a() ** b
                return PowFunctionScalar3D(<Function3D> a, <double> b)
        elif isinstance(a, numbers.Real):
            if isinstance(b, Function3D):
                # a ** b()
                return PowScalarFunction3D(<double> a, <Function3D> b)
        return NotImplemented


cdef class AddFunction3D(Function3D):
    """
    A Function3D class that implements the addition of the results of two Function3D objects: f1() + f2()

    This class is not intended to be used directly, but rather returned as the result of an __add__() call on a
    Function3D object.

    :param function1: A Function3D object.
    :param function2: A Function3D object.
    """

    def __init__(self, Function3D function1, Function3D function2):
        self._function1 = autowrap_function3d(function1)
        self._function2 = autowrap_function3d(function2)

    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        return self._function1.evaluate(x, y, z) + self._function2.evaluate(x, y, z)


cdef class SubtractFunction3D(Function3D):
    """
    A Function3D class that implements the subtraction of the results of two Function3D objects: f1() - f2()

    This class is not intended to be used directly, but rather returned as the result of a __sub__() call on a
    Function3D object.

    :param function1: A Function3D object.
    :param function2: A Function3D object.
    """

    def __init__(self, Function3D function1, Function3D function2):
        self._function1 = autowrap_function3d(function1)
        self._function2 = autowrap_function3d(function2)

    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        return self._function1.evaluate(x, y, z) - self._function2.evaluate(x, y, z)


cdef class MultiplyFunction3D(Function3D):
    """
    A Function3D class that implements the multiplication of the results of two Function3D objects: f1() * f2()

    This class is not intended to be used directly, but rather returned as the result of a __mul__() call on a
    Function3D object.

    :param function1: A Function3D object.
    :param function2: A Function3D object.
    """

    def __init__(self, function1, function2):
        self._function1 = autowrap_function3d(function1)
        self._function2 = autowrap_function3d(function2)

    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        return self._function1.evaluate(x, y, z) * self._function2.evaluate(x, y, z)


cdef class DivideFunction3D(Function3D):
    """
    A Function3D class that implements the division of the results of two Function3D objects: f1() / f2()

    This class is not intended to be used directly, but rather returned as the result of a __truediv__() call on a
    Function3D object.

    :param function1: A Function3D object.
    :param function2: A Function3D object.
    """

    def __init__(self, function1, function2):
        self._function1 = autowrap_function3d(function1)
        self._function2 = autowrap_function3d(function2)

    @cython.cdivision(True)
    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        cdef double denominator = self._function2.evaluate(x, y, z)
        if denominator == 0.0:
            raise ZeroDivisionError("Function used as the denominator of the division returned a zero value.")
        return self._function1.evaluate(x, y, z) / denominator


cdef class ModuloFunction3D(Function3D):
    """
    A Function3D class that implements the modulo of the results of two Function3D objects: f1() % f2()

    This class is not intended to be used directly, but rather returned as the result of a __mod__() call on a
    Function3D object.

    :param Function3D function1: A Function3D object.
    :param Function3D function2: A Function3D object.
    """
    def __init__(self, function1, function2):
        self._function1 = autowrap_function3d(function1)
        self._function2 = autowrap_function3d(function2)

    @cython.cdivision(True)
    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        cdef double divisor = self._function2.evaluate(x, y, z)
        if divisor == 0.0:
            raise ZeroDivisionError("Function used as the divisor of the modulo returned a zero value.")
        return self._function1.evaluate(x, y, z) % divisor


cdef class PowFunction3D(Function3D):
    """
    A Function3D class that implements the pow() operator on two Function3D objects.

    This class is not intended to be used directly, but rather returned as the result of a __pow__() call on a
    Function3D object.

    :param Function3D function1: A Function3D object.
    :param Function3D function2: A Function3D object.
    """
    def __init__(self, function1, function2):
        self._function1 = autowrap_function3d(function1)
        self._function2 = autowrap_function3d(function2)

    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        cdef double base, exponent
        base = self._function1.evaluate(x, y, z)
        exponent = self._function2.evaluate(x, y, z)
        if base < 0 and floor(exponent) != exponent:  # Would return a complex value rather than double
            raise ValueError("Negative base and non-integral exponent is not supported")
        if base == 0 and exponent < 0:
            raise ZeroDivisionError("0.0 cannot be raised to a negative power")
        return base ** exponent


cdef class AddScalar3D(Function3D):
    """
    A Function3D class that implements the addition of scalar and the result of a Function3D object: K + f()

    This class is not intended to be used directly, but rather returned as the result of an __add__() call on a
    Function3D object.

    :param value: A double value.
    :param function: A Function3D object.
    """

    def __init__(self, double value, Function3D function):
        self._value = value
        self._function = autowrap_function3d(function)

    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        return self._value + self._function.evaluate(x, y, z)


cdef class SubtractScalar3D(Function3D):
    """
    A Function3D class that implements the subtraction of scalar and the result of a Function3D object: K - f()

    This class is not intended to be used directly, but rather returned as the result of an __sub__() call on a
    Function3D object.

    :param value: A double value.
    :param function: A Function3D object.
    """

    def __init__(self, double value, Function3D function):
        self._value = value
        self._function = autowrap_function3d(function)

    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        return self._value - self._function.evaluate(x, y, z)


cdef class MultiplyScalar3D(Function3D):
    """
    A Function3D class that implements the multiplication of scalar and the result of a Function3D object: K * f()

    This class is not intended to be used directly, but rather returned as the result of an __mul__() call on a
    Function3D object.

    :param value: A double value.
    :param function: A Function3D object.
    """

    def __init__(self, double value, Function3D function):
        self._value = value
        self._function = autowrap_function3d(function)

    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        return self._value * self._function.evaluate(x, y, z)


cdef class DivideScalar3D(Function3D):
    """
    A Function3D class that implements the subtraction of scalar and the result of a Function3D object: K / f()

    This class is not intended to be used directly, but rather returned as the result of an __div__() call on a
    Function3D object.

    :param value: A double value.
    :param function: A Function3D object.
    """

    def __init__(self, double value, Function3D function):
        self._value = value
        self._function = autowrap_function3d(function)

    @cython.cdivision(True)
    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        cdef double denominator = self._function.evaluate(x, y, z)
        if denominator == 0.0:
            raise ZeroDivisionError("Function used as the denominator of the division returned a zero value.")
        return self._value / denominator


cdef class ModuloScalarFunction3D(Function3D):
    """
    A Function3D class that implements the modulo of scalar and the result of a Function3D object: K % f()

    This class is not intended to be used directly, but rather returned as the result of a __mod__() call on a
    Function3D object.

    :param float value: A double value.
    :param Function3D function: A Function3D object.
    """
    def __init__(self, double value, Function3D function):
        self._value = value
        self._function = autowrap_function3d(function)

    @cython.cdivision(True)
    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        cdef double divisor = self._function.evaluate(x, y, z)
        if divisor == 0.0:
            raise ZeroDivisionError("Function used as the divisor of the modulo returned a zero value.")
        return self._value % divisor


cdef class ModuloFunctionScalar3D(Function3D):
    """
    A Function3D class that implements the modulo of the result of a Function3D object and a scalar: f() % K

    This class is not intended to be used directly, but rather returned as the result of a __mod__() call on a
    Function3D object.

    :param Function3D function: A Function3D object.
    :param float value: A double value.
    """
    def __init__(self, Function3D function, double value):
        if value == 0:
            raise ValueError("Divisor cannot be zero")
        self._value = value
        self._function = autowrap_function3d(function)

    @cython.cdivision(True)
    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        return self._function.evaluate(x, y, z) % self._value


cdef class PowScalarFunction3D(Function3D):
    """
    A Function3D class that implements the pow of scalar and the result of a Function3D object: K ** f()

    This class is not intended to be used directly, but rather returned as the result of an __pow__() call on a
    Function3D object.

    :param float value: A double value.
    :param Function3D function: A Function3D object.
    """
    def __init__(self, double value, Function3D function):
        self._value = value
        self._function = autowrap_function3d(function)

    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        cdef double exponent = self._function.evaluate(x, y, z)
        if self._value < 0 and floor(exponent) != exponent:
            raise ValueError("Negative base and non-integral exponent is not supported")
        if self._value == 0 and exponent < 0:
            raise ZeroDivisionError("0.0 cannot be raised to a negative power")
        return self._value ** exponent


cdef class PowFunctionScalar3D(Function3D):
    """
    A Function3D class that implements the pow of the result of a Function3D object and a scalar: f() ** K

    This class is not intended to be used directly, but rather returned as the result of an __pow__() call on a
    Function3D object.

    :param Function3D function: A Function3D object.
    :param float value: A double value.
    """
    def __init__(self, Function3D function, double value):
        self._value = value
        self._function = autowrap_function3d(function)

    cdef double evaluate(self, double x, double y, double z) except? -1e999:
        cdef double base = self._function.evaluate(x, y, z)
        if base < 0 and floor(self._value) != self._value:
            raise ValueError("Negative base and non-integral exponent is not supported")
        if base == 0 and self._value < 0:
            raise ZeroDivisionError("0.0 cannot be raised to a negative power")
        return base ** self._value
