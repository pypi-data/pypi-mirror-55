"""C Extension module to test all aspects of PEP-3118.
Written by Stefan Krah."""

__all__ = (
    'ndarray', 'staticarray',
    'slice_indices', 'get_pointer', 'get_sizeof_void_p', 'get_contiguous',
    'py_buffer_to_contiguous', 'is_contiguous', 'cmp_contig',

    'ND_MAX_NDIM', 'ND_VAREXPORT', 'ND_WRITABLE', 'ND_FORTRAN', 'ND_SCALAR',
    'ND_PIL', 'ND_GETBUF_FAIL', 'ND_GETBUF_UNDEFINED', 'ND_REDIRECT',

    'PyBUF_SIMPLE', 'PyBUF_WRITABLE', 'PyBUF_FORMAT', 'PyBUF_ND',
    'PyBUF_STRIDES', 'PyBUF_INDIRECT', 'PyBUF_C_CONTIGUOUS',
    'PyBUF_F_CONTIGUOUS', 'PyBUF_ANY_CONTIGUOUS', 'PyBUF_FULL',
    'PyBUF_FULL_RO', 'PyBUF_RECORDS', 'PyBUF_RECORDS_RO', 'PyBUF_STRIDED',
    'PyBUF_STRIDED_RO', 'PyBUF_CONTIG', 'PyBUF_CONTIG_RO',
    'PyBUF_READ', 'PyBUF_WRITE',
)

#define PY_SSIZE_T_CLEAN

import struct as structmodule

from memorybuffer import Py_buffer, Buffer

Struct   = structmodule.Struct
calcsize = structmodule.calcsize

# cache simple format string
_simple_format = u"B"

#define SIMPLE_FORMAT(fmt) (fmt == NULL or strcmp(fmt, "B") == 0)
#define FIX_FORMAT(fmt)    (fmt == NULL ? "B" : fmt)


/**************************************************************************/
/*                             NDArray Object                             */
/**************************************************************************/

_

#define NDArray_Check(v) (Py_TYPE(v) == ndarray)

#define CHECK_LIST_OR_TUPLE(v) \
    if (!PyList_Check(v) and !PyTuple_Check(v)) { \
        PyErr_SetString(PyExc_TypeError,         \
            #v " must be a list or a tuple");    \
        return NULL;                             \
    }                                            \

#define PyMem_XFree(v) do { if (v) PyMem_Free(v); } while (0)

# Maximum number of dimensions.
ND_MAX_NDIM = (2 * PyBUF_MAX_NDIM)

/* Check for the presence of suboffsets in the first dimension. */
#define HAVE_PTR(suboffsets) (suboffsets and suboffsets[0] >= 0)
/* Adjust ptr if suboffsets are present. */
#define ADJUST_PTR(ptr, suboffsets) (HAVE_PTR(suboffsets) ? *((char**)ptr) + suboffsets[0] : ptr)

# Default: NumPy style (strides), read-only, no var-export, C-style layout
ND_DEFAULT          = 0x000
# User configurable flags for the ndarray
ND_VAREXPORT        = 0x001   # change layout while buffers are exported
# User configurable flags for each base buffer
ND_WRITABLE         = 0x002   # mark base buffer as writable
ND_FORTRAN          = 0x004   # Fortran contiguous layout
ND_SCALAR           = 0x008   # scalar: ndim = 0
ND_PIL              = 0x010   # convert to PIL-style array (suboffsets)
ND_REDIRECT         = 0x020   # redirect buffer requests
ND_GETBUF_FAIL      = 0x040   # trigger getbuffer failure
ND_GETBUF_UNDEFINED = 0x080   # undefined view.obj
# Internal flags for the base buffer
ND_C                = 0x100   # C contiguous layout (default)
ND_OWN_ARRAYS       = 0x200   # consumer owns arrays

/* ndarray properties */
#define ND_IS_CONSUMER(nd) (((ndarray *)nd)->head == &((ndarray *)nd)->staticbuf)

# ndbuf->flags properties
ND_C_CONTIGUOUS       = lambda flags: bool(flags & (ND_SCALAR | ND_C))
ND_FORTRAN_CONTIGUOUS = lambda flags: bool(flags & (ND_SCALAR | ND_FORTRAN))
ND_ANY_CONTIGUOUS     = lambda flags: bool(flags & (ND_SCALAR | ND_C | ND_FORTRAN))

# getbuffer() requests
REQ_INDIRECT       = lambda flags: (flags & PyBUF_INDIRECT)       == PyBUF_INDIRECT
REQ_C_CONTIGUOUS   = lambda flags: (flags & PyBUF_C_CONTIGUOUS)   == PyBUF_C_CONTIGUOUS
REQ_F_CONTIGUOUS   = lambda flags: (flags & PyBUF_F_CONTIGUOUS)   == PyBUF_F_CONTIGUOUS
REQ_ANY_CONTIGUOUS = lambda flags: (flags & PyBUF_ANY_CONTIGUOUS) == PyBUF_ANY_CONTIGUOUS
REQ_STRIDES        = lambda flags: (flags & PyBUF_STRIDES)        == PyBUF_STRIDES
REQ_SHAPE          = lambda flags: (flags & PyBUF_ND)             == PyBUF_ND
REQ_WRITABLE       = lambda flags:  flags & PyBUF_WRITABLE
REQ_FORMAT         = lambda flags:  flags & PyBUF_FORMAT


class ndbuf_t:

    """Single node of a list of base buffers. The list is needed to implement
       changes in memory layout while exported buffers are active."""

    ndbuf_t *next;
    ndbuf_t *prev;
    Py_ssize_t len;     # length of data
    Py_ssize_t offset;  # start of the array relative to data
    char *data;         # raw data
    int flags;          # capabilities of the base buffer
    Py_ssize_t exports; # number of exports
    Py_buffer base;     # base buffer

    /****************************************************************************/
    /*                            Initialize ndbuf                              */
    /****************************************************************************/

    /*
       State of a new ndbuf during initialization. 'OK' means that initialization
       is complete. 'PTR' means that a pointer has been initialized, but the
       state of the memory is still undefined and ndbuf->offset is disregarded.

      +-----------------+-----------+-------------+----------------+
      |                 | ndbuf_new | init_simple | init_structure |
      +-----------------+-----------+-------------+----------------+
      | next            | OK (NULL) |     OK      |       OK       |
      +-----------------+-----------+-------------+----------------+
      | prev            | OK (NULL) |     OK      |       OK       |
      +-----------------+-----------+-------------+----------------+
      | len             |    OK     |     OK      |       OK       |
      +-----------------+-----------+-------------+----------------+
      | offset          |    OK     |     OK      |       OK       |
      +-----------------+-----------+-------------+----------------+
      | data            |    PTR    |     OK      |       OK       |
      +-----------------+-----------+-------------+----------------+
      | flags           |    user   |    user     |       OK       |
      +-----------------+-----------+-------------+----------------+
      | exports         |   OK (0)  |     OK      |       OK       |
      +-----------------+-----------+-------------+----------------+
      | base.obj        | OK (NULL) |     OK      |       OK       |
      +-----------------+-----------+-------------+----------------+
      | base.buf        |    PTR    |     PTR     |       OK       |
      +-----------------+-----------+-------------+----------------+
      | base.len        | len(data) |  len(data)  |       OK       |
      +-----------------+-----------+-------------+----------------+
      | base.itemsize   |     1     |     OK      |       OK       |
      +-----------------+-----------+-------------+----------------+
      | base.readonly   |     0     |     OK      |       OK       |
      +-----------------+-----------+-------------+----------------+
      | base.format     |    NULL   |     OK      |       OK       |
      +-----------------+-----------+-------------+----------------+
      | base.ndim       |     1     |      1      |       OK       |
      +-----------------+-----------+-------------+----------------+
      | base.shape      |    NULL   |    NULL     |       OK       |
      +-----------------+-----------+-------------+----------------+
      | base.strides    |    NULL   |    NULL     |       OK       |
      +-----------------+-----------+-------------+----------------+
      | base.suboffsets |    NULL   |    NULL     |       OK       |
      +-----------------+-----------+-------------+----------------+
      | base.internal   |    OK     |    OK       |       OK       |
      +-----------------+-----------+-------------+----------------+
    */

    @classmethod
    ndbuf_t* ndbuf_new(cls, Py_ssize_t nitems, Py_ssize_t itemsize, Py_ssize_t offset, int flags):

        Py_buffer *base;
        Py_ssize_t len;

        len = nitems * itemsize
        if offset % itemsize:
            raise ValueError("offset must be a multiple of itemsize")

        if offset < 0 or offset + itemsize > len:
            raise ValueError("offset out of bounds")

        self = PyMem_Malloc(sizeof ndbuf_t)  # ndbuf_t*
        if self == NULL:
            raise PyErr_NoMemory()
        self.next    = NULL;
        self.prev    = NULL;
        self.len     = len;
        self.offset  = offset;
        self.data    = PyMem_Malloc(len);
        if self.data == NULL:
            PyMem_Free(self)
            raise PyErr_NoMemory()
        self.flags   = flags;
        self.exports = 0;

        base = self.base
        base.obj        = NULL;
        base.buf        = self.data;
        base.len        = len;
        base.itemsize   = 1;
        base.readonly   = 0;
        base.format     = NULL;
        base.ndim       = 1;
        base.shape      = NULL;
        base.strides    = NULL;
        base.suboffsets = NULL;
        base.internal   = self

        return self

    def free(self):

        base = self.base  # Py_buffer

        PyMem_XFree(self.data)
        PyMem_XFree(base.format)
        PyMem_XFree(base.shape)
        PyMem_XFree(base.strides)
        PyMem_XFree(base.suboffsets)

        PyMem_Free(self)

    @classmethod
    def init_ndbuf(cls,
                   PyObject *items, PyObject *shape, PyObject *strides,
                   Py_ssize_t offset, PyObject *format, int flags): # -> ndbuf_t

        Py_ssize_t ndim;
        Py_ssize_t nitems;
        Py_ssize_t itemsize;

        # ndim = len(shape)
        CHECK_LIST_OR_TUPLE(shape)

        ndim = PySequence_Fast_GET_SIZE(shape);
        if ndim > ND_MAX_NDIM:
            raise ValueError("ndim must not exceed %d" % ND_MAX_NDIM)

        # len(strides) = len(shape)
        if strides:
            CHECK_LIST_OR_TUPLE(strides)
            if PySequence_Fast_GET_SIZE(strides) == 0:
                strides = NULL;
            elif flags & ND_FORTRAN:
                raise TypeError("ND_FORTRAN cannot be used together with strides")
            elif PySequence_Fast_GET_SIZE(strides) != ndim:
                raise ValueError("len(shape) != len(strides)")

        # itemsize
        itemsize = _get_itemsize(format)
        if itemsize == 0:
            raise ValueError("itemsize must not be zero")

        # convert scalar to list
        if ndim == 0:
            items = Py_BuildValue("(O)", items);
            if (items == NULL)
                return NULL;
        else:
            CHECK_LIST_OR_TUPLE(items)
            Py_INCREF(items);

        try:
            # number of items
            nitems = PySequence_Fast_GET_SIZE(items)
            if nitems == 0:
                raise ValueError("initializer list or tuple must not be empty")

            self = ndbuf_t.ndbuf_new(nitems, itemsize, offset, flags)  # ndbuf_t

            if self.init_simple(items, format, itemsize) < 0:
                self.free()
                return NULL;

            if self.init_structure(shape, strides, ndim) < 0:
                self.free()
                return NULL;
        finally:
            Py_DECREF(items);

        return self

    int init_simple(self, PyObject *items, PyObject *format,  Py_ssize_t itemsize):

        base = self.base  # Py_buffer

        mview = PyMemoryView_FromBuffer(ct.byref(base))  # PyObject*
        if (mview == NULL):
            return -1;

        ret = pack_from_list(mview, items, format, itemsize)  # int
        del mview
        if ret < 0:
            return -1;

        base.readonly = not (self.flags & ND_WRITABLE)
        base.itemsize = itemsize
        base.format   = _get_format(format)

        return 0

    int init_structure(self, PyObject *shape, PyObject *strides, Py_ssize_t ndim):

        Py_buffer *base = &self.base;

        base->ndim = (int)ndim;
        if ndim == 0:
            if self.flags & ND_PIL:
                raise TypeError("ndim = 0 cannot be used in conjunction with ND_PIL")
                return -1;
            self.flags |= (ND_SCALAR | ND_C | ND_FORTRAN)
            return 0

        # shape
        base->shape = seq_as_ssize_array(shape, ndim, 1)
        if base->shape == NULL:
            return -1;

        # strides
        if strides:
            base->strides = seq_as_ssize_array(strides, ndim, 0)
            if base->strides == NULL:
                return -1;
        else:
            try:
                base->strides = self.strides_from_shape(self.flags)
            except:
                base->strides = NULL
                return -1;

        try:
            _verify_structure(base->len, base->itemsize, self.offset,
                              base->shape, base->strides, ndim)
        except:
            return -1;

        # buf
        base->buf = self.data + self.offset

        # len
        _init_len(base)

        # ndbuf_t.flags
        if PyBuffer_IsContiguous(base, 'C'):
            self.flags |= ND_C
        if PyBuffer_IsContiguous(base, 'F'):
            self.flags |= ND_FORTRAN

        # convert numpy array to suboffset representation
        if self.flags & ND_PIL:
            # modifies base->buf, base->strides and base->suboffsets
            return self.init_suboffsets()

        return 0

    def init_flags(self):

        if self.base.ndim == 0:
            self.flags |= ND_SCALAR
        if self.base.suboffsets:
            self.flags |= ND_PIL
        if PyBuffer_IsContiguous(ct.byref(self.base), 'C'):
            self.flags |= ND_C
        if PyBuffer_IsContiguous(ct.byref(self.base), 'F'):
            self.flags |= ND_FORTRAN

    int init_suboffsets(self):

        /*
           Convert a NumPy-style array to an array using suboffsets to stride in
           the first dimension. Requirements: ndim > 0.

           Contiguous example
           ==================

             Input:
             ------
               shape      = {2, 2, 3};
               strides    = {6, 3, 1};
               suboffsets = NULL;
               data       = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
               buf        = &data[0]

             Output:
             -------
               shape      = {2, 2, 3};
               strides    = {sizeof(char *), 3, 1};
               suboffsets = {0, -1, -1};
               data       = {p1, p2, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
                             |   |   ^                 ^
                             `---'---'                 |
                                 |                     |
                                 `---------------------'
               buf        = &data[0]

             So, in the example the input resembles the three-dimensional array
             char v[2][2][3], while the output resembles an array of two pointers
             to two-dimensional arrays: char (*v[2])[2][3].


           Non-contiguous example:
           =======================

             Input (with offset and negative strides):
             -----------------------------------------
               shape      = {2, 2, 3};
               strides    = {-6, 3, -1};
               offset     = 8
               suboffsets = NULL;
               data       = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};

             Output:
             -------
               shape      = {2, 2, 3};
               strides    = {-sizeof(char *), 3, -1};
               suboffsets = {2, -1, -1};
               newdata    = {p1, p2, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11};
                             |   |   ^     ^           ^     ^
                             `---'---'     |           |     `- p2+suboffsets[0]
                                 |         `-----------|--- p1+suboffsets[0]
                                 `---------------------'
               buf        = &newdata[1]  # striding backwards over the pointers.

             suboffsets[0] is the same as the offset that one would specify if
             the two {2, 3} subarrays were created directly, hence the name.
        */

        Py_buffer *base = &self.base;
        Py_ssize_t start, step;
        Py_ssize_t imin, suboffset0;
        Py_ssize_t addsize;
        Py_ssize_t n;
        char *data;

        assert base->ndim > 0
        assert base->suboffsets == NULL

        # Allocate new data with additional space for shape[0] pointers.
        addsize = base->shape[0] * (sizeof (char *));

        # Align array start to a multiple of 8.
        addsize = 8 * ((addsize + 7) / 8);

        data = PyMem_Malloc(self.len + addsize);
        if (data == NULL):
            raise PyErr_NoMemory()
            return -1;

        memcpy(data + addsize, self.data, self.len);

        PyMem_Free(self.data);
        self.data = data;
        self.len += addsize;
        base->buf = self.data;

        # imin: minimum index of the input array relative to ndbuf->offset.
        # suboffset0: offset for each sub-array of the output. This is the
        #             same as calculating -imin' for a sub-array of ndim-1.
        imin = suboffset0 = 0
        for (n = 0; n < base->ndim; n++):
            if base->shape[n] == 0:
                break
            if base->strides[n] <= 0:
                Py_ssize_t x = (base->shape[n] - 1) * base->strides[n]
                imin += x
                suboffset0 += -x if n >= 1 else 0

        # Initialize the array of pointers to the sub-arrays.
        start = addsize + self.offset + imin
        step  = -base->strides[0] if base->strides[0] < 0 else base->strides[0]

        for (n = 0; n < base->shape[0]; n++):
            ((char **)base->buf)[n] = (char *)base->buf + start + n*step;

        # Initialize suboffsets.
        base->suboffsets = PyMem_Malloc(base->ndim * (sizeof *base->suboffsets));
        if (base->suboffsets == NULL):
            raise PyErr_NoMemory()
            return -1;
        base->suboffsets[0] = suboffset0;
        for (n = 1; n < base->ndim; n++)
            base->suboffsets[n] = -1

        # Adjust strides for the first (zeroth) dimension.
        if base->strides[0] >= 0:
            base->strides[0] = sizeof(char *)
        else:
            # Striding backwards.
            base->strides[0] = -(Py_ssize_t)sizeof(char *)
            if base->shape[0] > 0:
                base->buf = (char *)base->buf + (base->shape[0]-1) * sizeof(char *)

        self.flags &= ~(ND_C|ND_FORTRAN)
        self.offset = 0

        return 0;

    Py_ssize_t * ndbuf_t.strides_from_shape(self, int flags):

        base = self.base  # Py_buffer

        Py_ssize_t *s, i;

        s = PyMem_Malloc(base.ndim * (sizeof *s));
        if (s == NULL):
            raise PyErr_NoMemory()

        if flags & ND_FORTRAN:
            s[0] = base.itemsize;
            for (i = 1; i < base.ndim; i++):
                s[i] = s[i-1] * base.shape[i-1]
        else:
            s[base.ndim-1] = base.itemsize;
            for (i = base.ndim-2; i >= 0; i--):
                s[i] = s[i+1] * base.shape[i+1]

        return s


def _verify_structure(Py_ssize_t len, Py_ssize_t itemsize, Py_ssize_t offset,
                      const Py_ssize_t *shape, const Py_ssize_t *strides,
                      Py_ssize_t ndim):

    """Bounds check:

      len := complete length of allocated memory
      offset := start of the array

      A single array element is indexed by:

        i = indices[0] * strides[0] + indices[1] * strides[1] + ...

      imin is reached when all indices[n] combined with positive strides are 0
      and all indices combined with negative strides are shape[n]-1, which is
      the maximum index for the nth dimension.

      imax is reached when all indices[n] combined with negative strides are 0
      and all indices combined with positive strides are shape[n]-1.
    """

    assert ndim >= 0

    if ndim == 0 and (offset < 0 or offset + itemsize > len):
        raise ValueError("invalid combination of buffer, shape and strides")

    for n in range(ndim):
        if strides[n] % itemsize:
            raise ValueError("strides must be a multiple of itemsize")

    for n in range(ndim):
        if shape[n] == 0:
            return

    imin = imax = 0
    for n in range(ndim):
        if strides[n] <= 0:
            imin += (shape[n] - 1) * strides[n]
        else
            imax += (shape[n] - 1) * strides[n]

    if imin + offset < 0 or imax + offset + itemsize > len:
        raise ValueError("invalid combination of buffer, shape and strides")


class ndarray(object):

    def ndarray.__new__(cls, *args, **kwargs):

        self = PyObject_New(ndarray, ndarray)
        self.flags     = 0          # int     # ndarray flags
        self.staticbuf = ndbuf_t()  # ndbuf_t # static buffer for re-exporting mode
        self.head      = NULL       # ndbuf_t # currently active base buffer
        return self

    def __del__(self):

        if self.head:
            if ND_IS_CONSUMER(self):
                base = self.head.base  # Py_buffer
                if self.head.flags & ND_OWN_ARRAYS:
                    PyMem_XFree(base.shape)
                    PyMem_XFree(base.strides)
                    PyMem_XFree(base.suboffsets)
                PyBuffer_Release(ct.byref(base))
            else:
                while self.head:
                    self._ndbuf_pop()

    int _init_staticbuf(self, PyObject *exporter, int flags):

        base = self.staticbuf.base  # Py_buffer

        if PyObject_GetBuffer(exporter, ct.byref(base), flags) < 0:
            return -1;

        self.head = &self.staticbuf;

        self.head->next   = NULL;
        self.head->prev   = NULL;
        self.head->len    = -1;
        self.head->offset = -1;
        self.head->data   = NULL;

        self.head->flags   = 0 if base.readonly else ND_WRITABLE
        self.head->exports = 0

    def _ndbuf_push(self, ndbuf_t elt):

        elt.next = self.head
        if self.head:
            self.head->prev = elt
        self.head = elt
        elt.prev = NULL

    def _ndbuf_pop(self):

        self._ndbuf_delete(self.head)

    def _ndbuf_delete(self, ndbuf_t elt):

        if elt.prev:
            elt.prev->next = elt.next
        else:
            self.head = elt.next

        if elt.next:
            elt.next->prev = elt.prev

        elt.free()


/****************************************************************************/
/*                          Buffer/List conversions                         */
/****************************************************************************/

/* Get number of members in a struct: see issue #12740 */
typedef struct {
    PyObject_HEAD
    Py_ssize_t s_size;
    Py_ssize_t s_len;
} PyPartialStructObject;


static Py_ssize_t get_nmemb(PyObject *s):
{
    return ((PyPartialStructObject *)s)->s_len;
}


static int pack_from_list(PyObject *obj, PyObject *items, PyObject *format, Py_ssize_t itemsize):
{
    # Pack all items into the buffer of 'obj'. The 'format' parameter must be
    # in struct module syntax. For standard C types, a single item is an integer.
    # For compound types, a single item is a tuple of integers.

    PyObject *structobj, *pack_into;
    PyObject *args, *offset;
    PyObject *item, *tmp;
    Py_ssize_t nitems; /* number of items */
    Py_ssize_t nmemb;  /* number of members in a single item */
    Py_ssize_t i, j;
    int ret = 0;

    assert PyObject_CheckBuffer(obj)
    assert PyList_Check(items) or PyTuple_Check(items)

    structobj = PyObject_CallFunctionObjArgs(Struct, format, NULL);
    if (structobj == NULL)
        return -1;

    nitems = PySequence_Fast_GET_SIZE(items);
    nmemb = get_nmemb(structobj);
    assert nmemb >= 1

    pack_into = structobj.pack_into
    if (pack_into == NULL)
    {
        Py_DECREF(structobj);
        return -1;
    }

    /* nmemb >= 1 */
    args = PyTuple_New(2 + nmemb);
    if (args == NULL)
    {
        Py_DECREF(pack_into);
        Py_DECREF(structobj);
        return -1;
    }

    offset = NULL;
    for (i = 0; i < nitems; i++)
    {
        /* Loop invariant: args[j] are borrowed references or NULL. */
        PyTuple_SET_ITEM(args, 0, obj);
        for (j = 1; j < 2+nmemb; j++)
            PyTuple_SET_ITEM(args, j, NULL);

        Py_XDECREF(offset);
        offset = PyLong_FromSsize_t(i*itemsize);
        if (offset == NULL) {
            ret = -1;
            break;
        }
        PyTuple_SET_ITEM(args, 1, offset);

        item = PySequence_Fast_GET_ITEM(items, i);
        if ((PyBytes_Check(item) or PyLong_Check(item) or PyFloat_Check(item)) and nmemb == 1) {
            PyTuple_SET_ITEM(args, 2, item);
        }
        elif ((PyList_Check(item) or PyTuple_Check(item)) and PySequence_Length(item) == nmemb):
        {
            for (j = 0; j < nmemb; j++) {
                tmp = PySequence_Fast_GET_ITEM(item, j);
                PyTuple_SET_ITEM(args, 2+j, tmp);
            }
        }
        else {
            raise ValueError("mismatch between initializer element and format string")
            ret = -1;
            break;
        }

        tmp = PyObject_CallObject(pack_into, args);
        if (tmp == NULL) {
            ret = -1;
            break;
        }
        Py_DECREF(tmp);
    }

    Py_INCREF(obj); /* args[0] */
    # args[1]: offset is either NULL or should be dealloc'd
    for (i = 2; i < 2+nmemb; i++):
    {
        tmp = PyTuple_GET_ITEM(args, i);
        Py_XINCREF(tmp);
    }
    Py_DECREF(args);

    Py_DECREF(pack_into);
    Py_DECREF(structobj);

    return ret;
}

static int pack_single(char *ptr, PyObject *item, const char *fmt, Py_ssize_t itemsize):
{
    /* Pack single element */

    PyObject *structobj = NULL, *pack_into = NULL, *args = NULL;
    PyObject *format = NULL, *mview = NULL, *zero = NULL;
    Py_ssize_t i, nmemb;
    int ret = -1;
    PyObject *x;

    if fmt == NULL:
        fmt = "B"

    format = PyUnicode_FromString(fmt);
    if (format == NULL)
        goto out;

    structobj = PyObject_CallFunctionObjArgs(Struct, format, NULL);
    if (structobj == NULL)
        goto out;

    nmemb = get_nmemb(structobj);
    assert nmemb >= 1

    mview = PyMemoryView_FromMemory(ptr, itemsize, PyBUF_WRITE);
    if (mview == NULL)
        goto out;

    zero = PyLong_FromLong(0);
    if (zero == NULL)
        goto out;

    pack_into = structobj.pack_into
    if (pack_into == NULL)
        goto out;

    args = PyTuple_New(2+nmemb);
    if (args == NULL)
        goto out;

    PyTuple_SET_ITEM(args, 0, mview);
    PyTuple_SET_ITEM(args, 1, zero);

    if (PyBytes_Check(item) or PyLong_Check(item) or PyFloat_Check(item)) and nmemb == 1:
         PyTuple_SET_ITEM(args, 2, item);
    elif (PyList_Check(item) or PyTuple_Check(item)) and PySequence_Length(item) == nmemb:
        for (i = 0; i < nmemb; i++):
            x = PySequence_Fast_GET_ITEM(item, i);
            PyTuple_SET_ITEM(args, 2+i, x);
    else:
        raise ValueError("mismatch between initializer element and format string")
        goto args_out;

    x = PyObject_CallObject(pack_into, args);
    if (x != NULL):
        Py_DECREF(x);
        ret = 0;

args_out:
    for (i = 0; i < 2+nmemb; i++)
        Py_XINCREF(PyTuple_GET_ITEM(args, i));
    Py_XDECREF(args);
out:
    Py_XDECREF(pack_into);
    Py_XDECREF(zero);
    Py_XDECREF(mview);
    Py_XDECREF(structobj);
    Py_XDECREF(format);
    return ret;
}


static void copy_rec(const Py_ssize_t *shape, Py_ssize_t ndim, Py_ssize_t itemsize,
                     char *dptr, const Py_ssize_t *dstrides, const Py_ssize_t *dsuboffsets,
                     char *sptr, const Py_ssize_t *sstrides, const Py_ssize_t *ssuboffsets,
                     char *mem):
    Py_ssize_t i;

    assert ndim >= 1

    if ndim == 1:
        if (!HAVE_PTR(dsuboffsets) and !HAVE_PTR(ssuboffsets) and
            dstrides[0] == itemsize and sstrides[0] == itemsize):
            memmove(dptr, sptr, shape[0] * itemsize);
        else:
            assert mem != NULL

            char *p;

            for (i=0, p=mem; i<shape[0]; p+=itemsize, sptr+=sstrides[0], i++):
                char *xsptr = ADJUST_PTR(sptr, ssuboffsets);
                memcpy(p, xsptr, itemsize);

            for (i=0, p=mem; i<shape[0]; p+=itemsize, dptr+=dstrides[0], i++):
                char *xdptr = ADJUST_PTR(dptr, dsuboffsets);
                memcpy(xdptr, p, itemsize);
    else:
        for (i = 0; i < shape[0]; dptr+=dstrides[0], sptr+=sstrides[0], i++):
            char *xdptr = ADJUST_PTR(dptr, dsuboffsets);
            char *xsptr = ADJUST_PTR(sptr, ssuboffsets);
            copy_rec(shape+1, ndim-1, itemsize,
                     xdptr, dstrides+1, dsuboffsets ? dsuboffsets+1 : NULL,
                     xsptr, sstrides+1, ssuboffsets ? ssuboffsets+1 : NULL,
                     mem)


@annotate(bool)
def _cmp_structure(Py_buffer *dest, Py_buffer *src):

    if (strcmp(FIX_FORMAT(dest->format), FIX_FORMAT(src->format)) != 0 or
        dest->itemsize != src->itemsize or
        dest->ndim     != src->ndim):
        return False

    for i in range(dest->ndim):
        if dest->shape[i] != src->shape[i]:
            return False
        if dest->shape[i] == 0:
            break

    return True


static PyObject * unpack_single(char *ptr, const char *fmt, Py_ssize_t itemsize):

    """Unpack single element"""

    PyObject *x, *mview;

    if (fmt == NULL):
        fmt = "B"
        itemsize = 1

    mview = PyMemoryView_FromMemory(ptr, itemsize, PyBUF_READ)
    if (mview == NULL):
        return NULL;

    x = PyObject_CallFunction(structmodule.unpack_from, "sO", fmt, mview)
    del mview
    if (x == NULL):
        return NULL;

    if len(x) == 1:
        return PyTuple_GET_ITEM(x, 0)

    return x;


static PyObject * unpack_rec(PyObject *unpack_from, char *ptr, PyObject *mview, char *item,
                             const Py_ssize_t *shape, const Py_ssize_t *strides,
                             const Py_ssize_t *suboffsets, Py_ssize_t ndim, Py_ssize_t itemsize):

    """Unpack a multi-dimensional matrix into a nested list.
    Return a scalar for ndim = 0."""

    PyObject *lst, *x;
    Py_ssize_t i;

    assert ndim >= 0
    assert shape   != NULL
    assert strides != NULL

    if (ndim == 0) {
        memcpy(item, ptr, itemsize);
        x = PyObject_CallFunctionObjArgs(unpack_from, mview, NULL);
        if (x == NULL)
            return NULL;
        if (PyTuple_GET_SIZE(x) == 1) {
            PyObject *tmp = PyTuple_GET_ITEM(x, 0);
            Py_INCREF(tmp);
            Py_DECREF(x);
            return tmp;
        }
        return x;
    }

    lst = PyList_New(shape[0]);
    if (lst == NULL)
        return NULL;

    for (i = 0; i < shape[0]; ptr+=strides[0], i++)
    {
        nextptr = ADJUST_PTR(ptr, suboffsets)  # char*

        x = unpack_rec(unpack_from, nextptr, mview, item,
                       shape+1, strides+1, suboffsets ? suboffsets+1 : NULL,
                       ndim-1, itemsize);
        if (x == NULL):
        {
            Py_DECREF(lst);
            return NULL;
        }

        PyList_SET_ITEM(lst, i, x);
    }

    return lst;


Py_ssize_t _get_itemsize(PyObject *format):

    Py_ssize_t itemsize;

    tmp = PyObject_CallFunctionObjArgs(calcsize, format, NULL) # PyObject*
    if tmp == NULL:
        # !!! tu wygenerowac exception !!!
        return -1;
    return PyLong_AsSsize_t(tmp)


char * _get_format(PyObject *format):

    tmp = PyUnicode_AsASCIIString(format)  # PyObject*
    if (tmp == NULL)
        return NULL;
    fmt = PyMem_Malloc(PyBytes_GET_SIZE(tmp)+1)  # char*
    if (fmt == NULL) {
        raise PyErr_NoMemory()
    }
    strcpy(fmt, PyBytes_AS_STRING(tmp));
    return fmt;


static Py_ssize_t * seq_as_ssize_array(PyObject *seq, Py_ssize_t len, int is_shape):

    Py_ssize_t *dest;
    Py_ssize_t x, i;

    # ndim = len <= ND_MAX_NDIM, so PyMem_New() is actually not needed.
    dest = PyMem_New(Py_ssize_t, len);
    if (dest == NULL):
        raise PyErr_NoMemory()

    for (i = 0; i < len; i++):

        PyObject *tmp = PySequence_Fast_GET_ITEM(seq, i);
        if not PyLong_Check(tmp):
            PyMem_Free(dest);
            raise ValueError("elements of %s must be integers" % (
                             "shape" if is_shape else "strides"))

        x = PyLong_AsSsize_t(tmp);
        if PyErr_Occurred():
            PyMem_Free(dest);
            return NULL;

        if is_shape and x < 0:
            PyMem_Free(dest);
            raise ValueError("elements of shape must be integers >= 0")

        dest[i] = x;

    return dest;


def _init_len(Py_buffer *base):

    base->len = 1
    for (i = 0; i < base->ndim; i++):
        base->len *= base->shape[i]
    base->len *= base->itemsize

PyBUF_UNUSED = 0x10000

    def int ndarray.__init__(self, PyObject *args, PyObject *kwds):

        static char *kwlist[] = {
            "obj", "shape", "strides", "offset", "format", "flags", "getbuf", NULL
        };
        PyObject *v = NULL;  /* initializer: scalar, list, tuple or base object */
        PyObject *shape = NULL;   /* size of each dimension */
        PyObject *strides = NULL; /* number of bytes to the next elt in each dim */
        Py_ssize_t offset = 0;            /* buffer offset */
        PyObject *format = _simple_format; /* struct module specifier: "B" */
        int flags = ND_DEFAULT;           /* base buffer and ndarray flags */

        int getbuf = PyBUF_UNUSED; /* re-exporter: getbuffer request flags */

        if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|OOnOii", kwlist,
                &v, &shape, &strides, &offset, &format, &flags, &getbuf))
            return -1;

        # ndarray is re-exporter
        if PyObject_CheckBuffer(v) and shape == NULL:

            if strides or offset or format != _simple_format or !(flags == ND_DEFAULT or flags == ND_REDIRECT):
                raise TypeError("construction from exporter object only takes 'obj', 'getbuf' "
                                "and 'flags' arguments")

            getbuf = PyBUF_FULL_RO if getbuf == PyBUF_UNUSED else getbuf

            if self._init_staticbuf(v, getbuf) < 0:
                return -1;

            self.head.init_flags()
            self.head.flags |= flags
            return

        # ndarray is the original base object.
        if getbuf != PyBUF_UNUSED:
            raise TypeError("getbuf argument only valid for construction from exporter "
                            "object")

        if shape == NULL:
            raise TypeError("shape is a required argument when constructing from "
                            "list, tuple or scalar")

        if flags & ND_VAREXPORT:
            self.flags |= ND_VAREXPORT
            flags &= ~ND_VAREXPORT

        # Initialize and push the first base buffer onto the linked list.
        self.ndarray._push_base(v, shape, strides, offset, format, flags)

    def ndarray.push(self, PyObject *args, PyObject *kwds):

        """Push an additional base onto the linked list."""

        static char *kwlist[] = {
            "items", "shape", "strides", "offset", "format", "flags", NULL
        };
        PyObject * items   = NULL;   /* initializer: scalar, list or tuple */
        PyObject * shape   = NULL;   /* size of each dimension */
        PyObject * strides = NULL; /* number of bytes to the next elt in each dim */
        Py_ssize_t offset  = 0;             /* buffer offset */
        PyObject * format  = _simple_format;  /* struct module specifier: "B" */
        int        flags   = ND_DEFAULT;            /* base buffer flags */

        if (!PyArg_ParseTupleAndKeywords(args, kwds, "OO|OnOi", kwlist,
                &items, &shape, &strides, &offset, &format, &flags))
            return NULL;

        if flags & ND_VAREXPORT:
            raise ValueError("ND_VAREXPORT flag can only be used during object creation")

        if ND_IS_CONSUMER(self):
            raise BufferError("structure of re-exporting object is immutable")

        if not (self.flags & ND_VAREXPORT) and self.head.exports > 0:
            raise BufferError("cannot change structure: %zd exported buffer%s" %
                              (self.head.exports, "" if self.head.exports == 1 else "s"))

        self.ndarray._push_base(items, shape, strides, offset, format, flags)

    def int ndarray._push_base(self, PyObject *items,
                               PyObject *shape, PyObject *strides,
                               Py_ssize_t offset, PyObject *format, int flags):

        # initialize and push a new base onto the linked list

        ndbuf = ndbuf_t.init_ndbuf(items, shape, strides, offset, format, flags)  # ndbuf_t
        self._ndbuf_push(ndbuf)

    def ndarray.pop(self):

        """Pop a base from the linked list (if possible)."""

        if ND_IS_CONSUMER(self):
            raise BufferError("structure of re-exporting object is immutable")

        if self.head.exports > 0:
            raise BufferError("cannot change structure: %zd exported buffer%s" %
                              (self.head.exports, "" if self.head.exports == 1 else "s"))

        if self.head->next == NULL:
            raise BufferError("list only has a single base")

        self._ndbuf_pop()

    def ndarray.ndarray_subscript(self, PyObject *key):

        ndarray *nd;
        ndbuf_t *ndbuf;

        Py_buffer *base = &self.head.base

        if base->ndim == 0:
            if PyTuple_Check(key) and PyTuple_GET_SIZE(key) == 0:
                return unpack_single(base->buf, base->format, base->itemsize)
            elif key == Py_Ellipsis:
                return self
            else:
                raise TypeError("invalid indexing of scalar")

        if PyIndex_Check(key):

            index = PyLong_AsSsize_t(key)
            if index == -1 and PyErr_Occurred():
                return NULL;
            return self.ndarray_item(index)

        else:
            nd = ndarray.__new__()

            # new ndarray is a consumer
            if nd._init_staticbuf(self, PyBUF_FULL_RO) < 0:
                return NULL;

            # copy shape, strides and suboffsets
            ndbuf = nd->head;
            base = &ndbuf->base;
            if copy_structure(base) < 0:
                return NULL;
            ndbuf->flags |= ND_OWN_ARRAYS;

            if PySlice_Check(key):

                # one-dimensional slice
                if init_slice(base, key, 0) < 0:
                    return NULL;

            elif PyTuple_Check(key):

                # multi-dimensional slice
                Py_ssize_t i, n;

                n = PyTuple_GET_SIZE(key);
                for (i = 0; i < n; i++):
                    item = PyTuple_GET_ITEM(key, i)
                    if not PySlice_Check(item):
                        raise TypeError("cannot index memory using \"%.200s\"" % item->ob_type->tp_name)
                    if init_slice(base, item, (int)i) < 0:
                        return NULL;

            else:
                raise TypeError("cannot index memory using \"%.200s\"" % key->ob_type->tp_name)

            _init_len(base)
            ndbuf.init_flags()

            return nd

    def ndarray.ndarray_item(self, Py_ssize_t index):

        ndbuf_t *ndbuf = self.head;
        base = ndbuf->base  # Py_buffer

        if base.ndim == 0:
            raise TypeError("invalid indexing of scalar")

        ptr = ptr_from_index(&base, index)  # char*
        if ptr == NULL:
            return NULL

        if base.ndim == 1:
            return unpack_single(ptr, base.format, base.itemsize)
        else:
            nd = ndarray.__new__()

            if nd._init_staticbuf(self, PyBUF_FULL_RO) < 0:
                return NULL;

            subview = nd.staticbuf.base  # Py_buffer

            subview.buf = ptr
            subview.len /= subview.shape[0]

            subview.ndim  -= 1
            subview.shape += 1
            if subview.strides:    subview.strides    += 1
            if subview.suboffsets: subview.suboffsets += 1

            nd.staticbuf.init_flags()

            return nd

    #**********************************************************************#
    #                              getbuffer                               #
    #**********************************************************************#

    def __getbuffer__(self, Py_buffer *view, int flags):

        ndbuf_t *ndbuf = self.head;
        Py_buffer *base = &ndbuf->base;
        int baseflags = ndbuf->flags;

        # redirect mode
        if base->obj != NULL and (baseflags & ND_REDIRECT):
            PyObject_GetBuffer(base->obj, view, flags)
            return

        # start with complete information
        *view = *base;
        view->obj = NULL

        # reconstruct format
        if view->format == NULL:
            view->format = "B"

        if (base->ndim != 0 and
            ((REQ_SHAPE(flags) and base->shape == NULL) or
             (REQ_STRIDES(flags) and base->strides == NULL))):
            # The ndarray is a re-exporter that has been created without full
            # information for testing purposes. In this particular case the
            # ndarray is not a PEP-3118 compliant buffer provider.
            raise BufferError("re-exporter does not provide format, shape or strides")

        if baseflags & ND_GETBUF_FAIL:
            if baseflags & ND_GETBUF_UNDEFINED:
                view->obj = (PyObject *)0x1; # wrong but permitted in <= 3.2
            raise BufferError("ND_GETBUF_FAIL: forced test exception")

        if REQ_WRITABLE(flags) and base->readonly:
            raise BufferError("ndarray is not writable")

        if not REQ_FORMAT(flags):
            # NULL indicates that the buffer's data type has been cast to 'B'.
            # view->itemsize is the _previous_ itemsize. If shape is present,
            # the equality product(shape) * itemsize = len still holds at this
            # point. The equality calcsize(format) = itemsize does _not_ hold
            # from here on!
            view->format = NULL

        if REQ_C_CONTIGUOUS(flags) and !ND_C_CONTIGUOUS(baseflags):
            raise BufferError("ndarray is not C-contiguous")

        if REQ_F_CONTIGUOUS(flags) and !ND_FORTRAN_CONTIGUOUS(baseflags):
            raise BufferError("ndarray is not Fortran contiguous")

        if REQ_ANY_CONTIGUOUS(flags) and !ND_ANY_CONTIGUOUS(baseflags):
            raise BufferError("ndarray is not contiguous")

        if not REQ_INDIRECT(flags) and (baseflags & ND_PIL):
            raise BufferError("ndarray cannot be represented without suboffsets")

        if not REQ_STRIDES(flags):
            if not ND_C_CONTIGUOUS(baseflags):
                raise BufferError("ndarray is not C-contiguous")
            view->strides = NULL

        if not REQ_SHAPE(flags):
            # PyBUF_SIMPLE or PyBUF_WRITABLE: at this point buf is C-contiguous,
            # so base->buf = ndbuf->data.
            if view->format != NULL:
                # PyBUF_SIMPLE|PyBUF_FORMAT and PyBUF_WRITABLE|PyBUF_FORMAT do
                # not make sense.
                raise BufferError("ndarray: cannot cast to unsigned bytes if the format flag "
                                  "is present")
            # product(shape) * itemsize = len and calcsize(format) = itemsize
            # do _not_ hold from here on!
            view->ndim  = 1
            view->shape = NULL

        # Ascertain that the new buffer has the same contiguity as the exporter
        if (ND_C_CONTIGUOUS(baseflags) != PyBuffer_IsContiguous(view, 'C') or
            # skip cast to 1-d
            (view->format != NULL and view->shape != NULL and
             ND_FORTRAN_CONTIGUOUS(baseflags) != PyBuffer_IsContiguous(view, 'F')) or
            # cast to 1-d
            (view->format == NULL and view->shape == NULL and
             not PyBuffer_IsContiguous(view, 'F'))):
            raise BufferError("ndarray: contiguity mismatch in getbuf()")

        view->obj = (PyObject *)self
        Py_INCREF(view->obj);
        self.head.exports += 1

    def __releasebuffer__(self, Py_buffer *view):

        if not ND_IS_CONSUMER(self):
            ndbuf_t *ndbuf = view->internal;
            ndbuf->exports -= 1
            if ndbuf->exports == 0 and ndbuf != self.head:
                self._ndbuf_delete(ndbuf)


/**************************************************************************/
/*                           indexing/slicing                             */
/**************************************************************************/

static char * ptr_from_index(Py_buffer *base, Py_ssize_t index):

    Py_ssize_t nitems; /* items in the first dimension */

    if base->shape:
        nitems = base->shape[0]
    else:
        assert base->ndim == 1 and SIMPLE_FORMAT(base->format)
        nitems = base->len

    if index < 0:
        index += nitems;
    if index < 0 or index >= nitems:
        raise IndexError("index out of bounds")
        return NULL;

    ptr = (char *)base->buf
    if base->strides == NULL:
         ptr += base->itemsize * index
    else:
         ptr += base->strides[0] * index

    ptr = ADJUST_PTR(ptr, base->suboffsets)  # char*
    return ptr


static int init_slice(Py_buffer *base, PyObject *key, int dim):

    /*
      For each dimension, we get valid (start, stop, step, slicelength) quadruples
      from PySlice_GetIndicesEx().

      Slicing NumPy arrays
      ====================

        A pointer to an element in a NumPy array is defined by:

          ptr = (char *)buf + indices[0] * strides[0] +
                              ... +
                              indices[ndim-1] * strides[ndim-1]

        Adjust buf:
        -----------
          Adding start[n] for each dimension effectively adds the constant:

            c = start[0] * strides[0] + ... + start[ndim-1] * strides[ndim-1]

          Therefore init_slice() adds all start[n] directly to buf.

        Adjust shape:
        -------------
          Obviously shape[n] = slicelength[n]

        Adjust strides:
        ---------------
          In the original array, the next element in a dimension is reached
          by adding strides[n] to the pointer. In the sliced array, elements
          may be skipped, so the next element is reached by adding:

            strides[n] * step[n]

      Slicing PIL arrays
      ==================

        Layout:
        -------
          In the first (zeroth) dimension, PIL arrays have an array of pointers
          to sub-arrays of ndim-1. Striding in the first dimension is done by
          getting the index of the nth pointer, dereference it and then add a
          suboffset to it. The arrays pointed to can best be seen a regular
          NumPy arrays.

        Adjust buf:
        -----------
          In the original array, buf points to a location (usually the start)
          in the array of pointers. For the sliced array, start[0] can be
          added to buf in the same manner as for NumPy arrays.

        Adjust suboffsets:
        ------------------
          Due to the dereferencing step in the addressing scheme, it is not
          possible to adjust buf for higher dimensions. Recall that the
          sub-arrays pointed to are regular NumPy arrays, so for each of
          those arrays adding start[n] effectively adds the constant:

            c = start[1] * strides[1] + ... + start[ndim-1] * strides[ndim-1]

          This constant is added to suboffsets[0]. suboffsets[0] in turn is
          added to each pointer right after dereferencing.

        Adjust shape and strides:
        -------------------------
          Shape and strides are not influenced by the dereferencing step, so
          they are adjusted in the same manner as for NumPy arrays.

      Multiple levels of suboffsets
      =============================

          For a construct like an array of pointers to array of pointers to
          sub-arrays of ndim-2:

            suboffsets[0] = start[1] * strides[1]
            suboffsets[1] = start[2] * strides[2] + ...
    */

    Py_ssize_t start, stop, step, slicelength;

    if (PySlice_Unpack(key, &start, &stop, &step) < 0):
        return -1;
    slicelength = PySlice_AdjustIndices(base->shape[dim], &start, &stop, step);

    if base->suboffsets == NULL or dim == 0:
        base->buf = (char *)base->buf + base->strides[dim] * start;
    else:
        Py_ssize_t n = dim - 1
        while n >= 0 and base->suboffsets[n] < 0: n -= 1
        if n < 0:
            # all suboffsets are negative
            base->buf = (char *)base->buf + base->strides[dim] * start;
        else:
            base->suboffsets[n] = base->suboffsets[n] + base->strides[dim] * start;

    base->shape[dim]   = slicelength;
    base->strides[dim] = base->strides[dim] * step;

    return 0;


static int copy_structure(Py_buffer *base):

    Py_ssize_t *shape = NULL, *strides = NULL, *suboffsets = NULL;
    Py_ssize_t i;

    shape = PyMem_Malloc(base->ndim * (sizeof *shape));
    strides = PyMem_Malloc(base->ndim * (sizeof *strides));
    if shape == NULL or strides == NULL:
        goto err_nomem;

    suboffsets = NULL;
    if (base->suboffsets) {
        suboffsets = PyMem_Malloc(base->ndim * (sizeof *suboffsets));
        if (suboffsets == NULL)
            goto err_nomem;
    }

    for (i = 0; i < base->ndim; i++) {
        shape[i] = base->shape[i];
        strides[i] = base->strides[i];
        if (suboffsets)
            suboffsets[i] = base->suboffsets[i];
    }

    base->shape = shape;
    base->strides = strides;
    base->suboffsets = suboffsets;

    return 0;

    err_nomem:

    PyMem_XFree(shape);
    PyMem_XFree(strides);
    PyMem_XFree(suboffsets);
    raise PyErr_NoMemory()
    return -1;


static int ndarray_ass_subscript(ndarray *self, PyObject *key, PyObject *value):

    ndarray *nd;

    src  = Py_buffer()
    dest = self.head.base  # Py_buffer

    char *ptr;
    Py_ssize_t index;
    int ret = -1;

    if dest.readonly:
        raise TypeError("ndarray is not writable")

    if value == NULL:
        raise TypeError("ndarray data cannot be deleted")

    if dest.ndim == 0:
        if key == Py_Ellipsis or (PyTuple_Check(key) and PyTuple_GET_SIZE(key) == 0):
            ptr = (char *)dest.buf;
            return pack_single(ptr, value, dest.format, dest.itemsize)
        else:
            raise TypeError("invalid indexing of scalar")

    if dest.ndim == 1 and PyIndex_Check(key):
        # rvalue must be a single item
        index = PyLong_AsSsize_t(key);
        if index == -1 and PyErr_Occurred():
            return -1;
        ptr = ptr_from_index(&dest, index)
        if ptr == NULL:
            return -1;
        return pack_single(ptr, value, dest.format, dest.itemsize)

    # rvalue must be an exporter
    if PyObject_GetBuffer(value, ct.byref(src), PyBUF_FULL_RO) == -1:
        return -1;
    try:
        nd = (ndarray *) self.ndarray_subscript(key)
        if (nd != NULL):
            dest = nd->head->base
            try:
                _copy_buffer(&dest, &src)
                ret = 0
            except:
                ret = -1
    finally:
        PyBuffer_Release(ct.byref(src))

    return ret;


def slice_indices(key, len):

    # PyObject *key;
    # Py_ssize_t len;
    #if (!PyArg_ParseTuple(args, "On", &key, &len))

    PyObject *tmp;

    if not PySlice_Check(key):
        raise TypeError("first argument must be a slice object")

    Py_ssize_t s[4]  # start, stop, step, slicelength
    if PySlice_Unpack(key, &s[0], &s[1], &s[2]) < 0:
        return NULL;
    s[3] = PySlice_AdjustIndices(len, &s[0], &s[1], s[2]);

    ret = []
    for (i = 0; i < 4; i++):
        tmp = PyLong_FromSsize_t(s[i]);
        if (tmp == NULL):
            Py_DECREF(ret);
            return NULL;
        PyTuple_SET_ITEM(ret, i, tmp);

    return tuple(ret)


static PyMappingMethods ndarray_as_mapping = {
    (binaryfunc)ndarray_subscript,        /* mp_subscript */
    (objobjargproc)ndarray_ass_subscript  /* mp_ass_subscript */
};

static PySequenceMethods ndarray_as_sequence = {
        (ssizeargfunc)ndarray_item,       /* sq_item */
};

    #**********************************************************************#
    #                                getters                               #
    #**********************************************************************#

    @property
    def ndarray.flags(self):

        return PyLong_FromLong(self.head.flags)

    @property
    def ndarray.offset(self):

        return PyLong_FromSsize_t(self.head->offset)

    @property
    def ndarray.obj(self):

        base = self.head.base  # Py_buffer
        return base.obj if base.obj != NULL else None

    @property
    def ndarray.nbytes(self):

        base = self.head.base  # Py_buffer
        return PyLong_FromSsize_t(base.len)

    @property
    def ndarray.readonly(self):

        base = self.head.base  # Py_buffer
        return PyLong_FromLong(base.readonly)

    @property
    def ndarray.itemsize(self):

        base = self.head.base  # Py_buffer
        return PyLong_FromSsize_t(base.itemsize)

    @property
    def ndarray.format(self):

        base = self.head.base  # Py_buffer
        fmt = base.format if base.format else ""  # char*
        return PyUnicode_FromString(fmt)

    @property
    def ndarray.ndim(self):

        base = self.head.base  # Py_buffer
        return PyLong_FromSsize_t(base.ndim)

    @property
    def ndarray.shape(self):

        base = self.head.base  # Py_buffer
        return _ssize_array_as_tuple(base.shape, base.ndim)

    @property
    def ndarray.strides(self):

        base = self.head.base  # Py_buffer
        return _ssize_array_as_tuple(base.strides, base.ndim)

    @property
    def ndarray.suboffsets(self):

        base = self.head.base  # Py_buffer
        return _ssize_array_as_tuple(base.suboffsets, base.ndim)

    @property
    def ndarray.c_contiguous(self):

        ret = PyBuffer_IsContiguous(ct.byref(self.head.base), 'C')  # int

        if ret != ND_C_CONTIGUOUS(self.head.flags):
            raise RuntimeError("results from PyBuffer_IsContiguous() and flags differ")

        return bool(ret)

    @property
    def ndarray.f_contiguous(self):

        ret = PyBuffer_IsContiguous(ct.byref(self.head.base), 'F')  # int

        if ret != ND_FORTRAN_CONTIGUOUS(self.head.flags):
            raise RuntimeError("results from PyBuffer_IsContiguous() and flags differ")

        return bool(ret)

    @property
    def ndarray.contiguous(self):

        ret = PyBuffer_IsContiguous(ct.byref(self.head.base), 'A')  # int

        if ret != ND_ANY_CONTIGUOUS(self.head.flags):
            raise RuntimeError("results from PyBuffer_IsContiguous() and flags differ")

        return bool(ret)

    def ndarray.tolist(self):

        PyObject *structobj = NULL, *unpack_from = NULL;
        PyObject *lst = NULL, *mview = NULL;
        Py_buffer *base = &self.head.base
        Py_ssize_t* shape   = base->shape;
        Py_ssize_t* strides = base->strides;
        Py_ssize_t simple_shape[1];
        Py_ssize_t simple_strides[1];
        char *item = NULL;
        PyObject *format;
        char *fmt = base->format;

        base = self.head.base

        if fmt == NULL:
            raise ValueError("ndarray: tolist() does not support format=NULL, use "
                             "tobytes()")

        if shape == NULL:
            assert ND_C_CONTIGUOUS(self.head.flags)
            assert base.strides == NULL
            assert base.ndim <= 1
            shape = simple_shape
            shape[0] = base.len
            strides = simple_strides
            strides[0] = base.itemsize
        elif strides == NULL:
            assert ND_C_CONTIGUOUS(self.head.flags)
            strides = self.head.strides_from_shape(0)

        format = PyUnicode_FromString(fmt);
        if (format == NULL)
            goto out;

        structobj = PyObject_CallFunctionObjArgs(Struct, format, NULL);
        Py_DECREF(format);
        if (structobj == NULL)
            goto out;

        unpack_from = structobj.unpack_from
        if (unpack_from == NULL)
            goto out;

        item = PyMem_Malloc(base.itemsize);
        if (item == NULL):
            raise PyErr_NoMemory()
            goto out;

        mview = PyMemoryView_FromMemory(item, base.itemsize, PyBUF_WRITE);
        if (mview == NULL):
            goto out;

        lst = unpack_rec(unpack_from, base.buf, mview, item,
                         shape, strides, base.suboffsets,
                         base.ndim, base.itemsize)

        out:
        Py_XDECREF(mview);
        PyMem_XFree(item);
        Py_XDECREF(unpack_from);
        Py_XDECREF(structobj);
        if strides != base.strides and strides != simple_strides:
            PyMem_XFree(strides)

        return lst;

    def tobytes(self):

        ndbuf_t *ndbuf = ((ndarray *)self)->head;

        src  = ndbuf->base  # Py_buffer
        dest = Py_buffer()

        if ND_C_CONTIGUOUS(ndbuf->flags):
            return PyBytes_FromStringAndSize(src.buf, src.len)

        assert src.ndim > 0
        assert src.shape   != NULL
        assert src.strides != NULL

        mem = PyMem_Malloc(src.len)  # char*
        if mem == NULL:
            raise PyErr_NoMemory()

        try:
            dest = copy.copy(src)
            dest.buf        = mem;
            dest.suboffsets = NULL;
            dest.strides    = NULL
            dest.strides    = ndbuf.strides_from_shape(0)
            try:
                _copy_buffer(&dest, &src)
            except Exception as exc:
                PyMem_XFree(dest.strides)
                raise exc
            ret = PyBytes_FromStringAndSize(mem, src.len)
        finally:
            PyMem_Free(mem)

        PyMem_XFree(dest.strides)
        return ret

    def ndarray.add_suboffsets(self):

        """add redundant (negative) suboffsets for testing"""

        base = self.head.base  # Py_buffer

        if base.suboffsets != NULL:
            raise TypeError("cannot add suboffsets to PIL-style array")

        if base.strides == NULL:
            raise TypeError("cannot add suboffsets to array without strides")

        base.suboffsets = PyMem_Malloc(base.ndim * (sizeof *base.suboffsets))
        if base.suboffsets == NULL:
            raise PyErr_NoMemory()
            return NULL;

        for i in range(base.ndim):
            base.suboffsets[i] = -1

        self.head.flags &= ~(ND_C|ND_FORTRAN)

    def ndarray.memoryview_from_buffer(self):

        # Test PyMemoryView_FromBuffer(): return a memoryview from a static buffer.
        # Obviously this is fragile and only one such view may be active at any
        # time. Never use anything like this in real code!

        const ndarray *nd = (ndarray *)self;
        const Py_buffer *view = &nd->head->base;
        const ndbuf_t *ndbuf;

        static char* infobuf = NULL;

        static char       format[ND_MAX_NDIM+1];
        static Py_ssize_t shape[ND_MAX_NDIM];
        static Py_ssize_t strides[ND_MAX_NDIM];
        static Py_ssize_t suboffsets[ND_MAX_NDIM];
        static info = Py_buffer()

        char *p;

        if not ND_IS_CONSUMER(nd):
            ndbuf = nd->head  # self is ndarray/original exporter
        elif NDArray_Check(view->obj) and not ND_IS_CONSUMER(view->obj):
            # self is ndarray and consumer from ndarray/original exporter
            ndbuf = ((ndarray *)view->obj)->head;
        else:
            raise TypeError("memoryview_from_buffer(): ndarray must be original exporter or "
                            "consumer from ndarray/original exporter")

        info = copy.copy(*view)
        p = PyMem_Realloc(infobuf, ndbuf->len);
        if (p == NULL):
            PyMem_Free(infobuf);
            infobuf = NULL;
            raise PyErr_NoMemory()
        else:
            infobuf = p;

        # copy the complete raw data
        memcpy(infobuf, ndbuf->data, ndbuf->len);
        info.buf = infobuf + ((char *)view->buf - ndbuf->data);

        if view->format:
            if strlen(view->format) > ND_MAX_NDIM:
                raise TypeError("memoryview_from_buffer: format is limited to %d characters" % ND_MAX_NDIM)
            strcpy(format, view->format);
            info.format = format;

        if view->ndim > ND_MAX_NDIM:
            raise TypeError("memoryview_from_buffer: ndim is limited to %d" % ND_MAX_NDIM)

        if view->shape:
            memcpy(shape, view->shape, view->ndim * sizeof(Py_ssize_t));
            info.shape = shape;

        if view->strides:
            memcpy(strides, view->strides, view->ndim * sizeof(Py_ssize_t));
            info.strides = strides;

        if view->suboffsets:
            memcpy(suboffsets, view->suboffsets, view->ndim * sizeof(Py_ssize_t));
            info.suboffsets = suboffsets;

        return PyMemoryView_FromBuffer(&info)

    def __hash__(self):

        view = self.head.base  # Py_buffer

        if not view.readonly:
            raise ValueError("cannot hash writable ndarray object")

        if view.obj != NULL:
            if PyObject_Hash(view.obj) == -1:
                return -1;

        return PyObject_Hash(self.tobytes())


def _copy_buffer(Py_buffer *dest, Py_buffer *src):

    # Copy src to dest. Both buffers must have the same format, itemsize,
    # ndim and shape. Copying is atomic, the function never fails with
    # a partial copy.

    assert dest->ndim > 0

    if not _cmp_structure(dest, src):
        raise ValueError("ndarray assignment: lvalue and rvalue have different structures")

    mem = NULL  # char*
    if ((dest->suboffsets and dest->suboffsets[dest->ndim-1] >= 0) or
        (src->suboffsets  and src->suboffsets[src->ndim-1]   >= 0) or
        dest->strides[dest->ndim-1] != dest->itemsize or
        src->strides[src->ndim-1]   != src->itemsize):
        mem = PyMem_Malloc(dest->shape[dest->ndim-1] * dest->itemsize)
        if mem == NULL:
            raise PyErr_NoMemory()

    copy_rec(dest->shape, dest->ndim, dest->itemsize,
             dest->buf, dest->strides, dest->suboffsets,
             src->buf, src->strides, src->suboffsets,
             mem)

    PyMem_XFree(mem)


PyObject * _ssize_array_as_tuple(Py_ssize_t *array, Py_ssize_t len):
{
    PyObject *tuple, *x;
    Py_ssize_t i;

    if (array == NULL)
        return ()

    tuple = PyTuple_New(len);
    if (tuple == NULL)
        return NULL;

    for (i = 0; i < len; i++) {
        x = PyLong_FromSsize_t(array[i]);
        if (x == NULL) {
            Py_DECREF(tuple);
            return NULL;
        }
        PyTuple_SET_ITEM(tuple, i, x);
    }

    return tuple;


def get_pointer(bufobj, seq):

    # Get a single item from bufobj at the location specified by seq.
    # seq is a list or tuple of indices. The purpose of this function
    # is to check other functions against PyBuffer_GetPointer().

    view = Py_buffer()

    Py_ssize_t indices[ND_MAX_NDIM];
    Py_ssize_t i;
    void *ptr;

    CHECK_LIST_OR_TUPLE(seq)

    if PyObject_GetBuffer(bufobj, ct.byref(view), PyBUF_FULL_RO) < 0:
        return NULL;
    try:
        if view.ndim > ND_MAX_NDIM:
            raise ValueError("get_pointer(): ndim > %d" % ND_MAX_NDIM)

        if PySequence_Fast_GET_SIZE(seq) != view.ndim:
            raise ValueError("get_pointer(): len(indices) != ndim")

        for i in range(view.ndim):
            x = PySequence_Fast_GET_ITEM(seq, i)  # PyObject*
            indices[i] = PyLong_AsSsize_t(x);
            if PyErr_Occurred():
                return NULL;
            if indices[i] < 0 or indices[i] >= view.shape[i]:
                raise ValueError("get_pointer(): invalid index %zd at position %zd" %  (
                                 indices[i], i))

        ptr = PyBuffer_GetPointer(ct.byref(view), indices)
        ret = unpack_single(ptr, view.format, view.itemsize)
    finally:
        PyBuffer_Release(ct.byref(view))

    return ret


def get_sizeof_void_p():

    return PyLong_FromSize_t(sizeof(void *))


def get_contiguous(obj, buffertype, order):

    """Get a contiguous memoryview."""

    #PyObject *obj;
    #PyObject *buffertype;
    #PyObject *order;

    long type;
    char ord;

    if not PyLong_Check(buffertype):
        raise TypeError("buffertype must be PyBUF_READ or PyBUF_WRITE")

    type = PyLong_AsLong(buffertype)
    if type == -1 and PyErr_Occurred():
        return NULL;

    if type != PyBUF_READ and type != PyBUF_WRITE:
        raise ValueError("invalid buffer type")

    ord = _get_ascii_order(order)
    if ord == CHAR_MAX:
        return NULL;

    return PyMemoryView_GetContiguous(obj, (int)type, ord)


def py_buffer_to_contiguous(obj, order, flags):

    """PyBuffer_ToContiguous()"""

    #PyObject *obj;
    #PyObject *order;
    #int flags;

    view = Py_buffer()

    if PyObject_GetBuffer(obj, ct.byref(view), flags) < 0:
        return NULL;
    buf = NULL  # char*
    try:
        ord = _get_ascii_order(order)  # char
        if (ord == CHAR_MAX):
            return NULL

        buf = PyMem_Malloc(view.len)
        if (buf == NULL):
            raise PyErr_NoMemory()

        if PyBuffer_ToContiguous(buf, ct.byref(view), view.len, ord) < 0:
            return NULL

        ret = PyBytes_FromStringAndSize(buf, view.len)
    finally:
        PyBuffer_Release(ct.byref(view))
        PyMem_XFree(buf)

    return ret


@annotate(bool)
def _fmtcmp(const char *fmt1, const char *fmt2):

    if fmt1 == NULL:
        return fmt2 == NULL or strcmp(fmt2, "B") == 0
    if fmt2 == NULL:
        return fmt1 == NULL or strcmp(fmt1, "B") == 0
    return strcmp(fmt1, fmt2) == 0


@annotate(bool)
def _arraycmp(const Py_ssize_t *a1, const Py_ssize_t *a2, const Py_ssize_t *shape, Py_ssize_t ndim):

    for (i = 0; i < ndim; i++):
        if shape and shape[i] <= 1:
            # strides can differ if the dimension is less than 2
            continue
        if a1[i] != a2[i]:
            return False
    else:
        return True


def cmp_contig(obj1, obj2):

    """Compare two contiguous buffers for physical equality."""

    # PyObject* obj1;  # buffer objects
    # PyObject* obj2;  #      -||-

    view1 = Py_buffer()
    view2 = Py_buffer()

    if PyObject_GetBuffer(obj1, ct.byref(view1), PyBUF_FULL_RO) < 0:
        raise TypeError("cmp_contig: first argument does not implement the buffer "
                        "protocol")

    if PyObject_GetBuffer(obj2, ct.byref(view2), PyBUF_FULL_RO) < 0:
        PyBuffer_Release(ct.byref(view1))
        raise TypeError("cmp_contig: second argument does not implement the buffer "
                        "protocol")
    try:
        if (not (PyBuffer_IsContiguous(ct.byref(view1), 'C') and
                 PyBuffer_IsContiguous(ct.byref(view2), 'C')) and
            not (PyBuffer_IsContiguous(ct.byref(view1), 'F') and
                 PyBuffer_IsContiguous(ct.byref(view2), 'F'))):
            return False

        # readonly may differ if created from non-contiguous
        if (view1.len      != view2.len or
            view1.itemsize != view2.itemsize or
            view1.ndim     != view2.ndim or
            not _fmtcmp(view1.format, view2.format) or
            bool(view1.shape)      != bool(view2.shape) or
            bool(view1.strides)    != bool(view2.strides) or
            bool(view1.suboffsets) != bool(view2.suboffsets)):
            return False

        if ((view1.shape      and not _arraycmp(view1.shape,      view2.shape,      NULL,        view1.ndim)) or
            (view1.strides    and not _arraycmp(view1.strides,    view2.strides,    view1.shape, view1.ndim)) or
            (view1.suboffsets and not _arraycmp(view1.suboffsets, view2.suboffsets, NULL,        view1.ndim))):
            return False

        if memcmp((char *)view1.buf, (char *)view2.buf, view1.len) != 0:
            return False
    finally:
        PyBuffer_Release(ct.byref(view1))
        PyBuffer_Release(ct.byref(view2))

    return True


def is_contiguous(obj, order):

    # PyObject* obj;
    # PyObject* order;

    Py_buffer* base;

    view = Py_buffer()

    ord = _get_ascii_order(order)  # char
    if (ord == CHAR_MAX):
        return NULL;

    if NDArray_Check(obj):
        # Skip the buffer protocol to check simple etc. buffers directly.
        base = &((ndarray *)obj)->head->base
        ret = bool(PyBuffer_IsContiguous(base, ord))
    else:
        if PyObject_GetBuffer(obj, ct.byref(view), PyBUF_FULL_RO) < 0:
            raise TypeError("is_contiguous: object does not implement the buffer "
                            "protocol")
        try:
            ret = bool(PyBuffer_IsContiguous(ct.byref(view), ord))
        finaly:
            PyBuffer_Release(ct.byref(view))

    return ret


char _get_ascii_order(order):

    char ord;

    if not PyUnicode_Check(order):
        raise TypeError("order must be a string")
        return CHAR_MAX

    ascii_order = PyUnicode_AsASCIIString(order)  # PyObject*
    if ascii_order == NULL:
        return CHAR_MAX

    ord = PyBytes_AS_STRING(ascii_order)[0]
    del ascii_order

    if ord != 'C' and ord != 'F' and ord != 'A':
        raise ValueError("invalid order, must be C, F or A")
        return CHAR_MAX

    return ord


static PyTypeObject ndarray =
{
    PyVarObject_HEAD_INIT(NULL, 0)
    "ndarray",                   /* Name of this type */
    &ndarray_as_sequence,        /* tp_as_sequence */
    &ndarray_as_mapping,         /* tp_as_mapping */
    PyObject_GenericGetAttr,     /* tp_getattro */
};

#**************************************************************************#
#                           StaticArray Object                             #
#**************************************************************************#

char       _static_mem[12]    = {0,1,2,3,4,5,6,7,8,9,10,11}
Py_ssize_t _static_shape[1]   = {12}
Py_ssize_t _static_strides[1] = {1}

_static_buffer = Py_buffer({
    _static_mem,     # buf
    NULL,            # obj
    12,              # len
    1,               # itemsize
    1,               # readonly
    1,               # ndim
    "B",             # format
    _static_shape,   # shape
    _static_strides, # strides
    NULL,            # suboffsets
    NULL             # internal
})


class staticarray(Buffer):

    #int legacy_mode; # if true, use the view.obj==NULL hack

    def __new__(cls, *args, **kwargs):
        return PyObject_New(staticarray, staticarray)

    def __init__(self, legacy_mode=False):
        self.legacy_mode = (legacy_mode != Py_False)

    def __getbuffer__(self, Py_buffer *view, int flags):
        """Return a buffer for a PyBUF_FULL_RO request. Flags are not checked,
        which makes this object a non-compliant exporter!"""
        *view = copy.copy(_static_buffer)
        if self.legacy_mode:
            view->obj = NULL  # Don't use this in new code.
        else:
            view->obj = self
