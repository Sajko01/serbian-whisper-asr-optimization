from pathlib import Path
import random

from pydub import AudioSegment
from pydub.silence import detect_silence


# ============================================================
# PODEŠAVANJA
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_DIR = PROJECT_ROOT / "audio" / "40Sentences00-08Notebooks"
OUTPUT_DIR = PROJECT_ROOT / "audio" / "VAD" / "natural_sr"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


FAJLOVI = [
    "28govornik1.wav",
    "32govornik3.wav",
    "33govornik3.wav",
    "36govornik1.wav",
    "40govornik3.wav",
]


# Koliko dodatnih pauza želimo po fajlu.
BROJ_PAUZA = 4

# Trajanje dodatne tišine koja se ubacuje.
# Za svaki fajl se uzima različita vrednost iz ovog opsega.
MIN_DODATNA_TISINA_MS = 1200
MAX_DODATNA_TISINA_MS = 2500

# Minimalno rastojanje između mesta na kojima ubacujemo pauze.
MIN_RAZMAK_IZMEDJU_PAUZA_MS = 3000

# Pydub silence detekcija.
MIN_POSTOJECA_TISINA_MS = 180

# Koliko dB ispod prosečne glasnoće mora biti segment da bi bio tišina.
SILENCE_OFFSET_DB = 16

# Fiksiran seed radi reproduktivnosti.
RANDOM_SEED = 42


# ============================================================
# POMOĆNE FUNKCIJE
# ============================================================

def pronadji_kandidate_za_pauze(audio: AudioSegment):
    """
    Pronalazi postojeće tihe delove audio zapisa.

    Kao kandidat za ubacivanje dodatne pauze koristi se sredina
    detektovanog tihog intervala.
    """

    silence_thresh = audio.dBFS - SILENCE_OFFSET_DB

    intervali_tisine = detect_silence(
        audio,
        min_silence_len=MIN_POSTOJECA_TISINA_MS,
        silence_thresh=silence_thresh
    )

    kandidati = []

    for start_ms, end_ms in intervali_tisine:
        sredina = (start_ms + end_ms) // 2

        # Ne želimo pauzu sasvim na početku ili kraju.
        if sredina < 1000:
            continue

        if sredina > len(audio) - 1000:
            continue

        kandidati.append(sredina)

    return kandidati


def izaberi_ravnomerno_kandidate(kandidati, broj_pauza):
    """
    Od postojećih kandidata bira nekoliko ravnomerno raspoređenih
    kroz ceo audio zapis.
    """

    if len(kandidati) <= broj_pauza:
        return sorted(kandidati)

    indeksi = []

    for i in range(broj_pauza):
        indeks = round(
            i * (len(kandidati) - 1) / (broj_pauza - 1)
        )
        indeksi.append(indeks)

    izabrani = [kandidati[i] for i in indeksi]

    # Uklanjanje kandidata koji su preblizu.
    filtrirani = []

    for pozicija in sorted(izabrani):
        if not filtrirani:
            filtrirani.append(pozicija)
            continue

        if pozicija - filtrirani[-1] >= MIN_RAZMAK_IZMEDJU_PAUZA_MS:
            filtrirani.append(pozicija)

    return filtrirani


def fallback_pozicije(audio: AudioSegment, broj_pauza):
    """
    Ako audio nema dovoljno jasno detektovanih tihih intervala,
    koristi približno ravnomerno raspoređene pozicije.

    Ovo se koristi samo kao rezervna opcija.
    """

    trajanje = len(audio)

    pozicije = []

    for i in range(1, broj_pauza + 1):
        pozicija = int(
            trajanje * i / (broj_pauza + 1)
        )

        pozicije.append(pozicija)

    return pozicije


def ubaci_tisine(audio: AudioSegment, pozicije, rng):
    """
    U audio ubacuje dodatnu tišinu na zadatim pozicijama.

    Važno:
    pozicije su definisane prema originalnom audio zapisu,
    pa prilikom umetanja pratimo koliko je vremena već dodato.
    """

    novi_audio = audio

    ukupno_dodato_ms = 0
    informacije = []

    for pozicija_original in sorted(pozicije):

        trajanje_tisine = rng.randint(
            MIN_DODATNA_TISINA_MS,
            MAX_DODATNA_TISINA_MS
        )

        stvarna_pozicija = (
            pozicija_original + ukupno_dodato_ms
        )

        tisina = AudioSegment.silent(
            duration=trajanje_tisine,
            frame_rate=audio.frame_rate
        )

        novi_audio = (
            novi_audio[:stvarna_pozicija]
            + tisina
            + novi_audio[stvarna_pozicija:]
        )

        informacije.append({
            "pozicija_original_ms": pozicija_original,
            "trajanje_tisine_ms": trajanje_tisine
        })

        ukupno_dodato_ms += trajanje_tisine

    return novi_audio, informacije


# ============================================================
# OBRADA JEDNOG FAJLA
# ============================================================

def obradi_fajl(naziv_fajla, rng):

    input_path = INPUT_DIR / naziv_fajla

    if not input_path.exists():
        print(f"[GREŠKA] Ne postoji: {input_path}")
        return

    print("\n" + "=" * 90)
    print(f"Obrada: {naziv_fajla}")
    print("=" * 90)

    audio = AudioSegment.from_wav(input_path)

    original_ms = len(audio)

    kandidati = pronadji_kandidate_za_pauze(audio)

    print(f"Pronađeno postojećih tihih mesta: {len(kandidati)}")

    pozicije = izaberi_ravnomerno_kandidate(
        kandidati,
        BROJ_PAUZA
    )

    # Ako nema dovoljno sigurnih tihih mesta,
    # koristi rezervne ravnomerne pozicije.
    if len(pozicije) < BROJ_PAUZA:

        print(
            "Nema dovoljno pouzdanih prirodnih pauza. "
            "Koristi se fallback raspored."
        )

        pozicije = fallback_pozicije(
            audio,
            BROJ_PAUZA
        )

    novi_audio, info = ubaci_tisine(
        audio,
        pozicije,
        rng
    )

    stem = Path(naziv_fajla).stem

    output_path = OUTPUT_DIR / f"{stem}_VAD.wav"

    # Forsiramo standardan WAV format.
    novi_audio.export(
        output_path,
        format="wav",
        parameters=[
            "-acodec", "pcm_s16le"
        ]
    )

    novo_ms = len(novi_audio)

    print(
        f"Originalno trajanje: "
        f"{original_ms / 1000:.2f} s"
    )

    print(
        f"Novo trajanje:       "
        f"{novo_ms / 1000:.2f} s"
    )

    print(
        f"Ukupno dodata tišina: "
        f"{(novo_ms - original_ms) / 1000:.2f} s"
    )

    print("\nUbačene pauze:")

    for i, stavka in enumerate(info, start=1):

        print(
            f"  {i}. oko "
            f"{stavka['pozicija_original_ms'] / 1000:.2f} s"
            f"  -> +"
            f"{stavka['trajanje_tisine_ms'] / 1000:.2f} s"
        )

    print(f"\nSačuvano: {output_path}")


# ============================================================
# MAIN
# ============================================================

def main():

    print("=" * 90)
    print("GENERISANJE PRIRODNIH SRPSKIH VAD TEST FAJLOVA")
    print("=" * 90)

    print(f"Ulaz:  {INPUT_DIR}")
    print(f"Izlaz: {OUTPUT_DIR}")

    rng = random.Random(RANDOM_SEED)

    for naziv_fajla in FAJLOVI:
        obradi_fajl(
            naziv_fajla,
            rng
        )

    print("\n" + "=" * 90)
    print("GOTOVO")
    print("=" * 90)

    print(
        f"Generisano je do {len(FAJLOVI)} "
        f"VAD test fajlova u:"
    )

    print(OUTPUT_DIR)


if __name__ == "__main__":
    main()