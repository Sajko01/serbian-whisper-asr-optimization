
import sys
import json
import time
import threading
import os
import psutil

from faster_whisper import WhisperModel


model_size = sys.argv[1]
compute_type = sys.argv[2]
audio_path = sys.argv[3]

process = psutil.Process(os.getpid())

def rss_mb():
    return process.memory_info().rss / (1024 ** 2)


# Početni RSS meri se nakon uvoza biblioteka, ali pre učitavanja modela.
baseline_rss = rss_mb()
uzorci = [baseline_rss]
stop_event = threading.Event()


def monitor_ram():
    while not stop_event.is_set():
        uzorci.append(rss_mb())
        time.sleep(0.01)

    uzorci.append(rss_mb())


monitor = threading.Thread(
    target=monitor_ram,
    daemon=True
)

monitor.start()

start_load = time.perf_counter()

try:
    model = WhisperModel(
        model_size,
        device="cpu",
        compute_type=compute_type
    )

    load_time = time.perf_counter() - start_load
    rss_after_load = rss_mb()

    # Jedna kontrolisana transkripcija istog audio zapisa.
    # Generator mora biti iscrpljen da bi se obrada zaista izvršila.
    start_transcribe = time.perf_counter()

    segments, _ = model.transcribe(
        audio_path,
        language="sr",
        beam_size=1,
        temperature=0.0,
        vad_filter=False
    )

    _ = " ".join(
        segment.text.strip()
        for segment in segments
    )

    transcribe_time = time.perf_counter() - start_transcribe

finally:
    stop_event.set()
    monitor.join()


peak_rss = max(uzorci)

rezultat = {
    "Model": model_size,
    "Kvantizacija": compute_type,
    "Baseline RSS [MB]": baseline_rss,
    "RSS nakon učitavanja [MB]": rss_after_load,
    "Peak RSS [MB]": peak_rss,
    "Peak RSS delta [MB]": max(0.0, peak_rss - baseline_rss),
    "Model Load Time [s]": load_time,
    "Kontrolna transkripcija [s]": transcribe_time
}

print("RAM_RESULT_JSON=" + json.dumps(rezultat))
