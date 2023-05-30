from playsound import playsound # 미디어 출력 패키지 >> pip install playsound

def google_tts(query: str, res_path: str):
    from google.cloud import texttospeech

    # 클라이언트 객체를 인스턴스화합니다.
    client = texttospeech.TextToSpeechClient()

    # 합성할 텍스트 입력을 설정합니다.
    synthesis_input = texttospeech.SynthesisInput(text=query)

    # 음성 요청을 빌드합니다.
    # 언어 코드는 "ko-KR"를 선택하고, ssml 음성 성별은 "중립"으로 설정합니다.
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # 반환할 오디오 파일의 유형을 선택합니다.
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # 선택한 음성 매개변수와 오디오 파일 유형으로 텍스트를 음성 합성합니다.
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # 응답의 오디오 콘텐츠는 바이너리입니다.
    # 출력된 mp3파일의 이름을 넣으시면 됩니다.
    with open(res_path, "wb") as out:
        # 응답을 출력 파일에 작성합니다.
        out.write(response.audio_content)
        print('Audio content written to file "./audio/output.mp3"')

answer = "출력하고 싶은 문장"
google_tts(answer, "./audio/output.mp3")
playsound('./audio/output.mp3')