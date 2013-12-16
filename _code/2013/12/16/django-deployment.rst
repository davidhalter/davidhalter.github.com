public: yes
tags: [python, depl, deploy, django]
summary: "Deploying Django sucks. Still. A proposed solution."

The current state of deploying Django applications
==================================================

I've recently tried to release a Django application in a small intranet. It was
hell all over again. I'm not very experienced with nginx, uwsgi and gunicorn,
so I always have to read a lot.

The fact is: **Deploying Django in 2013 is hard!** As a guy who writes 2-3
small web apps a year, I don't want to fight with nginx and gunicorn. I just
want to use something like ``deploy test.example.org`` in my Django directory.

So I decided to write my own (and yet) little deployment software. If people
like it, I'm willing to invest some of my time. I would be very happy to
receive feedback on how we could create an API that makes deploying simple
things really easy!


PHP Goodness?!
--------------

Let's face it, PHP is horrible_. But the PHP eco system has always done one
thing fairly well: Deploying is easy. You can argue that Nginx is better than
Apache, but still all the new sexy systems (Django/Rails/Node/Flask) are far
more complicated to set up than ``apt-get install php5``, if you want to deploy
to your own server.

Now - I don't want (old) PHP deployment back. There's often no easy way of
making a difference between debug and production. People screw up dependencies
and permissions. But let's face it. PHP has something really valuable there for
beginners and "app programmers" that don't like dealing with systems,
especially if they don't like Linux (e.g. ``WAMP`` people).


Solution: Travis-ci?
--------------------

Anybody using `Travis-ci <https://travis-ci.org>`_? **Awesome**, right?  It
just solves testing for you. That is how I imagine depl_ to be. Travis also
does something like a deployment. Your code is completely running on their
servers and can be tested. In comparison to e.g. Heroku (which is also pretty
cool), travis uses a more explicit way to deploy. I like travis way better,
because travis yaml files allow for a more flexibility and complete control. I
also like to know what's going on.

My solution provides defaults for typical use cases. It leaves more complex use
cases to awesome software like ansible_. If you really need 10 different
databases, custom paths, etc, you shouldn't be using depl_.


Some Deployment Options
-----------------------

There are a variety of tools to deploy, but non of them really fit the simple
use case. I don't want dozens of files just for deploying my very simple Django
project. I want at most one (something like travis). But to give you an
overview:

- ansible_ is awesome for deploying big projects, you could check out `this 
  <http://www.stavros.io/posts/example-provisioning-and-deployment-ansible/>`_
  for a Django deployment with ansible.
- chef_/puppet_ do the same thing. But I like ansible_ with its ``.yml`` files
  better somehow. It's a cleaner approach IMHO.
- docker_ is awesome, but you still have to deploy your software into docker
  containers - that's where depl_ could step in.
- vagrant_ is cool(for development), but again - how do you deploy in the first
  place. And also I wouldn't trust virtualbox for deploying things.

I have analyzed those options and `Platform as a Service`_ providers
briefly. I realized that there is nothing to deploy Django easily (in an
in-house setting), so I started creating depl_. Not just for Django. For all
the frameworks out there that still struggle with deployment.


On a Side Note: Similar ideas to depl
-------------------------------------

I've found two projects that are similar to what I imagine a good deploy tool
should be like. The first one is capistrano_ for ruby/rails. My problem with
capistrano is that I don't really understand it - but I also don't really
understand the ruby world, so I won't complain here.  Something just smells
bad, because the tool can not be explained in one page.

Quite with the same problems struggles the second tool "wercker_". It's a
little bit too hard to explain, because it also includes a
testing/deploying/whatever platform. It seems to be a very complete and
complicated model - too complicated for a normal open source developer. Might
be interesting for professionals deploying web applications very often. 

However both really haven't inspired me. The only positive inspiration is
travis and the fact that all things should be easy in life. :-)

.. _depl: https://github.com/davidhalter/depl
.. _ansible: https://github.com/ansible/ansible
.. _ansible-django: 
.. _vagrant: https://github.com/mitchellh/vagrant
.. _docker: http://www.docker.io
.. _chef: https://github.com/opscode/chef
.. _puppet: https://github.com/puppetlabs/puppet
.. _horrible: http://me.veekun.com/blog/2012/04/09/php-a-fractal-of-bad-design/
.. _wercker: http://gigaom.com/2012/10/11/wercker-aims-to-fix-the-app-dev-universe/
.. _capistrano: https://github.com/capistrano/capistrano
.. _Platform as a Service: /code/2013/12/16/paas/
