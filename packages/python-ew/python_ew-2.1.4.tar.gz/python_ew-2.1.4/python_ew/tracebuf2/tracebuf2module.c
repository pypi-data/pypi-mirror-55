/* Python wrapper for reading and writing Earthwrom Tracebuf2 data into a ring

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. */

#include <stdio.h>
#include <stdlib.h>

#include <Python.h>
#include <trace_buf.h>

#include <ringwriter.h>
#include <ringreader.h>

#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

typedef struct{
    TRACE2_HEADER header;
    char samples[MAX_TRACEBUF_SIZ - sizeof(TRACE2_HEADER)];
} TRACE2_HEADER_AND_SAMPS;

static PyObject *ring_write(PyObject *self, PyObject *args, PyObject *kws)
{
    int pinno, nsamp;
    PyObject *sample_list;
    double starttime, endtime, samprate;
    char *sta, *net, *chan, *loc;
    char *version, *datatype, *quality, *pad, *ring, *module, *sequence;
    char *keywords[] = {
        "pinno",
        "nsamp",
        "starttime",
        "endtime",
        "samprate",
        "sta",
        "net",
        "chan",
        "loc",
        "version",
        "datatype",
        "quality",
        "pad",
        "samples",
        "ring",
        "module",
        "sequence",
        NULL
    };
    int parsed;

    parsed = PyArg_ParseTupleAndKeywords(args, kws, "iidddssssssssOsss", keywords, &pinno,
            &nsamp, &starttime, &endtime, &samprate, &sta, &net,
            &chan, &loc, &version, &datatype, &quality, &pad,
            &sample_list, &ring, &module, &sequence);

    if (!parsed) {
        printf("Tracebuf2: Wrong args! \n");
        return Py_BuildValue("");
    }

    else {
        int tracesize = sizeof(TRACE2_HEADER) + (sizeof(int) *nsamp);
        if (tracesize > MAX_TRACEBUF_SIZ) {
            printf("Tracebuf2: Message too long! \n");
            return Py_BuildValue("");
        }

        int i;
        int samples_int[nsamp];
        char *samples;
        for (i = 0; i < nsamp; i++) {
            int sample;

            PyArg_Parse(PyList_GetItem(sample_list, i), "i", &sample);
            samples_int[i] = sample;
        }

        samples = (char *) samples_int;

        char *raw_data;
        char *params[] = {ring, "TYPE_TRACEBUF2", module, sequence};
        TRACE2_HEADER trace_header;
        TRACE2_HEADER_AND_SAMPS trace_data;

        trace_header.pinno = pinno;
        trace_header.nsamp = nsamp;
        trace_header.starttime = starttime;
        trace_header.endtime = endtime;
        trace_header.samprate = samprate;

        strcpy(trace_header.sta, sta);
        strcpy(trace_header.net, net);
        strcpy(trace_header.chan, chan);
        strcpy(trace_header.loc, loc);
        strcpy(trace_header.datatype, datatype);
        strncpy(trace_header.version, version, 2);
        strncpy(trace_header.quality, quality, 2);
        strncpy(trace_header.pad, pad, 2);

        trace_data.header = trace_header;
        for (i = 0; i < sizeof(int) *nsamp; i++)
            trace_data.samples[i] = samples[i];

        raw_data = (char *) &trace_data;
        write_ring(raw_data, params, tracesize);

        return Py_BuildValue("");

    }
}

static PyObject *ring_read(PyObject *self, PyObject *args, PyObject *kws)
{
    int max_traces = -1;
    char *ring;
    char *module;
    char *sta = NULL;
    char *keywords[] = {"ring", "module", "max_traces", "sta", NULL};

    if (!PyArg_ParseTupleAndKeywords(args, kws, "ss|is", keywords, &ring, &module, &max_traces, &sta)) {
        printf("Tracebuf2: Wrong args! \n");
        return PyList_New(0);
    }

    char *params[] = {ring, "TYPE_TRACEBUF2", module};
    char **raw_data = NULL;
    int items = 0;
    PyObject *trace_list;

    raw_data = read_ring(params, MAX_TRACEBUF_SIZ, &items);
    trace_list = PyList_New(0);
    max_traces = max_traces == -1 ? items : max_traces;

    int k;
    int i = 0;
    int inserted = 0;

    /*i and items prevent accessing raw_data at a invalid
       index; inserted and max_traces prevent returning more
       items than asked */
    while (inserted < max_traces && i < items) {
        PyObject *sample_list;
        PyObject *trace;

        TRACE2_HEADER *trace_data;
        trace_data = (TRACE2_HEADER *) raw_data[i];

        int *long_data = (int *)(raw_data[i] + sizeof(TRACE2_HEADER));
        short *short_data = (short *)(raw_data[i] + sizeof(TRACE2_HEADER));

        i++;
        if (sta != NULL) {
            if(strcmp(trace_data->sta, sta) != 0)
                continue;
        }

        /*Let's Null terminate some strings to they are
           are passed to Python correctly */
        char version[3];
        char quality[3];

        strncpy((char *) &version[0], trace_data->version, 2);
        strncpy((char *) &quality[0], trace_data->quality, 2);

        version[2] = '\0';
        quality[2] = '\0';

        trace = Py_BuildValue("{s:i,s:i,s:d,s:d,s:d,s:s,s:s,s:s,s:s,s:s,s:s,s:s,s:s}",
                "pinno", trace_data->pinno, "nsamp", trace_data->nsamp,
                "starttime", trace_data->starttime, "endtime", trace_data->endtime,
                "samprate", trace_data->samprate, "sta", trace_data->sta,
                "net", trace_data->net, "chan", trace_data->chan, "loc", trace_data->loc,
                "version", version, "datatype", trace_data->datatype,
                "quality", quality, "pad", trace_data->pad);

        sample_list = PyList_New(trace_data->nsamp);

        if ((strcmp(trace_data->datatype, "s2") == 0) || (strcmp(trace_data->datatype, "i2") == 0)) {
            for (k = 0; k < trace_data->nsamp; k++ )
                PyList_SetItem(sample_list, k, Py_BuildValue("i", *(short_data + k)));
        }

        else if ((strcmp(trace_data->datatype, "s4") == 0) || (strcmp(trace_data->datatype, "i4") == 0)) {
            for (k = 0; k < trace_data->nsamp; k++)
                PyList_SetItem(sample_list, k, Py_BuildValue("i", *(long_data + k)));
        }

        PyDict_SetItem(trace, Py_BuildValue("s", "samples"), sample_list);
        PyList_Append(trace_list, trace);
        inserted++;
    }
    free(raw_data);
    return trace_list;
}

// Module initialization

struct module_state {
    PyObject *error;
};

#if PY_MAJOR_VERSION >= 3
#define GETSTATE(m) ((struct module_state*)PyModule_GetState(m))
#else
#define GETSTATE(m) (&_state)
static struct module_state _state;
#endif

static PyObject *
error_out(PyObject *m) {
    struct module_state *st = GETSTATE(m);
    PyErr_SetString(st->error, "something bad happened");
    return NULL;
}

static PyMethodDef tracebuf2module_methods[] = {
    {"ring_write", (void*)ring_write, METH_VARARGS | METH_KEYWORDS, "Writes a TYPE_TRACEBUF2 message into the a ring."},
    {"ring_read", (void*)ring_read, METH_VARARGS | METH_KEYWORDS, "Reads TYPE_TRACEBUF2 messages from the ring."},
    {"error_out", (PyCFunction)error_out, METH_NOARGS, NULL},
    {NULL, NULL}
};

#if PY_MAJOR_VERSION >= 3

static int tracebuf2module_traverse(PyObject *m, visitproc visit, void *arg) {
    Py_VISIT(GETSTATE(m)->error);
    return 0;
}

static int tracebuf2module_clear(PyObject *m) {
    Py_CLEAR(GETSTATE(m)->error);
    return 0;
}


static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "tracebuf2module",
    NULL,
    sizeof(struct module_state),
    tracebuf2module_methods,
    NULL,
    tracebuf2module_traverse,
    tracebuf2module_clear,
    NULL
};

#define INITERROR return NULL

    PyMODINIT_FUNC
PyInit_tracebuf2module(void)

#else
#define INITERROR return

    void
inittracebuf2module(void)
#endif
{
#if PY_MAJOR_VERSION >= 3
    PyObject *module = PyModule_Create(&moduledef);
#else
    PyObject *module = Py_InitModule("tracebuf2module", tracebuf2module_methods);
#endif

    if (module == NULL)
        INITERROR;
    struct module_state *st = GETSTATE(module);

    st->error = PyErr_NewException("tracebuf2module.Error", NULL, NULL);
    if (st->error == NULL) {
        Py_DECREF(module);
        INITERROR;
    }

#if PY_MAJOR_VERSION >= 3
    return module;
#endif
}
