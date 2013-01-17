public: yes

Blog reST Styleguide
====================

Sourcecode style
----------------

- Max line length is 80 characters.

Basic Formatting
----------------

- Use a single asterisk for *italic* text and a double asterisk for **bold**
  text.

**Example:**

.. sourcecode:: rst

    *italic*
    **bold**

Computer stuff
--------------

- Use single backticks for filenames or directories.

- Use double backticks for inline sourcecode or variable names.

- Use ``.. sourcecode:: language`` for larger parts of sourcecode.

**Example:**

.. sourcecode:: rst

    `/path/to/file.ext`
    ``size = 1000``

    .. sourcecode:: python
        for i in xrange(0, 11):
            print i

- If you don't want any syntax highlighting, use a normal literal block using
  ``::``.

** Example:**

.. sourcecode:: rst

    Following a block of code without syntax highlighting::

        $ ./manage.py migrate cmsplugin_mailchimp

        Running migrations for cmsplugin_mailchimp:
         - Migrating forwards to 0003_redirect_url.
         > cmsplugin_mailchimp:0003_redirect_url
         - Loading initial data for cmsplugin_mailchimp.
        Installed 0 object(s) from 0 fixture(s)

Images, alignment
-----------------

- To include images, use the ``image`` or ``figure`` directives. By default,
  images should be left aligned. You should provide an alt text using the
  ``:alt:`` attribute.

- A figure may provide a caption, it should be rendered in *italic* font.

- Images should be placed in a `/static/img/<year>/<month>/<day>/` folder.

**Example:**

.. sourcecode:: rst

    .. image:: /static/img/2012/6/17/spam.png
        :alt: Picture of a can of spam

    .. figure:: /static/img/2012/6/17/ni.jpg
        :alt: A knight who says NI!

        A knight who says NI!

Videos
------

- Use the ``youtube`` and ``vimeo`` directives.

- Videos sometimes look nice if they're scaled up to the width of the page. You
  can use the ``:width:`` and ``:height:`` attributes to resize them.

**Example:**

.. sourcecode:: rst

    .. youtube:: UsMvG8Tz0Ac

    .. vimeo:: 17227977
        :width: 900
        :height: 504

Tags
----

Use English, lowercase tag names.

TODO
----

- quotes, blockquotes
