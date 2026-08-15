# ⛳ FairwayData 

Eine moderne iOS-App für Golfer, entwickelt mit **SwiftUI** und **MapKit**. Die App bietet eine umfassende Übersicht über Golfplätze, integriert lokale OpenStreetMap-Daten (OSM) sowie Overpass-API-Abfragen und ermöglicht es der Community, Platzdetails direkt zu korrigieren und als strukturierte OSM-Notizen zu übermitteln.

## ✨ Features

* **Interaktive Golf-Karte (`GPSMapView`):** Visualisierung von Golfplätzen und POIs in der Umgebung mit 3D-Flyover-Ansicht.
* **OpenStreetMap Integration:** Offline-fähige und aktuelle Golfplatzdaten, kombiniert mit Geodaten.
* **Strukturierter OSM-Platz-Editor (`StructuredOSMReportView`):** Direkte Korrektur von Platzdetails (Name, Löcher, Greenfee, Golf-Cart-Verleih, Öffnungszeiten, Par, Kontaktdaten und Adresse) mit direktem Export an die OpenStreetMap-Notizen-API.
* **Lokaler Self-Healing-Datenabgleich:** Sofortige Übernahme von Korrekturen in die lokalen JSON-Datenstrukturen.

## 📱 Technologie-Stack

* **SwiftUI** & **MapKit** (für moderne iOS-UI und Kartendarstellung)
* **CoreLocation** (Standortdienste)
* **Codable JSON Management** (lokale Datenhaltung der Kontinente/Golfclubs)

