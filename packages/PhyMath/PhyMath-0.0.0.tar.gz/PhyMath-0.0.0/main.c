#include <stdio.h>
#include <math.h>
#include <complex.h>
#include <Python.h>

double gravitational_force(double m1, double m2, int r) {
    const double G = 6.67408e-11;
    return G * (m1 * m2) / (pow(r, 2));
}

double velocity(double speed_change, double time_change) {
    return speed_change / time_change;
}

double force(double mass, double acceleration) {
    return mass * acceleration;
}

double weight(double mass, double gravity) {
    return mass * gravity;
}

double static_friction(double coefficient, double mass) {
    return coefficient * mass * 9.8;
}

double kinetic_friction(double coeffiecient, double mass, double force) {
    double eq1 = coeffiecient * mass * 9.8;
    return force - eq1;
}

double centripetal_acceleration(double velocity, double radius) {
    return (pow(velocity, 2)) / radius;
}

double work(double force, double displacement, double angle) {
    return force * displacement * cos(30 / (180 / M_PI));
}

double potential_energy(double mass, double height) {
    return mass * height * 9.8;
}

static PyObject * gravitational_force_solve(PyObject *self, PyObject *args) {
    double m1, m2;
    int r;

    if(!PyArg_ParseTuple(args, "ddi", &m1, &m2, &r)) {
        return NULL;
    }

    double result = gravitational_force(m1, m2, r);
    return Py_BuildValue("d", result);
}
static PyObject * velocity_solve(PyObject *self, PyObject *args) {
    double speed_change, time_change;
    if(!PyArg_ParseTuple(args, "dd", &speed_change, &time_change)) {
        return NULL;
    }
    double result = velocity(speed_change, time_change);
    return Py_BuildValue("d", result);
}
static PyObject * force_solve(PyObject *self, PyObject *args) {
    double mass, acceleration;
    if(!PyArg_ParseTuple(args, "dd", &mass, &acceleration)) {
        return NULL;
    }
    double result = force(mass, acceleration);
    return Py_BuildValue("d", result);
}
static PyObject * weight_solve(PyObject *self, PyObject *args) {
    double mass, gravity;
    if(!PyArg_ParseTuple(args, "dd", &mass, &gravity)) {
        return NULL;
    }
    double result = weight(mass, gravity);
    return Py_BuildValue("d", result);
}
static PyObject * static_friction_solve(PyObject *self, PyObject *args) {
    double coeffecient, mass;
    if(!PyArg_ParseTuple(args, "dd", &coeffecient, &mass)) {
        return NULL;
    }

    double result = static_friction(coeffecient, mass);
    return Py_BuildValue("d", result);
}
static PyObject * kinetic_friction_solve(PyObject *self, PyObject *args) {
    double force, mass, coeffecient;
    if(!PyArg_ParseTuple(args, "ddd", &coeffecient, &mass, &force)) {
        return NULL;
    }
    double result = kinetic_friction(coeffecient, mass, force);
    return Py_BuildValue("d", result);
}
static PyObject * centripetal_acceleration_solve(PyObject *self, PyObject *args) {
    double velocity, radius;
    if(!PyArg_ParseTuple(args, "dd", &velocity, &radius)) {
        return NULL;
    }
    double result = centripetal_acceleration(velocity, radius);
    return Py_BuildValue("d", result);
}
static PyObject * work_solve(PyObject *self, PyObject *args) {
    double force, displacement, angle;
    if(!PyArg_ParseTuple(args, "ddd", &force, &displacement, &angle)) {
        return NULL;
    }
    double result = work(force, displacement, angle);
    return Py_BuildValue("d", result);
}
static PyObject * potential_energy_solve(PyObject *self, PyObject *args) {
    double mass, height;
    if(!PyArg_ParseTuple(args, "ddi", &mass, &height)) {
        return NULL;
    }
    double result = potential_energy(mass, height);
    return Py_BuildValue("d", result);
}


static PyMethodDef Methods[] = {
        {"gfsolve", gravitational_force_solve, METH_VARARGS, "Calculate gravitational force"},
        {"vsolve", velocity_solve, METH_VARARGS, "Calculate velocity"},
        {"fosolve", force_solve, METH_VARARGS, "Calculate force"},
        {"wesolve", weight_solve, METH_VARARGS, "Calculate weight"},
        {"sfricsolve", static_friction_solve, METH_VARARGS, "Calculate static friction"},
        {"kfricsolve", kinetic_friction_solve, METH_VARARGS, "Calculate kinetic friction"},
        {"caccsolve", centripetal_acceleration_solve, METH_VARARGS, "Calculate centripetal acceleration"},
        {"wosolve", work_solve, METH_VARARGS, "Calculate work exerted"},
        {"pgsolve", potential_energy_solve, METH_VARARGS, "Calculate potential energy"},
        {NULL, NULL, 0, NULL}
};

static struct PyModuleDef PhyMath = {
        PyModuleDef_HEAD_INIT,
        "PhyMath",
        "Physics Math library for python",
        -1,
        Methods
};

PyMODINIT_FUNC PyInit_PhyMath(void) {
    return PyModule_Create(&PhyMath);
}