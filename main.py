import threading, random, pathlib, sys
from pygame import mixer
from pystray import Icon, MenuItem, Menu
from mutagen.mp3 import MP3
from PIL import Image, ImageTk
import tkinter as tk

mixer.init()
running = True

if getattr(sys, 'frozen', False):
    BASE_DIR = pathlib.Path(sys._MEIPASS)
else:
    BASE_DIR = pathlib.Path(__file__).parent

ASSET_FOLDER = BASE_DIR / "assets"
SOUND_FOLDER = BASE_DIR / "sounds"

root = tk.Tk()
root.withdraw()

def popup_fullscreen_image(image_path, audio_path, opacity=0.65, volume=0.3):
    audio_length = MP3(audio_path).info.length
    popup = tk.Toplevel(root)
    popup.overrideredirect(True)
    popup.attributes("-topmost", True)
    popup.attributes("-alpha", opacity)
    popup.configure(bg="black")
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    popup.geometry(f"{screen_width}x{screen_height}+0+0")
    img = Image.open(image_path)
    max_width = screen_width // 3
    max_height = screen_height // 3
    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    label = tk.Label(popup, image=tk_img, bg="black")
    label.place(relx=0.5, rely=0.55, anchor="center")
    label.image = tk_img
    mixer.music.load(audio_path)
    mixer.music.set_volume(volume)
    mixer.music.play()
    root.after(int(audio_length * 1000), popup.destroy)

def play_random_phonk_with_overlay():
    sound_files = list(SOUND_FOLDER.glob("*.mp3"))
    if not sound_files:
        return
    audio_file = random.choice(sound_files)
    images = [img for img in ASSET_FOLDER.glob("*.png") if img.name != "icon.png"]
    if not images:
        return
    image_file = random.choice(images)
    popup_fullscreen_image(image_file, audio_file, opacity=0.65, volume=0.5)

def schedule_chaos():
    if running:
        play_random_phonk_with_overlay()
        root.after(15000, schedule_chaos)

def quit_app(icon, item):
    global running
    running = False
    mixer.quit()
    icon.stop()
    root.quit()

icon_path = ASSET_FOLDER / "icon.ico"
icon_image = Image.open(icon_path)
menu = Menu(MenuItem("Quit", quit_app))
icon = Icon("WinPhonk", icon_image, "WinPhonk", menu)

threading.Thread(target=icon.run, daemon=True).start()
root.after(15000, schedule_chaos)
root.mainloop()
