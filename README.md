# AI Travel Guide MVP

Vorausschauender KI-Reiseführer für Autofahrten.

Der MVP ist als iOS/SwiftUI-App-Skeleton angelegt. Kernfunktion:

- GPS/Heading erfassen
- POIs vor dem Fahrzeug erkennen
- Entfernung und Uhrzeit-Richtung berechnen
- relevante Hinweise priorisieren
- deutsche Sprachausgabe vorbereiten
- Simulationsmodus für Route Nals → Terlan → Bozen → Ritten/Oberbozen

## Start in Xcode

1. Neues iOS-Projekt in Xcode erstellen:
   - Product Name: `TravelGuideMVP`
   - Interface: SwiftUI
   - Language: Swift
2. Die Dateien aus `TravelGuideMVP/Sources/TravelGuideMVP/` in das Xcode-Projekt übernehmen.
3. `NSLocationWhenInUseUsageDescription` in `Info.plist` setzen:

```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>Die App nutzt deinen Standort, um vorausliegende interessante Orte zu erkennen.</string>
```

## Architektur

- `AppConfig`
- `GeoMath`
- `POI`
- `LocalDemoPOIProvider`
- `ForwardCorridorScanner`
- `RelevanceRanker`
- `NarrationBuilder`
- `SpeechService`
- `LocationService`
- `SimulationService`
- `TravelGuideViewModel`
- `ContentView`

## Datenschutz

Der MVP arbeitet lokal mit Demo-POIs. Es ist kein API-Key im Code enthalten.

## Status

Erster technischer Startpunkt. Noch kein fertiges Produkt.
