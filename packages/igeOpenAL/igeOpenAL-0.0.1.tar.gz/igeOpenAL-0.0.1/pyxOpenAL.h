#include <Python.h>
#include "OpenAL.h"

typedef struct {
	PyObject_HEAD
		OpenAL* sound;
} sound_obj;
