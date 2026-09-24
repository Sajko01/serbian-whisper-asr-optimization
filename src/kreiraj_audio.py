from gtts import gTTS
import os
from pydub import AudioSegment

os.makedirs('audio', exist_ok=True)

test_set = [
    {
        "audio": "audio/govor_p1_VAD.mp3",
        "ref": "Artificial intelligence represents a transformative branch of computer science dedicated to the creation of sophisticated systems capable of solving complex problems, making autonomous decisions, learning from vast amounts of data, and accurately understanding natural human speech in real-time environments."
    },
    {
        "audio": "audio/govor_p2_VAD.mp3",
        "ref": "Automatic speech recognition technology enables the seamless conversion of spoken audio signals into structured written text, playing a crucial role in modern applications such as voice assistants, automated transcription services, and accessibility tools for individuals with disabilities."
    },
    {
        "audio": "audio/govor_p3_VAD.mp3",
        "ref": "Deep learning based neural network models have significantly improved both the overall quality and the processing speed of modern speech recognition systems, allowing them to perform exceptionally well even in noisy environments and across various acoustic conditions."
    },
    {
        "audio": "audio/govor_p4_VAD.mp3",
        "ref": "The Whisper model family, originally developed by OpenAI, utilizes large-scale neural networks trained on diverse multilingual datasets to enable highly accurate speech recognition, translation, and speaker alignment across dozens of different languages and dialects."
    },
    {
        "audio": "audio/govor_p5_VAD.mp3",
        "ref": "Faster Whisper is an advanced and highly optimized implementation of the original Whisper architecture, built upon the CTranslate2 inference engine to deliver dramatic speed improvements and lower memory consumption without sacrificing transcription accuracy."
    }
]

for item in test_set:
    putanja = item["audio"]
    tekst = item["ref"]

    # 1. Generisanje govora preko gTTS-a
    temp_path = "temp.mp3"

    tts = gTTS(
        text=tekst,
        lang='en',
        slow=False
    )

    tts.save(temp_path)

    # 2. Učitavanje generisanog audio fajla
    audio_sve = AudioSegment.from_mp3(temp_path)

    # 3. Definisanje pauza
    pauza_pocetak = AudioSegment.silent(duration=2000)  # 2 sekunde
    pauza_sredina = AudioSegment.silent(duration=4000)  # 4 sekunde
    pauza_kraj = AudioSegment.silent(duration=5000)     # 5 sekundi

    # 4. Pronalaženje sredine audio zapisa
    sredina = len(audio_sve) // 2

    # 5. Podela audio zapisa na dva dela
    prvi_deo = audio_sve[:sredina]
    drugi_deo = audio_sve[sredina:]

    # 6. Spajanje:
    # 2s tišine + prvi deo govora + 4s tišine + drugi deo govora + 5s tišine
    audio_sa_pauzama = (
        pauza_pocetak
        + prvi_deo
        + pauza_sredina
        + drugi_deo
        + pauza_kraj
    )

    # 7. Čuvanje finalnog fajla
    audio_sa_pauzama.export(
        putanja,
        format="mp3"
    )

    print(f'Uspešno generisano: {putanja}')

# 8. Brisanje privremenog fajla
if os.path.exists("temp.mp3"):
    os.remove("temp.mp3")

print("Svi engleski audio fajlovi sa pauzama su spremni!")




###Priprema i generisanje test audio skupova






# from gtts import gTTS
# import os

# os.makedirs('audio', exist_ok=True)

# rechenice = [
#     ('audio/govor_sr_p1.mp3', 'Veštačka inteligencija predstavlja transformativnu granu računarskih nauka posvećenu kreiranju sofistiranih sistema sposobnih za rešavanje kompleksnih problema, donošenje autonomnih odluka, učenje iz ogromnih količina podataka i tačno razumevanje prirodnog ljudskog govora u okruženjima u realnom vremenu.'),
#     ('audio/govor_sr_p2.mp3', 'Tehnologija automatskog prepoznavanja govora omogućava besprekornu konverziju izgovorenih zvučnih signala u strukturirani pisani tekst, igrajući ključnu ulogu u savremenim aplikacijama kao što su glasovni asistenti, usluge automatske transkripcije i alati za pristupačnost osobama sa invaliditetom.'),
#     ('audio/govor_sr_p3.mp3', 'Modeli neuronskih mreža zasnovani na dubokom učenju značajno su poboljšali i ukupni kvalitet i brzinu obrade savremenih sistema za prepoznavanje govora, omogućavajući im da izuzetno dobro funkcionišu čak i u bučnim okruženjima i u različitim akustičkim uslovima.'),
#     ('audio/govor_sr_p4.mp3', 'Porodica modela Whisper, koju je originalno razvio OpenAI, koristi neuronske mreže velikog obima trenirane na raznovrsnim višejezičkim skupovima podataka kako bi omogućila visoko precizno prepoznavanje govora, prevođenje i usklađivanje govornika na desetinama različitih jezika i dijalekata.'),
#     ('audio/govor_sr_p5.mp3', 'Faster Whisper je napredna i visoko optimizovana implementacija originalne Whisper arhitekture, sagrađena na mašini za zaključivanje CTranslate2 radi pružanja dramatičnih poboljšanja brzine i manje potrošnje memorije bez žrtvovanja tačnosti transkripcije.')
# ]

# for putanja, tekst in rechenice:
#     # gTTS direktno čuva fajl (u mp3 formatu koji Whisper model bez problema čita na Windowsu)
#     tts = gTTS(text=tekst, lang='sr', slow=False)
#     tts.save(putanja)
#     print(f'Uspešno generisano: {putanja}')

# print('Svi audio fajl resursi su spremni!')








# from gtts import gTTS
# import os

# os.makedirs('audio', exist_ok=True)

# test_set = [
#     {
#         "audio": "audio/govor_p1_doprinos3.mp3",
#         "ref": "Artificial intelligence represents a transformative branch of computer science dedicated to the creation of sophisticated systems capable of solving complex problems, making autonomous decisions, learning from vast amounts of data, and accurately understanding natural human speech in real-time environments."
#     },
#     {
#         "audio": "audio/govor_p2_doprinos3.mp3",
#         "ref": "Automatic speech recognition technology enables the seamless conversion of spoken audio signals into structured written text, playing a crucial role in modern applications such as voice assistants, automated transcription services, and accessibility tools for individuals with disabilities."
#     },
#     {
#         "audio": "audio/govor_p3_doprinos3.mp3",
#         "ref": "Deep learning based neural network models have significantly improved both the overall quality and the processing speed of modern speech recognition systems, allowing them to perform exceptionally well even in noisy environments and across various acoustic conditions."
#     },
#     {
#         "audio": "audio/govor_p4_doprinos3.mp3",
#         "ref": "The Whisper model family, originally developed by OpenAI, utilizes large-scale neural networks trained on diverse multilingual datasets to enable highly accurate speech recognition, translation, and speaker alignment across dozens of different languages and dialects."
#     },
#     {
#         "audio": "audio/govor_p5_doprinos3.mp3",
#         "ref": "Faster Whisper is an advanced and highly optimized implementation of the original Whisper architecture, built upon the CTranslate2 inference engine to deliver dramatic speed improvements and lower memory consumption without sacrificing transcription accuracy."
#     }
# ]

# for item in test_set:
#     putanja = item["audio"]
#     tekst = item["ref"]
    
#     # gTTS za engleski jezik (lang='en')
#     tts = gTTS(text=tekst, lang='en', slow=False)
#     tts.save(putanja)
#     print(f'Uspešno generisano: {putanja}')

# print('Svi engleski audio fajlovi su spremni!')




