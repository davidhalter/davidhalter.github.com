public: yes
tags: [python, jedi, rope, comparison]
summary: A comparison between the autocompletion libraries Jedi and rope.

Why Jedi not Rope
=================

Recently `I was asked
<http://www.reddit.com/r/Python/comments/15604u/pycharm_sale_75_off/c7qw8kv?context=3>`_
to compare Jedi with Rope, because saying "it's better" was just not good
enough. :-)

Now, in the python world there are 3 fairly good auto-completion systems:

- `Rope <http://rope.sourceforge.net/>`_
- PyCharm (commercial IDE, not a library)
- `Jedi <http://jedi.jedidjah.ch/>`_

The only other autocompletion library is `PySmell`, which is just very simple.
Doesn't understand code that is a little bit more complicated. Other solutions
include `PyDev`, `PyDiction`, and `pythoncomplete`, which are all fine but
don't offer a good autocompletion system.

I will compare Rope and Jedi now. I'm not comparing with PyCharm now, it's not
as good as Jedi, but I'll talk about that another day.

So the main difference between Rope and Jedi is their goal. You can see that in
the description:

- Rope, a python refactoring library.
- Jedi, an awesome autocompletion library for Python.

Rope was never really intended to be an autocompletion library and therefore
has a natural disadvantage in this field.

Completion comparison
---------------------

So I went down to the real business: Checking for cases that might work in one
library, but not in the other. So I sat down and used Spyder to compare a few
things (Spyder is using rope, but `is considering
<https://github.com/davidhalter/jedi/issues/102>`_ to switch to Jedi).  As
expected I haven't found anything that is working in rope, but not in Jedi.
With rope the following things don't complete (work in Jedi though):

- generators/iterators
- `__call__` and other magic methods
- completion within classes/functions
- dynamic arrays
- `*args`, `**kwargs`
- lambdas
- simple sys.path manipulations
- invalid code, rope cannot handle too many errors, in Jedi it will always work
  if some parts of the code are valid.
- performance in big files

Rope isn't "bad". It's just not as good as Jedi for autocompletion. But it's
pretty clear that rope fails to understand some basic principles of Python. For
example `list.append` in one place will already make rope useless.


API goodness
------------

Jedi has a very nice and user-friendly API:

.. sourcecode:: python

    >>> import jedi
    >>> source = '''import json; json.l'''
    >>> script = jedi.Script(source, 1, 19, 'example.py')
    >>> script
    <Script: 'example.py'>
    >>> completions = script.complete()
    >>> completions
    [<Completion: load>, <Completion: loads>]
    >>> completions[0].complete
    'oad'
    >>> completions[0].word
    'load'

So, what about rope? The documentation says something like this:

.. sourcecode:: python

    from rope.base.project import Project
    project = Project('.ropeproject')

    from rope.contrib import codeassist
    # Get the proposals; you might want to pass a Resource
    proposals = codeassist.code_assist(project, source_code, offset)
    proposals = codeassist.sorted_proposals(proposals)

    proposal[0].name

While I don't know it it's possible to do the same with rope and Jedi, it's
certainly clear that there's `no documentation
<http://rope.sourceforge.net/library.html#rope-contrib-codeassist>`_ around for
rope. It's also not clear how rope would check for relative imports, because
rope simply doesn't know where the file it is completing is situated at (the
project folder might be in an other directory).

Refactoring
-----------

This is really the place where rope shines. I don't want to talk about this too
long, but Jedi has only very limited refactoring possibilities like renaming.
There's a `discussion <https://github.com/davidhalter/jedi/issues/103>`_ going
on on github, how to improve the refactoring in Jedi. But rope will probably
always be better there.

Conclusion
----------

As Jedi is not really suited for refactoring, Rope is not really suited for
autocompletion. In a fully fledged IDE I would recommend to use Jedi for
autocompletion and Rope for refactorings. I think these two complement one
another very well.  would recommend to use Jedi for IDE features like 

But if you are asking yourself: **Which one should I choose** for my editor
(vim, emacs, sublime, etc)?* The answer should always be **Jedi**. You can
always add refactoring later on. But what you want in the beginning is a good
and rock-solid autocompletion library.
