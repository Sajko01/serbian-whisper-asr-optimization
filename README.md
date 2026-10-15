# Whisper / Faster-Whisper — Serbian ASR Benchmark & Domain Adaptation

Ovaj projekat realizovan je u okviru master rada na Elektronskom fakultetu Univerziteta u Nišu, na studijskom programu **Veštačka inteligencija i mašinsko učenje**.

Cilj projekta je analiza, optimizacija i domenska adaptacija Whisper modela za automatsko prepoznavanje govora (ASR) na srpskom jeziku. Poseban fokus stavljen je na poređenje Whisper i Faster-Whisper implementacija, uticaj veličine modela, kvantizacije i parametara transkripcije na tačnost, brzinu i potrošnju resursa.

Pored CPU benchmark eksperimenata, projekat obuhvata simulaciju segmentne transkripcije, višekriterijumski izbor konfiguracije i dodatno obučavanje Whisper Small modela na govornim podacima iz oblasti poljoprivrede.

## Eksperimentalni podaci

Za glavni benchmark korišćeno je **40 snimaka čitanog srpskog govora, tri govornika i različite dužine audio zapisa**.

Za dodatne eksperimente korišćeni su srpski i engleski govorni podaci, snimci sa kontrolisano dodatim šumom, kao i podaci iz korpusa FLEURS.

Za domensku adaptaciju formiran je poseban skup od **800 audio zapisa**, ukupnog trajanja 111,55 minuta, sa terminologijom iz oblasti poljoprivrede i uzgoja biljaka.

| Podskup | Broj snimaka |
|---|---:|
| Obučavanje | 675 |
| Validacija | 75 |
| Testiranje | 50 |
| **Ukupno** | **800** |

Test skup obuhvata snimke četvrtog govornika, koji nije bio zastupljen u podacima za obučavanje.

## Eksperimenti

Eksperimenti su organizovani u 12 Jupyter notebook-ova:

| Notebook | Šta se ispituje |
|---|---|
| `00` | Poređenje originalnog Whisper-a i Faster-Whisper-a |
| `01` | Uticaj veličine modela: tiny, base, small i medium |
| `02` | Otpornost na beli, roze i šum poljoprivredne mehanizacije pri različitim SNR nivoima |
| `03` | Poređenje transkripcije na srpskom i engleskom jeziku |
| `04` | Uticaj beam size parametra na WER i brzinu |
| `05` | INT8 i FP32 — vreme izvršavanja, RAM i RTF |
| `06` | Uticaj Voice Activity Detection (VAD) algoritma |
| `07` | Simulacija streaming transkripcije sa segmentima od 2, 5 i 10 sekundi |
| `08` | Automatski izbor konfiguracije na osnovu WER-a, RTF-a i RAM-a |
| `09` | Domenska adaptacija Whisper Small modela na poljoprivredni govor |
| `98` | Generalizacija adaptiranog modela na govorne podatke van ciljnog domena |
| `99` | Validacija konačnog profila za segmentnu transkripciju |

Eksperimenti optimizacije sprovedeni su prvenstveno na CPU-u, dok je dodatno obučavanje modela realizovano na GPU-u u Kaggle okruženju.

## Neki od rezultata

- INT8 kvantizacija ubrzala je `medium` model približno **1,64×** u odnosu na FP32, uz smanjenje prosečnog RTF-a sa 1,390 na 0,832.
- U eksperimentu sa šumom prosečan WER raste sa **47,89%** na čistim snimcima na približno **82,7%** pri SNR-u od 0 dB.
- Kod streaming simulacije segment od 2 s omogućava raniji prvi rezultat, ali uz znatno veći WER. Segment od 10 s ostvaruje manji WER uz duže čekanje.
- U višekriterijumskoj analizi `Faster-Whisper Small INT8` ostvario je najviši balansirani skor za korišćeni benchmark i definisane kriterijume.

Rezultati se odnose na konkretne test skupove i korišćeno hardversko okruženje.

## Domenska adaptacija Whisper Small modela

U završnom delu istraživanja sprovedeno je dodatno obučavanje prethodno obučenog modela `openai/whisper-small` na specijalizovanom govornom skupu iz oblasti poljoprivrede.

Obučavanje je realizovano pomoću biblioteke Hugging Face Transformers, u Kaggle okruženju na GPU-u NVIDIA Tesla T4.

Glavni parametri:

- Broj epoha: 5.
- Stopa učenja: `1e-5`.
- Efektivna veličina serije: 8.
- Mešovita preciznost FP16 tokom obučavanja.
- Izbor najboljeg modela na osnovu validacionog WER-a.
- Najbolji model sačuvan nakon treće epohe.
- Greedy dekodiranje prilikom evaluacije.

### Rezultati domenske adaptacije

| Metrika | Originalni Whisper Small | Adaptirani Whisper Small |
|---|---:|---:|
| WER korpusa | 31,01% | **17,32%** |
| CER korpusa | 5,91% | **3,23%** |
| Prosečan RTF | 0,0741 | 0,1012 |

Domenska adaptacija smanjila je WER na poljoprivrednom test skupu za **13,69 procentnih poena**, odnosno za približno **44,15% relativno**.

### Generalizacija na druge govorne skupove

| Test skup | Originalni WER | Adaptirani WER |
|---|---:|---:|
| Poljoprivredni govor — 50 snimaka | 31,01% | **17,32%** |
| Opšti srpski govor — 40 snimaka | 22,75% | **17,45%** |
| FLEURS srpski — 100 snimaka | **37,98%** | 40,43% |

Rezultati pokazuju da je adaptacija poboljšala tačnost na ciljnom poljoprivrednom skupu i glavnom skupu srpskog govora. Međutim, na FLEURS skupu došlo je do pogoršanja, što ukazuje da poboljšanje nije jednako na svim govornim podacima.

## Kaggle — skupovi podataka i eksperimenti

**Skupovi podataka:**

- [Serbian Agriculture Whisper Dataset](https://www.kaggle.com/datasets/sajkobre/serbian-agriculture-whisper) — poljoprivredni govorni skup za domensku adaptaciju.
- [Serbian General Speech ASR Benchmark](https://www.kaggle.com/datasets/sajkobre/serbian-general-speech-asr-benchmark) — govorni podaci za evaluaciju na opštem srpskom govoru.

**Kaggle notebook-ovi:**

- [Whisper Small — Serbian Agricultural Speech Fine-Tuning](https://www.kaggle.com/code/sajkobre/whisper-small-serbian-agricultural-speech-fine-t) — dodatno obučavanje i evaluacija modela.
- [Whisper Small — Generalization After Agricultural Fine-Tuning](https://www.kaggle.com/code/sajkobre/whisper-small-generalization-after-agricultural) — provera generalizacije adaptiranog modela.

## Struktura projekta

```text
Projekat2ASR/
├── audio/
│   ├── 03_srpski_engleski/
│   │   ├── engleski/
│   │   ├── fleurs/
│   │   └── srpski/
│   ├── 40Sentences00-08Notebooks/
│   ├── Fine_Tuning/
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   ├── snr_test_10sr/
│   ├── sum_mehanizacija/
│   └── VAD/
│       ├── natural_sr/
│       └── synthetic_en/
├── notebooks/
│   ├── 00_osnovno_poredjenje_whisper_faster_whisper_KONTROLISANO.ipynb
│   ├── 01_uticaj_velicine_modela.ipynb
│   ├── 02_otpornost_na_sum_snr.ipynb
│   ├── 03_srpski_engleski.ipynb
│   ├── 04_beam_search.ipynb
│   ├── 05_kvantizacija_latencija_rtf.ipynb
│   ├── 06_vad.ipynb
│   ├── 07_streaming.ipynb
│   ├── 08_automatski_izbor_konfiguracije.ipynb
│   ├── 09_fine_tuning_.ipynb
│   ├── 98_generalizacija_nakon_dodatnog_obucavanja.ipynb
│   └── 99_validacija_konacnog_profila.ipynb
├── src/
│   ├── generisi_vad_sr.py
│   ├── kreiraj_audio.py
│   └── realtime_whisper.py
├── texts/
│   ├── referentni_tekstovi_40.txt
│   └── sve_recenice.txt
├── rezultati/             # CSV rezultati, tabele i grafikoni
├── docs/                  # Master rad u DOCX/PDF formatu i prezentacija
├── faster-whisper-master/ # Lokalna kopija izvornog koda biblioteke
├── .gitignore
├── requirements.txt
├── links.txt
└── README.md
```

Direktorijum `src/` sadrži pomoćne Python skripte za pripremu audio podataka i demonstraciju segmentne transkripcije.

Direktorijum `texts/` sadrži referentne transkripcije, dok se u `rezultati/` nalaze sačuvani rezultati eksperimenata, tabele i grafikoni.

## Pokretanje

Projekat je realizovan u Python-u, uz Jupyter Notebook, PyTorch, Whisper, Faster-Whisper, CTranslate2 i Hugging Face Transformers.

```bash
pip install -r requirements.txt
jupyter notebook
```

Notebook-ovi se nalaze u direktorijumu `notebooks/`. Eksperimenti `00–07` mogu se pokretati pojedinačno uz odgovarajuće audio podatke, dok `08` koristi prethodno sačuvane rezultate.

Notebook `99` služi za validaciju konačne konfiguracije, dok su `09` i `98` namenjeni domenskoj adaptaciji i proveri generalizacije. Za ove eksperimente dostupne su i Kaggle verzije.

Pomoćne skripte nalaze se u direktorijumu `src/`:

- `generisi_vad_sr.py` — generisanje srpskih VAD test snimaka sa dodatim pauzama.
- `kreiraj_audio.py` — priprema sintetičkih audio zapisa pomoću gTTS-a.
- `realtime_whisper.py` — demonstracija segmentne Faster-Whisper transkripcije iz prethodno snimljenog audio fajla.

Simulacija segmentne transkripcije ne predstavlja potpuno implementiran sistem sa neprekidnim mikrofonskim ulazom.

## Dokumentacija

Kompletan master rad, sa opisom metodologije, tabelama, grafikonima, analizom rezultata i ograničenjima istraživanja, nalazi se u direktorijumu `docs/`, zajedno sa prezentacijom.

**Naslov master rada:** Analiza, optimizacija i domenska adaptacija Whisper modela za automatsko prepoznavanje govora na srpskom jeziku.

---

**Aleksandar Jovanović**  
Master studije — Veštačka inteligencija i mašinsko učenje  
Elektronski fakultet, Univerzitet u Nišu  
2026.