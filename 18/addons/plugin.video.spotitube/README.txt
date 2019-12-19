README bei Problemen mit Kodi-JARVIS 16 und Diesem und evtl. anderen ADDONS:

Da jetzt mehr und mehr Webseiten auf SSL\TLS 1.2 umstellen (bzw. diese voraussetzen) kommt es hier und da zu Fehlern mit älteren Kodi\Python-Versionen.

Erstmal ein paar Fakten:

- kein generelles Problem mit HTTPS-Links
- kein Youtube Music-Problem
- kein Kodi-Problem
- Problem mit älteren Python-Versionen

Um genauer zu werden:

Python < 2.7.9 = Fehlermeldungen bei TLS 1.2
Python > 2.7.9 = Keine Fehlermeldungen bei TLS 1.2

Die Fehlermeldung sieht z.B. so aus:
URLError: <urlopen error [Errno 1] _ssl.c:510: error:14077410:SSL routines:SSL23_GET_SERVER_HELLO:sslv3 alert handshake failure>

Die von euren System benutzte Python-Version lässt sich im DEBUG-Log von KODI einsehen (steht direkt neben der z.B. YOUTUBE-Version).
z.B.: [plugin.video.youtube] Running: YouTube (5.3.6) on Jarvis (16.1) with Python 2.7.8

Da die Kodi 17 Installationen funktionieren, gibt es bei Problemen mit "ssl-ERROR" in Kodi-JARVIS eigentlich nur eine Möglichkeit:

WINDOWS:
1.  Kodi 16 (kodi-16.1-Jarvis.exe) installieren und NICHT starten
2.  Kodi 17 downloaden
3.  Kodi 17 entpacken (z.b mit 7-Zip)
4.  Danach den gesamten entpackten "$_OUTDIR\python" kopieren nach "C:\Program Files (x86)\Kodi\system\python" und vorhandene Dateien ersetzen
(Sollte keine Probleme verursachen, bei mir läuft wieder alles mit dieser Änderung)

Für portable Kodi-Version auf WINDOWS:
Vorgang 1 bis 3 siehe oben.
4.  Danach den gesamten entpackten "$_OUTDIR\python" kopieren nach "...Kodi\system\python" und vorhandene Dateien ersetzen

ANDROID-Boxen:
neustes libreelec Build für Kodi 16 installieren (sofern die Box das unterstützt)

Also wer dasselbe Problem wie ich hat, sollte natürlich auf eigene Gefahr, diesen Lösungsansatz mal in Betracht ziehen !