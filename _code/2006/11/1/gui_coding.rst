public: yes
tags: [game, delphi, gui, matura]
summary: Game GUI Coding

GUI - Coding
============

.. note ::

    This is about a game I once wrote, which was part of my high school
    thesis. Unfortunately, it's written in German.

Ich hab in den Herbstferien und auch in den folgenden Wochen ziemlich lange
Zeit mit dem proggen einer selbst entworfenen GUI (graphical user interface)
zugebracht. Mittlerweile ist die Unit 2100 Zeilen lang, was ungefähr 40 Seiten
entspricht. Also nicht gerade ein kleines Projekt ;)

Das ganze ist natürlich Objekt - Orientiert um diese GUI so leicht wie möglich
in verschiedene Projekte importieren zu können. Durch die Objektorientierung
kann man auch beliebige Elemente für Fenster hinzufügen. Sie braucht ausserdem
zwei Bibliotheken namens `dglOpenGL.pas` und `Textures.pas`. Dies ist übrigens
auch mein erster wirklicher Versuch Objekt - Orientiert zu programmieren und
ich finde, es ist mir wirklich ziemlich gut gelungen!

Im allgemeinen Erben alle Komponenten von der Klasse TGUIObject, wo die ganzen
grundsätzlichen Variabeln drin sind (z.B. `X`,`Y`, `Width`, `onMousedownEvent`,
etc...)

Die Klasse `TButton` sieht dann zb nur noch so aus:

.. sourcecode:: pascal

    TButton = class(TGUIObject)
        Caption: String;
        Pressed: boolean;
        TextColor: TColor;
        procedure Render;
    end;


die Klasse `TPanel` gar so:

.. sourcecode:: pascal

    TPanel = class(TGUIObject)
        procedure Render;
    end;


Die Klasse `TGUIObject` möchte ich jetzt nicht niederschreiben, dass würde wohl
den Rahmen sprengen (Es sind nämlich über 50 Elemente die da drin versteckt
sind ;) ).

Die GUI besteht aus 10 verschiedenen Elementen:

* 0: Buttons 
* 1: Text 
* 2: Panels 
* 3: ProgressBars 
* 4: Edits
* 5: Checkboxes 
* 6: RadioButtons 
* 7: Windows
* 8: minimizeButton 
* 9: maximizeButton 
* 10: closeButton

Dabei muss man aber zwingenderweise betrachten, dass die letzten 3 Elemente nur
für die Vervollständigung der Windows sind.
Ausserdem gibt es folgende Key/Mouse Routinen:

* onclickevent 
* onMousedownevent 
* onMouseupevent
* onMousemove 
* onkeydownevent 
* onkeyupevent 
* onDragEvent 
* afterDragEvent

Diese sind auf alle Objekte anwendbar (ausser die Buttons in der Captionbar).
Das schöne an diesem Aufbau ist, dass ich durch diese Befehle z.B.(Das zweite
kleine Fenster):

.. sourcecode:: pascal

    i := GUIclass.AddWindow(400,300,100,100,0,'Test2');
    GUIclass.Windows[i].visible := true;
    GUIclass.Windows[i].dragevent := true;
    GUIclass.Windows[i].CaptionBar := true;

ganz einfach ein Window anzeigen kann. Das dann auch schon verschiebbar ist und
alle Grundelemente hat. Wenn man dann noch
`GUIclass.Windows[0].AddButton(220,60,125,20,'Decrease Alpha!');` eingibt, kann
man auch ganz leicht Buttons und ähnliche Elemente anzeigen.

Die GUI ist noch nicht wirklich voll ausgearbeitet, es ist erst ein
Anfangsstadium. Ausserdem ist der Style momentan auf dem doofen Windows 2000
und dies möchte ich definitiv nicht beibehalten (*schäm*). Die Texturen sind
auch noch gekehrt, dies müsste ich noch bei allen ändern. Dies sollte
allerdings nicht ein rieses Problem sein.

Da man aber im generellen sagt, jede Beschreibung kommt nicht an Bilder heran,
hier sind sie:
Bild mit 100% Alpha...
(Die Frameraten sollten übrigens überhaupt nicht entscheidend sein, denn da ist
noch ein sleep von 10ms drin bei jedem Frame, also ist 100 das Maximum)

.. image:: ../sample1.0.jpg
   :align: center

Bild 2 mit 30% Alpha oder sowas ähnliches...

.. image:: ../sample2.1.jpg
   :align: center

Zwei Tipps noch an OpenGL/Delphi Programmierer:

1. Achtet auf eure Pointer, die müssen immer schön aktuell sein, sonst kanns zu
   ziemlich dämlichen Komplikationen kommen.
2. Ich konnte irgendwie mit `Pointer := @self;` nicht den Effekt erreichen, den
   ich erreiche wenn ich das ganze einfach zb so eingebe: `Pointer := @windows[j]`.
   Hantiert also nicht mit `@self` herum, ist zumindest bei mir schief gelaufen.
