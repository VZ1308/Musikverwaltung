import tkinter as tk
from tkinter import messagebox, Toplevel
from classes import Musiksammlung, Track, Album


class AddAlbumDialog:
    def __init__(self, parent):
        self.top = Toplevel(parent)
        self.top.title("Album hinzufügen")
        self.top.geometry("400x200")
        self.top.transient(parent)  # Macht das Fenster modal
        self.top.grab_set()  # Stellt sicher, dass nur dieses Fenster Ereignisse empfangen kann

        tk.Label(self.top, text="Album Titel:").pack(pady=5)
        self.album_entry = tk.Entry(self.top)
        self.album_entry.pack(pady=5)

        tk.Label(self.top, text="Interpret:").pack(pady=5)
        self.interpret_entry = tk.Entry(self.top)
        self.interpret_entry.pack(pady=5)

        tk.Button(self.top, text="OK", command=self.on_ok, width=10).pack(pady=5)
        tk.Button(self.top, text="Abbrechen", command=self.on_cancel, width=10).pack(pady=5)

    def on_ok(self):
        self.album_titel = self.album_entry.get().capitalize().strip()
        self.interpret = self.interpret_entry.get().strip()

        if not self.album_titel or not self.interpret:
            messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt werden.")
        else:
            self.top.destroy()

    def on_cancel(self):
        self.top.destroy()

class AddTrackDialog:
    def __init__(self, parent):
        self.top = Toplevel(parent)
        self.top.title("Track hinzufügen")
        self.top.geometry("600x400")
        self.top.transient(parent)  # Macht das Fenster modal
        self.top.grab_set()  # Stellt sicher, dass nur dieses Fenster Ereignisse empfangen kann

        tk.Label(self.top, text="Album Titel:").pack(pady=5)
        self.album_entry = tk.Entry(self.top)
        self.album_entry.pack(pady=5)

        tk.Label(self.top, text="Track Titel:").pack(pady=5)
        self.track_entry = tk.Entry(self.top)
        self.track_entry.pack(pady=5)

        tk.Label(self.top, text="MP3 Dateiname:").pack(pady=5)
        self.dateiname_entry = tk.Entry(self.top)
        self.dateiname_entry.pack(pady=5)

        tk.Label(self.top, text="Länge des Tracks (in Sekunden):").pack(pady=5)
        self.laenge_entry = tk.Entry(self.top)
        self.laenge_entry.pack(pady=5)

        tk.Button(self.top, text="OK", command=self.on_ok, width=10).pack(pady=5)
        tk.Button(self.top, text="Abbrechen", command=self.on_cancel, width=10).pack(pady=5)

    def on_ok(self):
        self.album_titel = self.album_entry.get().capitalize().strip()
        self.track_titel = self.track_entry.get().strip()
        self.dateiname = self.dateiname_entry.get().strip()
        self.laenge = self.laenge_entry.get().strip()

        if not self.album_titel or not self.track_titel or not self.dateiname or not self.laenge:
            messagebox.showerror("Fehler", "Alle Felder müssen ausgefüllt werden.")
            return

        try:
            self.laenge = int(self.laenge)
        except ValueError:
            messagebox.showerror("Fehler", "Die Länge des Tracks muss eine Zahl sein.")
            return

        self.top.destroy()

    def on_cancel(self):
        self.top.destroy()

class ShowAlbumDialog:
    def __init__(self, parent, alben):
        self.top = Toplevel(parent)
        self.top.title("Album anzeigen")
        self.top.geometry("400x300")
        self.top.transient(parent)  # Macht das Fenster modal
        self.top.grab_set()  # Stellt sicher, dass nur dieses Fenster Ereignisse empfangen kann

        tk.Label(self.top, text="Wählen Sie ein Album:").pack(pady=5)

        self.album_listbox = tk.Listbox(self.top)
        self.album_listbox.pack(pady=5, fill=tk.BOTH, expand=True)

        for album in alben:
            self.album_listbox.insert(tk.END, f"{album.titel} - {album.interpret}")

        tk.Button(self.top, text="OK", command=self.on_ok, width=10).pack(pady=5)
        tk.Button(self.top, text="Abbrechen", command=self.on_cancel, width=10).pack(pady=5)

        self.selected_album = None

    def on_ok(self):
        if not self.album_listbox.curselection():
            messagebox.showerror("Fehler", "Bitte wählen Sie ein Album aus.")
            return

        index = self.album_listbox.curselection()[0]
        self.selected_album = self.album_listbox.get(index)
        self.top.destroy()

    def on_cancel(self):
        self.selected_album = None
        self.top.destroy()

class MusiksammlungGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Musiksammlung Verwaltung")
        self.root.geometry("800x600")

        self.musiksammlung = Musiksammlung()
        self.musiksammlung.laden_aus_datei("musiksammlung.json")

        self.create_widgets()

    def create_widgets(self):
        button_frame = tk.Frame(self.root, padx=10, pady=10)
        button_frame.pack()

        self.info_frame = tk.Frame(self.root, padx=10, pady=10, bg="lightgrey")
        self.info_frame.pack(side=tk.BOTTOM, fill=tk.BOTH)

        self.text_frame = tk.Frame(self.root, padx=10, pady=10)
        self.text_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        buttons = [
            ("Album hinzufügen", self.add_album),
            ("Album entfernen", self.remove_album),
            ("Track hinzufügen", self.add_track),
            ("Track entfernen", self.remove_track),
            ("Alle Alben anzeigen", self.show_albums),
            ("Album anzeigen", self.show_album),
            ("Speichern und Beenden", self.save_and_exit),
        ]

        for text, command in buttons:
            button = tk.Button(button_frame, text=text, command=command, width=20, height=2, bg="#4CAF50", fg="white", font=("Arial", 12))
            button.pack(pady=5)

        self.album_text = tk.Text(self.text_frame, font=("Arial", 12), wrap=tk.WORD)
        self.album_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.album_text.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.album_text.yview)

        self.info_label = tk.Label(self.info_frame, text="Willkommen zur Musiksammlungs-Verwaltung", bg="lightgrey", font=("Arial", 14))
        self.info_label.pack(pady=20)

    def add_album(self):
        dialog = AddAlbumDialog(self.root)
        self.root.wait_window(dialog.top)

        if hasattr(dialog, 'album_titel') and hasattr(dialog, 'interpret'):
            album = Album(dialog.album_titel, dialog.interpret)
            self.musiksammlung.album_hinzufuegen(album)
            self.info_label.config(text=f"Album '{dialog.album_titel}' von '{dialog.interpret}' wurde hinzugefügt.")
        else:
            messagebox.showinfo("Info", "Album hinzufügen abgebrochen.")

    def remove_album(self):
        if not self.musiksammlung.alben:
            messagebox.showinfo("Info", "Es gibt keine Alben zu entfernen.")
            return

        self.album_text.delete(1.0, tk.END)

        for album in self.musiksammlung.alben:
            self.album_text.insert(tk.END, f"{album.titel} - {album.interpret}\n")

        def on_select(event):
            if not self.album_text.tag_ranges(tk.SEL):
                return

            selected_text = self.album_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            album_title = selected_text.split(" - ")[0]

            self.musiksammlung.album_entfernen(album_title)
            self.info_label.config(text=f"Album '{album_title}' wurde entfernt.")
            self.album_text.delete(tk.SEL_FIRST, tk.SEL_LAST)

        self.album_text.bind('<ButtonRelease-1>', on_select)

    def add_track(self):
        dialog = AddTrackDialog(self.root)
        self.root.wait_window(dialog.top)

        if hasattr(dialog, 'album_titel') and hasattr(dialog, 'track_titel') and hasattr(dialog,
                                                                                         'dateiname') and hasattr(
                dialog, 'laenge'):
            album_titel = dialog.album_titel
            track_titel = dialog.track_titel
            dateiname = dialog.dateiname
            laenge = dialog.laenge

            import re
            if not re.search(r'\.mp3$', dateiname):
                messagebox.showerror("Fehler", "Dateiname muss mit '.mp3' enden.")
                return

            for album in self.musiksammlung.alben:
                if album.titel == album_titel:
                    track = Track(track_titel, dateiname, laenge)
                    album.track_hinzufuegen(track)
                    self.info_label.config(text=f"Track '{track_titel}' wurde zu Album '{album_titel}' hinzugefügt.")
                    return
            self.info_label.config(text=f"Album '{album_titel}' wurde nicht gefunden.")
        else:
            messagebox.showinfo("Info", "Track hinzufügen abgebrochen.")

    def remove_track(self):
        if not self.musiksammlung.alben:
            messagebox.showinfo("Info", "Es gibt keine Tracks zu entfernen.")
            return

        self.album_text.delete(1.0, tk.END)

        for album in self.musiksammlung.alben:
            for track in album.tracks:
                self.album_text.insert(tk.END, f"{album.titel} - {track.titel}\n")

        def on_select(event):
            if not self.album_text.tag_ranges(tk.SEL):
                return

            selected_text = self.album_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            album_title, track_title = selected_text.split(" - ")

            for album in self.musiksammlung.alben:
                if album.titel == album_title:
                    try:
                        album.track_entfernen(track_title)
                        self.info_label.config(text=f"Track '{track_title}' wurde aus Album '{album_title}' entfernt.")
                        self.album_text.delete(tk.SEL_FIRST, tk.SEL_LAST)
                    except ValueError as e:
                        messagebox.showerror("Fehler", f"Fehler beim Entfernen des Tracks: {e}")
                        return

        self.album_text.bind('<ButtonRelease-1>', on_select)

    def show_albums(self):
        self.album_text.delete(1.0, tk.END)
        self.info_label.config(text="")

        if not self.musiksammlung.alben:
            messagebox.showinfo("Info", "Es gibt keine Alben anzuzeigen.")
            return

        for album in self.musiksammlung.alben:
            album_duration = album.gesamt_spieldauer()
            self.album_text.insert(tk.END, f"--------------------------------------------------\n"
                                           f"Album: {album.titel}\nVon: {album.interpret}\nLänge: {album_duration}\n\n")
            for index, track in enumerate(album.tracks, start=1):
                try:
                    self.album_text.insert(tk.END, f"Track {index}: {track.track_daten()}\n")
                except AttributeError as e:
                    messagebox.showerror("Fehler", f"Fehler beim Anzeigen des Tracks: {e}")
                    return
            self.album_text.insert(tk.END, "\n")

    def show_album(self):
        if not self.musiksammlung.alben:
            messagebox.showinfo("Info", "Es gibt keine Alben anzuzeigen.")
            return

        dialog = ShowAlbumDialog(self.root, self.musiksammlung.alben)
        self.root.wait_window(dialog.top)
        if dialog.selected_album:
            album_title, _ = dialog.selected_album.split(" - ", 1)
            for album in self.musiksammlung.alben:
                if album.titel == album_title:
                    self.album_text.delete(1.0, tk.END)
                    self.album_text.insert(tk.END, f"Album: {album.titel} von {album.interpret}\n")
                    for idx, track in enumerate(album.tracks, start=1):
                        self.album_text.insert(tk.END, f"   Track {idx}: {track.track_daten()}\n")
                    self.album_text.insert(tk.END, f"Dauer: {album.gesamt_spieldauer()} \n")
                    self.info_label.config(text=f"Album '{album_title}' wird angezeigt.")
                    return

    def save_and_exit(self):
        self.musiksammlung.speichern_in_datei("musiksammlung.json")
        messagebox.showinfo("Info", "Daten wurden gespeichert. Programm wird beendet.")
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusiksammlungGUI(root)
    root.mainloop()
