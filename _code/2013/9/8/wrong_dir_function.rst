public: yes
tags: [python, jedi, builtins]
summary: 
    Pythons dir function is what developers use all the time, but it
    doesn't return correct results when used with classes.

Why Python's dir function is wrong
==================================

In this post I want to describe why Pythons ``dir`` function is not working
correctly. It's something that I've stumbled upon by developing Jedi_. This
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
may want to read some things about metaclasses_.


An improved dir function
------------------------

To simplify things, let us just create a different ``dir`` function, where
``old_dir`` would be how the ``dir`` function currently behaves:

.. sourcecode:: python

    NotDefined = object()
    old_dir = dir

    def dir(obj=NotDefined):
        if obj is NotDefined:
            return old_dir()

        if isinstance(obj, type):
            return sorted(set(old_dir(obj)) | set(old_dir(obj.__class__)))
        else:
            return old_dir(object)


Why does this happen?
---------------------

For C code analysis I'm going to switch to the latest revisions (Python
3.4.0a1+). Somewhere in Python > 3.2 ``__dir__`` methods have been added to
all the normal objects (You could've customized your functions for a long time
now). The ``dir`` function looks up the magic functions for an object and
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


As you can see there's a note in front of the ``type_dir`` method (in
``Objects/typeobject.c``), that says: *"We deliberately don't suck up its
__class__, as methods belonging to the metaclass would probably be more
confusing than helpful."* **This is the explanation.** I think that's not
correct, because people would like to know that there's a ``__bases__``
variable and a very useful ``__subclasses__`` method in classes. ``dir`` is the
tool Python programmers typically find out about it.

Solution? Just change the ``type_dir`` function, please! I will also suggest
this in the Python issue tracker. Edit: `I just did
<http://bugs.python.org/msg197471>`_.

Why did I research this? Because I want Jedi_ to be correct. Really.


Update
------

Thank you for the discussion on `reddit
<http://www.reddit.com/r/Python/comments/1m6zrq/pythons_dir_function_is_wrong/>`_,
I want to clarify a few things:

Jedi_ doesn't actually use the ``dir`` and ``__dir__`` function. I
just realized that I haven't made this clear. Jedi generally doesn't execute
code. The reason why I'm mentioning this is because it has really confused me 
(I'm using the interactive shell to introspect).

Some argue that ``__bases__`` is not relevant. That's true in a lot of cases.
But most of the other magic methods are also not relevant. I mean seriously,
who knows what ``str.__reduce_ex__`` even does? Who would use it? ``__bases__``
is something that a lot of people have used in contrary. So IMHO there are two
options: Either show all the methods or none. I think it's perfectly ok to now
show magic methods in ``dir``. You could also change the function to 
``dir(object, magic=False)``, that's also ok. I just think that the current
implementation is confusing.

If you still don't believe me, even the awesome ``ipython`` `rewrote dir
<https://github.com/ipython/ipython/blob/f645e5c044efeacf1aa523ec43f6a25d439e287b/IPython/utils/dir2.py>`_
and included the ``type`` methods.


.. _Jedi: https://github.com/davidhalter/jedi-vim
.. _metaclasses: http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python
