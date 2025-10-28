from pathlib import Path
import sys
import os

track_map = {
    3: "Level3.mp3",
    4: "Level4.mp3",
    5: "Level5.mp3",
    6: "Level6.mp3",
    7: "Level7.mp3",
    "home": "Home.mp3"
}

_muted = False
_current_music = None
_pygame_ok = False

# INIT GAME MIXER
try:
    import pygame
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    _pygame_ok = True
except Exception as e:
    print(f"[music] pygame not available or failed to init: {e}")
    _pygame_ok = False

def _resource_path(filename):
    if getattr(sys, "frozen", False): base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    else: base = os.path.abspath(".")
    return os.path.join(base, filename)

def _resolve_target(target):
    if isinstance(target, int): fname = track_map.get(target)
    elif isinstance(target, str) and target in track_map: fname = track_map[target]
    elif isinstance(target, str): fname = target
    else: return None

    path = _resource_path(fname)
    if Path(path).is_file(): return path
    else:
        dirp = Path(os.path.dirname(path) or ".")
        for f in dirp.iterdir():
            if f.is_file() and f.name.lower() == fname.lower(): return str(f)
    return None

def play(target, loop=True, volume=0.7):
    global _current_music
    if not _pygame_ok:
        if not hasattr(play, "_warned"):
            print("[music] pygame not available — music disabled.")
            play._warned = True
        return

    filepath = _resolve_target(target)
    if not filepath:
        print(f"[music] File for target {target!r} not found. Looked for: {track_map.get(target, target)}")
        return

    try:
        try:
            pygame.mixer.music.stop()
            if hasattr(pygame.mixer.music, "unload"): pygame.mixer.music.unload()
        except Exception: pass

        pygame.mixer.music.load(filepath)
        pygame.mixer.music.set_volume(0.0 if _muted else float(volume))
        pygame.mixer.music.play(-1 if loop else 0)
        _current_music = filepath
        if _muted:
            try: pygame.mixer.music.pause()
            except Exception: pass
    except Exception as e: print(f"[music] error playing {filepath}: {e}")

def stop():
    global _current_music
    if not _pygame_ok: return
    try: pygame.mixer.music.stop()
    except Exception: pass
    _current_music = None

def mute():
    global _muted
    _muted = True
    if not _pygame_ok: return
    try: pygame.mixer.music.pause()
    except Exception: pass

def unmute():
    global _muted
    _muted = False
    if not _pygame_ok: return
    try: pygame.mixer.music.unpause()
    except Exception: pass

def toggle_mute():
    global _muted
    if _muted:
        unmute()
        return True
    else:
        mute()
        return False

def is_muted(): return _muted

def current(): return _current_music
