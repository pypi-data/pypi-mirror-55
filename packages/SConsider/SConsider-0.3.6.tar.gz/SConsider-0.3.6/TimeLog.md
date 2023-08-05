~~~ {.plantuml name="diagram2"}
@startuml
(with_perf laufen lassen) as a1
(sconsider aktuell buildet nicht) as a2
(Build ohne Baseoutdir \ngeht nicht) as a3
(Testcase erstellen) as a4
(relativer Pfad wird \nnicht richtig zus'gesetzt) as a5
(anpassen von newsconsider) as a6
(warum brauchts package-reldir?) as a7
(build output von 3rdparty kommt sonst\nin das sconsider 3rdparty verzeichnis) as a8
(configurable 'once' filter for deprecated msg\nhttps://docs.python.org/2/howto/logging-cookbook.html#using-filters-to-impart-contextual-information) as a9
(InstallSystemLibs soll auch gehen\nfür installed binaries) as aa
a1 --> a2: erledigt
a2 --> a3: erledigt
a3 --> a5: 20160816T1500-20160816T1700
a3 --> a4: 20160816T1700-20160816T1715\n20160817T0810-20160817T1200\n20160817T1320-20160817T1330
a7 --> a8: 20160816T1330-20160816T1355
a1 --> a1: 20160816T1355-20160816T1650
a6 --> a6: 20160817T1650-20160817T1704
aa --> aa: 20160817T1710-20160817T1805\n20160817T2145-20160817T2245\n20160818T0733-20160818T
@enduml
~~~

