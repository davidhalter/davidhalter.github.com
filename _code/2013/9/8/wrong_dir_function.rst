public: yes
tags: [python, jedi, builtins]
summary: A comparison between the autocompletion libraries Jedi and Rope.

Why Python's dir function is wrong
==================================

In this post I want to describe why Pythons ``dir`` function is not working
correctly. It's something that I've stumbled upon by developing jedi_. This
also describes how the ``type`` and ``object`` internals work.

Have you ever noted how the ``dir`` function is not returning all the
attributes of an object? (Note: all examples are Python 3.2, but I've tested it
with the latest revisions as well)

.. sourcecode:: python

    dir(str)
    >>> dir(str)  # note: no __bases__
    ['__add__', '__class__', '__contains__', ...]
    >>> str.__bases__  # note: no AttributeError
    (<class 'object'>,)

``dir`` obviously doesn't return all the methods it should. Why? ``str`` is a
``type`` and an ``object``:

.. sourcecode:: python

    >>> isinstance(str, object)
    True
    >>> isinstance(str, type)
    True

Well is everything a ``type`` then?

.. sourcecode:: python

    >>> isinstance(type, type)
    True
    >>> isinstance(str(), type)
    False

This also shows how ``type`` is a ``type``. If you want to understand that, you
may want to read some things about metaclasses_. ``type`` also has an attribute
``bases``


An improved dir function
------------------------

To simplify things, let us just create a different ``dir`` function, where
``old_dir`` would be how the ``dir`` function currently behaves:

.. sourcecode:: python

    NotDefined = object()
    old_dir = dir

    def dir(object=NotDefined):
        if object is NotDefined:
            return old_dir()

        if isinstance(type, object):
            return sorted(set(old_dir(object)) | set(old_dir(object.__class__)))
        else:
            return old_dir(object)

Does this solve the problem completely?

No.


Further explorations
--------------------

There are other problems. At least this one:

.. sourcecode:: python

    >>> class X(): pass
    ...
    >>> set(dir(X)) - set(dir(object))
    {'__dict__', '__module__', '__weakref__'}
    >>> set(dir(object)) - set(dir(X))
    set()
    >>> object.__dict__
    dict_proxy({'__ne__': <slot wrapper '__ne__' of 'object' objects>, ...}
    >>> object.__module__
    'builtins'
    >>> object.__weakref__
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: type object 'object' has no attribute '__weakref__'

As you can see, ``dir`` tells us that the "empty" class ``X`` has three more
attributes than ``object``. This is not true. ``__dict__`` and ``__module__``
do exist in the class. By instantiating ``object()``, it loses these two 
attributes. This also happens when you use ``__slots__``:

.. sourcecode:: python

    >>> class Z():
    ...     __slots__ = ()
    ... 
    >>> Z().__dict__
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: 'Z' object has no attribute '__dict__'

However, ``object.__slots__`` and other builtin methods without a ``__dict__``
at runtime (like ``str``) don't specify ``__slots__``. This makes it more
complicated to write a dir function in pure Python solution, but probably not
in cpython.


Why does this happen?
---------------------

For C code analysis I'm going to switch to the latest revisions (Python
3.4.0a1+). Somewhere in Python > 3.2 ``__dir__`` functions have been added to
all the normal objects. Before that the logic was probably in a different
place. The ``dir`` function looks up the magic functions for an object and
executes it.

There are two different kind of ``__dir__`` functions, one for objects - one
for types, let's look at the C code documentation:

.. sourcecode:: c

    /* __dir__ for generic objects: returns __dict__, __class__,                    
       and recursively up the __class__.__bases__ chain.                            
    */                                                                              
    static PyObject *                                                               
    object_dir(PyObject *self, PyObject *args)                                      
    {                                                                               
        /* the comments above say everything */
    }                                                                               

    /* __dir__ for type objects: returns __dict__ and __bases__.                    
       We deliberately don't suck up its __class__, as methods belonging to the     
       metaclass would probably be more confusing than helpful.                     
    */                                                                              
    static PyObject *                                                               
    type_dir(PyObject *self, PyObject *args)                                                                              
    {                                                                               
        PyObject *result = NULL;                                                    
        PyObject *dict = PyDict_New();                                              
                                                                                    
        if (dict != NULL && merge_class_dict(dict, self) == 0)                      
            result = PyDict_Keys(dict);                                             
                                                                                    
        Py_XDECREF(dict);                                                           
        return result;                                                              
        /* full source code, not shortened*/
    }


As you can see there's a note in front of the ``type_dir`` method, that says:
*"We deliberately don't suck up its __class__, as methods belonging to the
metaclass would probably be more confusing than helpful."* **This is the
explanation.** I think that's not correct, because people would like to know that
there's a ``__bases__`` variable and a very useful ``__subclasses__`` method in
classes. ``dir`` is the tool Python programmers typically find out about it.

Solution? Just change the ``type_dir`` function, please! I will also suggest
this in the Python issue tracker.


.. _jedi: https://github.com/davidhalter/jedi-vim
.. _metaclasses: http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python
