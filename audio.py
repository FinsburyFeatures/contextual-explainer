from gtts import gTTS


def generate_audio_file(text_for_conversion, file_basename) -> str:
    audio = gTTS(text=text_for_conversion, lang='en', slow=False)
    audio.save((
        f"{file_basename}.mp3"
    ))
