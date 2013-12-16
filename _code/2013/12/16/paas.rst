public: yes
tags: [python, depl, deploy, paas]
summary: 

Platform as a Service: A Market Analysis
========================================

Trying to create a really developer friendly deploy tool depl_, I did some
market research. By creating it open source and not as a business, it does not
make sense to create it if something clearly better is out there. Platform as a
Service (`PaaS <wiki>`_) is a very easy way of getting your website deployed.
Sometimes. In a few blog posts I am thinking out loud about deploying. See
also TODO_

The thing that current PaaS solves
----------------------------------

There are quite a few companies trying to compete for a developer friendly 
hosting/deploy platform. Among those are heroku_, openshift_ and cloudfoundry_,
to name the biggest players.

PaaS essentially solves the struggle to deploy apps (typically web apps) to the
internet. What you could have done with a few build scripts, ansible_ or chef_
is now possible without any hassle, especially because it solves:

- No downtime, also during deploy (depends on hoster).
- Automatic app detection, typically with heroku buildpacks, even dokku_ uses
  those. Which means no configuration at all.
- An integrated backup solution - backup is not an issue anymore.
- Multiple staging/deployment "clusters", that one can target (see cloudfoundry_)

I know, some of the PaaS solutions may not solve all of those points, but they
are basically things that are not so easy to solve with "just another deploy
tool".

It is important to note at this point, that PaaS are not an option for a lot of
in-house apps, because even if they are created open source - like openshift_
and cloudfoundry_ - it's not that easy to set them up, because your own cloud
still requires a lot of ressources and maintenance.


Why is PaaS not enough?
-----------------------

The big problem with PaaS is basically that they don't really give you power
over the servers you are using. The most visible manifestation of that is that
almost nobody uses static files with heroku_ (and there's probably the same
issue with openshift_).

I really don't want app development - I want software development, where you as
a developer have control over the machine. This means configuring nginx and so
on. Being limited as a web developer reminds me too much of the old PHP shared
hosting times. What if you realize that you can gain a lot of speed by using a
certain cache, but your PaaS doesn't support that? Maybe it doesn't support
memcached?

But really - PaaS could also allow more configuration
-----------------------------------------------------

I think one of the problems that PaaS has right now is that people thought too
much about billing customers. I know cashflow is important - but having happy
customers also allows for that. They invest a lot into new services, but not
into a multitude of configurations of services. I think a combination of a
depl_ style configurations and a good docker_ service with backup capability
and HA load balancers could be a really interesting new PaaS for example.

Do you agree? I would really like to have your opinion on depl_ and its
approach. Especially the configuration API.


.. _depl: https://github.com/davidhalter/depl
.. _dokku: https://github.com/progrium/dokku
.. _cloudfoundry: http://cloudfoundry.com
.. _heroku: http://www.heroku.com
.. _openshift: https://www.openshift.com/
.. _ansible: https://github.com/ansible/ansible
.. _chef: https://github.com/opscode/chef
.. _depl: https://github.com/davidhalter/depl
.. _docker: http://www.docker.io
.. _wiki: http://en.wikipedia.org/wiki/Platform_as_a_service
