public: yes
tags: [git, history, paas]
summary: 
    Sometimes you want to purge old git history, because you have started atop
    of something that doesn't exist anymore.

Purging old git history
=======================

I have recently come across a situation where I had to purge git history. A
friend of mine has created a repository on top of CPython for good reasons.
However after we decided to move CPython out of `his library
<https://github.com/sk-/python-type-annotator/>`_, in which case we wouldn't need
the old history anymore.

So I had set out to do that. It was way more complicated than I expected.
Purging the history is quite easy, you basically follow `this stackoverflow
post
<http://stackoverflow.com/questions/4515580/how-do-i-remove-the-old-history-from-a-git-repository>`_.
You create a grafts file with the corresponding commit and use filter-branch.

Be careful though, this "tutorial" will delete your old history permanently. It
will keep the history starting from the commit you make a graft from.
Yes: **Make a backup!**

.. sourcecode:: bash

    $ du -sh .git
    121M    .git
    $ # Removing the origin just to make sure no reference is kept.
    $ git remote rm origin
    $ echo 21581f18dc98b69c0dad8863d70a0ce7842ce4fe > .git/info/grafts
    $ git filter-branch -- --all
    Rewrite 4352ea1fb4b0dfa5d28ad26ce6b9e042b126bd60 (8/8)
    Ref 'refs/heads/master' was rewritten
    $ rm .git/info/grafts
    $ du -sh .git
    121M    .git

However, the repository size is quite big, still. It's basically the same as in
the beginning. Git doesn't just delete old files that don't have a reference
anymore (you have to actually tell it to do that). There are mechanisms to keep
your repository clean (automatic ``git gc`` after a while, but still we want a
clean repository, now).

Removing old objects without references from ``.git/objects``
-------------------------------------------------------------

To actually remove all references to old git objects, you need to do quite a
few things:

- Remove the ``filter-branch`` backup.
- Expire the ``reflog``.
- Garbage collect everything

If you forget just **one** thing you might end up with the old repository size,
because the if reference remains, ``git gc`` is unable to remove the old
objects. The corresponding stackoverflow post can be found `here`_.

.. sourcecode:: bash

    $ git update-ref -d refs/original/refs/heads/master
    $ git reflog expire --expire=now --all
    $ git gc --prune=now --aggressive 
    $ du -sh .git
    164K    .git

*164K*: Win.

.. _here: http://stackoverflow.com/questions/7654822/remove-refs-original-heads-master-from-git-repo-after-filter-branch-tree-filte
