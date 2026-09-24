###Samostalna simulacija Faster-Whisper transkripcije u realnom vremenu



import time
import wave
import numpy as np
from faster_whisper import WhisperModel

# 1. Konfiguracija simulacije
PUTANJA_FAJLA = "audio/govor_sr_p1_gtts.wav"  # Izaberi jedan od tvojih snimljenih fajlova
TRAJANJE_BLOKA = 5                # Koliko sekundi "glumi" jedan blok u realnom vremenu

print(f"Učitavam audio fajl za simulaciju: {PUTANJA_FAJLA}...")

def ucitaj_wav_fajl(putanja):
    with wave.open(putanja, 'rb') as wf:
        framerate = wf.getframerate()
        n_frames = wf.getnframes()
        audio_bytes = wf.readframes(n_frames)
        # Konvertovanje 16-bit PCM u float32 normalizovano na opseg [-1.0, 1.0]
        audio_data = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        return audio_data, framerate

try:
    audio_celo, SAMPLE_RATE = ucitaj_wav_fajl(PUTANJA_FAJLA)
except FileNotFoundError:
    print(f"Greška: Fajl '{PUTANJA_FAJLA}' nije pronađen! Proveri da li se nalazi u 'audio' folderu.")
    exit()

print("Učitavanje Faster-Whisper modela (base)...")
model = WhisperModel("base", device="cpu", compute_type="int8")
print("Model je spreman! Pokrećem simulaciju striminga iz fajla...\n")

trenutna_pozicija = 0
velicina_bloka = int(TRAJANJE_BLOKA * SAMPLE_RATE)
ukupno_frejmova = len(audio_celo)

def simuliraj_blok():
    global trenutna_pozicija
    
    # Ako smo stigli do kraja fajla, vraćamo se na početak (beskonačna petlja)
    if trenutna_pozicija >= ukupno_frejmova:
        print("\n[INFO] Kraj fajla dostignut, vraćam se na početak... (Petlja)")
        trenutno_pozicija = 0
        
    kraj_pozicija = min(trenutna_pozicija + velicina_bloka, ukupno_frejmova)
    audio_data = audio_celo[trenutna_pozicija : kraj_pozicija]
    
    # Pomeramo pokazivač za sledeći blok
    stvarno_trajanje_isecka = len(audio_data) / SAMPLE_RATE
    trenutna_pozicija = kraj_pozicija

    print(f"\n--- [Simulacija] Obrada dela od {stvarno_trajanje_isecka:.1f} sekundi ---")
    
    pocetak = time.time()
    
    # Transkripcija isečka u hodu
    segments, info = model.transcribe(audio_data, beam_size=1, language="sr")
    
    tekst = ""
    for segment in segments:
        tekst += segment.text + " "
        
    kraj = time.time()
    latency = kraj - pocetak
    
    # Izračunavanje RTF-a (Real-Time Factor) za ovaj konkretan blok
    rtf = latency / stvarno_trajanje_isecka if stvarno_trajanje_isecka > 0 else 0
    
    print(f"Prepoznati tekst: {tekst.strip() if tekst.strip() else '[tišina / nema govora]'}")
    print(f"[Info] Vreme obrade (latencija): {latency:.2f} s")
    print(f"[Info] Real-Time Factor (RTF): {rtf:.4f} (Manje od 1.0 znači rad u realnom vremenu!)")

try:
    # Beskonačna petlja koja simulira striming dok je ne prekineš sa Ctrl + C
    while True:
        simuliraj_blok()
        time.sleep(1) # Kratka pauza između blokova
except KeyboardInterrupt:
    print("\nSimulacija zaustavljena od strane korisnika.")