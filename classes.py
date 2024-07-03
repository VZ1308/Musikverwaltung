import datetime
import json


class Track:
    def __init__(self, titel, dateiname, laenge):
        self.titel = titel
        self.dateiname = dateiname
        self.laenge = datetime.timedelta(seconds=laenge)  # laenge als Sekundenwert

    def track_daten(self):
        minutes, seconds = divmod(self.laenge.total_seconds(), 60)
        return f"{self.titel} [{int(minutes):02d}:{int(seconds):02d}]"

    def to_dict(self):
        return {
            "titel": self.titel,
            "dateiname": self.dateiname,
            "laenge": int(self.laenge.total_seconds())
        }


class Album:
    def __init__(self, titel, interpret):
        self.titel = titel
        self.interpret = interpret
        self.tracks = []

    def track_hinzufuegen(self, track):
        self.tracks.append(track)

    def track_entfernen(self, titel):
        self.tracks = [track for track in self.tracks if track.titel != titel]

    def gesamt_spieldauer(self):
        total = sum((track.laenge for track in self.tracks), datetime.timedelta())
        minutes, seconds = divmod(total.total_seconds(), 60)
        return f"{int(minutes):02d}:{int(seconds):02d}"

    def album_daten(self):
        output = f"Album: {self.titel}\nVon: {self.interpret}\nLänge: {self.gesamt_spieldauer()}\n"
        for idx, track in enumerate(self.tracks, start=1):
            output += f"Track {idx}: {track.track_daten()}\n"
        return output

    def to_dict(self):
        return {
            "titel": self.titel,
            "interpret": self.interpret,
            "tracks": [track.to_dict() for track in self.tracks]
        }


class Musiksammlung:
    def __init__(self):
        self.alben = []

    def album_hinzufuegen(self, album):
        self.alben.append(album)

    def album_entfernen(self, titel):
        self.alben = [album for album in self.alben if album.titel != titel]

    def alle_alben_anzeigen(self):
        return "\n\n".join(album.album_daten() for album in self.alben)

    def speichern_in_datei(self, dateiname):
        with open(dateiname, 'w') as f:
            data = {
                "alben": [album.to_dict() for album in self.alben]
            }
            json.dump(data, f, indent=4)

    def laden_aus_datei(self, dateiname):
        try:
            with open(dateiname, 'r') as f:
                data = json.load(f)
                self.alben = []
                for album_data in data.get("alben", []):
                    album = Album(album_data["titel"], album_data["interpret"])
                    for track_data in album_data["tracks"]:
                        track = Track(track_data["titel"], track_data["dateiname"], track_data["laenge"])
                        album.track_hinzufuegen(track)
                    self.album_hinzufuegen(album)
        except FileNotFoundError:
            print(f"Die Datei '{dateiname}' wurde nicht gefunden.")
