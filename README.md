# Whisper / Faster-Whisper — ASR Benchmark

Ovaj projekat radim u okviru master rada na Elektronskom fakultetu u Nišu, na studijskom programu Veštačka inteligencija i mašinsko učenje.

Cilj mi je da uporedim Whisper i Faster-Whisper i ispitam kako veličina modela, kvantizacija i parametri transkripcije utiču na tačnost, brzinu i potrošnju resursa. Poseban fokus je na prepoznavanju govora na srpskom jeziku i izvršavanju na CPU-u.

Za glavni benchmark koristim **40 prirodnih srpskih audio snimaka, tri govornika i različite dužine govora**. Rezultate analiziram pomoću WER-a, RTF-a, vremena izvršavanja i RAM memorije.

## Eksperimenti

Eksperimenti su organizovani u Jupyter notebook-ovima od `00` do `08`:

| Notebook | Šta se ispituje                                                        |
| -------- | ---------------------------------------------------------------------- |
| `00`     | Poređenje originalnog Whisper-a i Faster-Whisper-a                     |
| `01`     | Uticaj veličine modela: tiny, base, small i medium                     |
| `02`     | Otpornost na beli i pink šum pri različitim SNR nivoima                |
| `03`     | Poređenje tačnosti transkripcije na srpskom i engleskom jeziku         |
| `04`     | Uticaj beam search parametra na WER i brzinu                           |
| `05`     | INT8 i FLOAT32 kvantizacija — latencija, RAM i RTF                     |
| `06`     | Uticaj Voice Activity Detection (VAD) algoritma                        |
| `07`     | Simulacija streaming transkripcije sa chunk-ovima od 2, 5 i 10 sekundi |
| `08`     | Automatski izbor konfiguracije na osnovu WER-a, RTF-a i RAM-a          |

## Neki od rezultata

* INT8 kvantizacija ubrzala je `medium` model približno **1,64×** u odnosu na FLOAT32, uz smanjenje prosečnog RTF-a sa 1,390 na 0,832.
* U eksperimentu sa šumom prosečan WER raste sa **47,89%** na čistim snimcima na približno **82,7%** pri SNR-u od 0 dB.
* Kod streaming simulacije chunk od 2 s daje brži prvi rezultat, ali znatno veći WER. Chunk od 10 s ostvaruje manji WER uz duže čekanje.
* U integracionom eksperimentu `small + INT8` ostvario je najviši balansirani skor za korišćeni benchmark i definisane kriterijume.

Rezultati se odnose na konkretan test skup i korišćeno CPU okruženje.

## Struktura projekta

```text
Projekat2ASR/
├── audio/
│   ├── 40Sentences00-08Notebooks/
│   ├── 03_srpski_engleski/
│   ├── snr_test_10sr/
│   ├── VAD/
│   └── Fine_Tuning/
├── notebooks/          # Eksperimenti 00–08
├── rezultati/           # CSV tabele i grafikoni
├── docs/                # Dokumentacija master rada, trenuntno master rad u PDF formatu. Prezentacija uskoro. 
├── requirements.txt
└── README.md
```

U folderu `Fine_Tuning` pripremljeni su dodatni audio zapisi i metadata fajlovi za prilagođavanje modela.

## Pokretanje

Projekat je rađen u Python-u, uz Jupyter Notebook, PyTorch, Whisper, Faster-Whisper i CTranslate2.

```bash
pip install -r requirements.txt
jupyter notebook
```

Notebook-ovi se nalaze u folderu `notebooks/`. Eksperimenti `00–07` mogu se pokretati pojedinačno, dok `08` koristi prethodno sačuvane rezultate.

---

**Aleksandar Jovanović**
Master studije — Veštačka inteligencija i mašinsko učenje
Elektronski fakultet, Univerzitet u Nišu
