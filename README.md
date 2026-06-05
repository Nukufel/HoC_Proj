# Persönlicher Assistent – Telegram Chatbot

## Idee & Motivation

Ich hatte einen Termin vergessen und habe mir gedacht das einen Kalender it einer KI zu verbinden,
währe ein gutes Projekt für das Modul.
Daraus entstand die Idee, einen persönlichen Assistenten zu bauen,
der mir dabei hilft, Termine, Aufgaben und Einkäufe im Alltag im Blick zu behalten und nicht zu vergessen.
Als Interface habe ich Telegram gewählt,
da es plattformübergreifend verfügbar ist und ich kein eigenes UI machen wollte.

## Architektur & Vorgehen

Das System besteht aus drei Schichten:

**Telegram-Interface** nimmt Nachrichten und Fotos entgegen und gibt die Antwort des Agenten zurück.
Täglich um 07:00 Uhr sendet der Bot automatisch eine Morgennachricht mit den anstehenden Terminen.

**ReAct-Agent** basiert auf LangChain/LangGraph mit GPT-4o-mini und erhält bei jedem Aufruf das aktuelle Datum sowie den Wochentag.
Eine Middleware-Pipeline verarbeitet die Anfrage:
- **SummarizationMiddleware** fasst den Chatverlauf zusammen, sobald er zu lang wird, um den Kontext im Rahmen zu halten.
- **ModelCallLimitMiddleware** begrenzt die Anzahl Tool-Aufrufe des Agents um nicht in einem Loop stecken zu bleiben.
- **PIIMiddleware** blockiert sensible Nachrichten.
- **advance_date** Ein before_model-Hook aktualisiert vor jedem LLM-Aufruf wiederkehrende Events, wenn ihr Datum in der Vergangenheit liegt. 
Ihr Datum wird dann um sieben Tage nach hinten geschoben.

Ursprünglich wurden Nutzereingaben vor der Übergabe an den Agenten durch `dateparser` normalisiert. 
Dies hat aber zu problemen geführt. Z.B. "10 am" wurde zu Oktober. Deshalb wird das jetzt vom Model selbst gemacht.

**Datenbank** ist eine lokale SQLite-Datenbank mit vier Tabellen: Benutzer-Profil, Kalenderevents, Einkaufsliste und Notizen. 
Die Datenbank ist das Langzeitgedächtnis des Agents alle relevanten informationen werde darin gespeichert.

## Tools

Der Agent verfügt über mehrere Tools um mit der Datenbank zu interagieren.
Eine grosse Herausforderung war die Gestaltung der Tool-Beschreibungen.
Der Agent muss selbstständig entscheiden, welches Tool wann aufgerufen wird.
Zu Beginn waren die beschreibungen KI generiert. Das hat nicht gut funktioniert. 
Dann habe ich die beschreibungen überarbeitend habe aber die Struktur beibehalten was gut funktioniert hat.
Auch wichtig war es nicht zu ähnliche Tools zu haben da das den Agent verwirren kann. Deshalb musste ich ein paar Tools entfernen.

## Bildanalyse

Schickt der User ein Foto (Einkaufsliste, Stundenplan, Notizen), 
extrahiert der Image handler die relevanten Informationen und strukturiert diese. 
Die strukturierte Informationen werden dann an den Agent übergeben.
Der Agent speichert die Informationen anschliessend automatisch in der Datenbank indem er die passenden Tools.

## RAG (entfernt)
Ursprünglich war die Bildanalyse eine RAG-Middleware. Man konnte PDF über den Chat hochladen. 
Allerdings ist es mir nicht gelungen strukturierte Daten daraus zu bekommen. Ein weiterer grund für die änderung war,
dass ich meinen Stundenplan nicht als PDF exportieren konnte.

## Testing
Ich habe hauptsächlich Manuel getestet. Ich habe mir Testcases generieren lassen und habe diese dann Bearbeitet.
Die Manuellen Tests sollen der Reihenfolge nach ausgeführt werden. 
Ich teste Manuel um zu sehen ob die Applikation richtig funktioniert.
Zudem habe ich mir von Claude ein paar Unit-Tests für die Tools schreiben lasse. 
Ich habe mir nicht viel mühe mit den Unit-Test gegeben da ich zuerst Manuel Getestet habe.

## Probleme (gross)
1.  Beim Testen zeigte sich ein Bug: Events die per Bild erfasst wurden, hatten oft ein falsches Datum.
    Ich hatte vergessen, dass das aktuelle Datum nicht an den Vision-Prompt übergeben wurde. 
    Relative Angaben im Bild wie „Montag" konnten deshalb nicht korrekt interpretiert werden.
2. Beim hinzufügen von einem Event ist es oft nicht ganz klar ob dies wiederkehrend ist. 
   Dafür, habe ich leider keine lösung gefunden.
3. Ich habe lange gebraucht bis ich den 'daly-job' für die "Good-Morning-Message" aufgesetzt hatte. 
   Mir hat die Chat-ID gefehlt und mir war nicht klar wie ich an dir herankomme.
   Schlussendlich habe ich herausgefunden das es erst eine Nachricht von Telegram braucht um die ID zu erhalten. 
   Die Chat-ID wird in einem .env File gespeichert.

## Security

Sowohl der OpenAI-API-Key als auch der Telegram-API-Key werden in Umgebungsvariablen gespeichert und sind im Code selbst nie sichtbar.
Die PIIMiddleware im Agent blockiert Nachrichten, die API-Keys oder andere sensitiven Daten enthalten, bevor sie das Modell erreichen.

Warum gibt es kein Call/Rate limit? Ich glaube nicht, dass das für einen Personal-Assistant nötig ist.

## Setup/Deployment

Der Telegram-Bot und der Agent laufen lokal.
Der Bot wurde über BotFather erstellt, das offizielle Telegram-Tool zum Registrieren von Bots.
Für Anfragen an das LLM wird LangChains OpenAI-Wrapper benutzt.
Als LLM wird OpenAI's GPT-4o-mini für Text und Bildanalyse verwendet.

Der Telegram Bot muss beim ersten Mal mit "/start" im Telegram-Chat selbst gestartet werden.
Die App kann dann durch Ausführen von `telegram_bot.py` gestartet werden.

## Erweiterungs-Möglichkeiten
Wie schon in der Präsentation gesagt währ das hochladen von Quittungen cool. Damit könnten dan gekaufte sachen aus der Einkaufsliste gelöscht werden.
Auch hatte ich überlegt die Stundenplan API zu benutzen bin aber nicht mehr dazu gekommen.
