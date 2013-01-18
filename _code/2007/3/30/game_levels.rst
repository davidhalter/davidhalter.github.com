public: yes
tags: [game, delphi, gui, matura]
summary: High school thesis, loading of game levels.

Game Levels
===========

.. note ::

    This is about a game I once wrote, which was part of my high school
    thesis. Unfortunately, it's written in German.


Ich habe jetzt das Levelladen und den Leveleditor eigentlich fertiggestellt.
Das ganze ist so aufgebaut, dass man von `.3ds` Dateien laden kann, die dann
verarbeitet werden intern und in ein eigenes Format übergehen.

Das schöne daran ist, dass ich einfach Levels in `3ds Max` konstruieren kann,
die dann in meinem Spiel optimiert werden. Auf den Bildern werden überall die
Nodes der Octrees angezeigt, die max. 500 dreiecke enthalten.

Wie man auf einigen Bildern sieht, sind teilweise Objekte relativ krass Polygon
- intensiv, wie z.B. dieser Busch hier.

Ausserdem habe ich Frustum Culling eingebaut, sodass nur die Würfel, die vor
der Kamera liegen angezeigt werden.

Weiterhin werde ich noch PVS (potentially visible sets) einbauen, die dann
helfen werden Würfel auszublenden, die hinter anderen Objekten verdeckt werden.

Momentan arbeite ich fest an den Kollisionen und bin mich heftig in
Vektorgeometrie 3d am einarbeiten, da ich dies bei einem Lehrer gehabt hab, wo
ich nicht gerade viel gelernt hab. Ausserdem sind Kollisionsberechnungen wie
z.B. Sphere-Triangle und orientet Bounding Box - Triangle, die auf
Geschwindigkeit optimiert werden müssen nicht gerade die einfachsten.
Schwerer wirds dann noch wenn ich Treppen usw. realisieren will, wo man dann
auch noch über polygone hinwegsteigen können sollte. Da frag ich mich dann
wirklich, wie ich sowas mach. Wenn jemand eine gute Idee hat, bitte melden! ;-)


.. image:: ../level2.jpg
   :align: center

.. image:: ../level1.jpg
   :align: center

Hier ist leider noch was dazwischengerutscht, sry ;)

.. image:: ../level3.jpg
   :align: center
