import tkinter as tk
from tkinter import ttk, messagebox
import requests
import pygame
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.configure(bg='#1C1C1C')  # background color
        self.root.geometry("400x300")  # The initial size of the window
        self.root.resizable(False, False)  # Disable resizing

        # Set window icon
        icon_image = ImageTk.PhotoImage(Image.open("music_icon.jpg"))
        self.root.tk.call('wm', 'iconphoto', self.root._w, icon_image)

        # Borders
        self.root.option_add('*BorderWidth', 2)
        self.root.option_add('*Relief', 'solid')

        # Style
        style = ttk.Style()
        style.configure('TButton', padding=6, font=('Helvetica', 10), background='#00A2FF', foreground='white')
        style.configure('TLabel', padding=6, font=('Helvetica', 12), background='#1C1C1C', foreground='white')
        style.configure('TEntry', padding=6, font=('Helvetica', 10), background='#3C3C3C', foreground='white')
        style.configure('TListbox', padding=6, font=('Helvetica', 10), background='#3C3C3C', foreground='white')

        self.base_url = "https://api.deezer.com/search"
        self.music_listbox = tk.Listbox(root, selectmode=tk.SINGLE, width=40, height=8, font=('Helvetica', 10), bg='#3C3C3C', fg='white')
        self.music_listbox.pack(pady=10)

        self.search_entry = ttk.Entry(root, font=('Helvetica', 10))
        self.search_entry.pack(pady=10)

        self.search_button = ttk.Button(root, text="Search Music", command=self.search_music)
        self.search_button.pack(pady=10)

        self.play_button = ttk.Button(root, text="Play", command=self.play_music)
        self.play_button.pack(pady=10)

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_music)
        self.stop_button.pack(pady=10)

        # Initialize Pygame for music playback
        pygame.init()

    def search_music(self):
        query = self.search_entry.get()
        if query:
            params = {'q': query}
            try:
                response = requests.get(self.base_url, params=params)
                data = response.json()

                if 'data' in data and len(data['data']) > 0:
                    self.music_listbox.delete(0, tk.END)  # Clear previous search results

                    for track in data['data']:
                        title = track['title']
                        artist = track['artist']['name']
                        self.music_listbox.insert(tk.END, f"{title} - {artist}")

                else:
                    messagebox.showinfo("No Results", "No music found for the given query.")

            except requests.ConnectionError:
                messagebox.showerror("Connection Error", "Unable to connect to the Deezer API.")

        else:
            messagebox.showwarning("Empty Input", "Please enter a music query.")

    def play_music(self):
        selected_index = self.music_listbox.curselection()
        if selected_index:
            selected_track = self.music_listbox.get(selected_index)
            messagebox.showinfo("Now Playing", f"Now playing: {selected_track}")

            # You should implement the logic to play the selected music using pygame here.
            # For simplicity, let's assume you have the music file URL and use pygame.mixer.music.load and pygame.mixer.music.play.

            # Example:
            # music_url = "https://example.com/music.mp3"
            # pygame.mixer.music.load(music_url)
            # pygame.mixer.music.play()

        else:
            messagebox.showwarning("No Selection", "Please select a music to play.")

    def stop_music(self):
        pygame.mixer.music.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayer(root)
    root.mainloop()
