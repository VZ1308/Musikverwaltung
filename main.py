from classes import Musiksammlung, Track, Album
def main():
    musiksammlung = Musiksammlung()
    musiksammlung.laden_aus_datei("musiksammlung.json")

    while True:
        print("\n--------------------------")
        print("Musiksammlung Verwaltung")
        print("--------------------------")
        print("1. Album hinzufügen")
        print("2. Album entfernen")
        print("3. Track hinzufügen")
        print("4. Track entfernen")
        print("5. Alle Alben anzeigen")
        print("6. Speichern und Beenden")

        choice = input("Wählen Sie eine Option (1/2/3/4/5/6): ")

        if choice == '1':
            titel = input("Album Titel: ")
            interpret = input("Interpret: ")
            album = Album(titel, interpret)
            musiksammlung.album_hinzufuegen(album)
            print(f"Album '{titel}' von '{interpret}' wurde hinzugefügt.")

        elif choice == '2':
            titel = input("Album Titel zum Entfernen: ")
            musiksammlung.album_entfernen(titel)
            print(f"Album '{titel}' wurde entfernt.")

        elif choice == '3':
            album_titel = input("Album Titel: ")
            for album in musiksammlung.alben:
                if album.titel == album_titel:
                    track_titel = input("Track Titel: ")
                    dateiname = input("MP3 Dateiname: ")
                    laenge = int(input("Länge des Tracks (in Sekunden): "))
                    track = Track(track_titel, dateiname, laenge)
                    album.track_hinzufuegen(track)
                    print(f"Track '{track_titel}' wurde zu Album '{album_titel}' hinzugefügt.")
                    break
            else:
                print(f"Album '{album_titel}' wurde nicht gefunden.")

        elif choice == '4':
            album_titel = input("Album Titel: ")
            track_titel = input("Track Titel zum Entfernen: ")
            for album in musiksammlung.alben:
                if album.titel == album_titel:
                    album.track_entfernen(track_titel)
                    print(f"Track '{track_titel}' wurde aus Album '{album_titel}' entfernt.")
                    break
            else:
                print(f"Album '{album_titel}' wurde nicht gefunden.")

        elif choice == '5':
            print("\n--- Alle Alben ---")
            print(musiksammlung.alle_alben_anzeigen())

        elif choice == '6':
            musiksammlung.speichern_in_datei("musiksammlung.json")
            print("Daten wurden gespeichert. Programm wird beendet.")
            break

        else:
            print("Ungültige Eingabe. Bitte wählen Sie eine der angegebenen Optionen.")


if __name__ == "__main__":
    main()
