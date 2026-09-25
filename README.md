# Project JarvisBox

A plan for a desk-sized, voice-controlled AI assistant on a Raspberry Pi: wake word, speech-to-text, an LLM, text-to-speech, and a bit of personality through LEDs, a servo and a small OLED face.

> **Status: design and application skeleton. It does not run yet.** The repository contains the main loop (`main.py`) that wires the components together, but the modules it imports (`core/`, `hardware/`, `utils/`) are not in the repository, and `requirements.txt` and `settings.yaml` are empty.

## Why

Smart speakers are closed and cloud-bound; chat assistants live in a browser tab. JarvisBox aims for something in between: a standalone terminal that listens for "Hey Jarvis", answers with an LLM (cloud or local), can automate tasks on your machine, and physically reacts, turning toward the speaker and showing its state on LEDs and a tiny screen.

## What exists today

[`main.py`](./main.py) defines the `JarvisBox` class and its main loop:

1. Load `config/settings.yaml` and a `.env` file.
2. Initialize hardware (`LEDController`, `ServoController`, `DisplayController`) and AI components (`WakeWordDetector`, `SpeechToTextEngine`, `TextToSpeechEngine`, `LLMInterface`).
3. Loop: wait for the wake word, turn the servo toward the speaker, record and transcribe speech, send it to the LLM, show a short version on the display, speak the reply, return to idle.
4. On `SIGINT`/`SIGTERM`, release the hardware and exit.

It expects these modules, none of which exist yet:

```
core/wake_word.py            WakeWordDetector
core/speech_to_text.py       SpeechToTextEngine
core/text_to_speech.py       TextToSpeechEngine
core/llm_interface.py        LLMInterface
hardware/led_controller.py   LEDController
hardware/servo_controller.py ServoController
hardware/display_controller.py DisplayController
utils/logging_utils.py       setup_logger
config/settings.yaml         (the repo's settings.yaml is at the root and empty)
```

It also needs `python-dotenv` and `PyYAML`.

## Planned features

**AI**
- Voice conversation through the OpenAI API or a local model
- Long-term memory and personalization
- Calendar, weather and task queries
- Plugin-style agents (file parsing, market scans and similar)

**Voice**
- Wake word (`Hey Jarvis`) with passive listening
- Speech-to-text with noise handling (Whisper, Deepgram or similar)
- Natural text-to-speech (ElevenLabs or Coqui)

**Automation**
- Open apps, write scripts, Git integration
- Home Assistant and IoT hooks
- Repo scaffolding, commit summaries, file watching

**On-device (stretch)**
- Quantized local LLMs (Mistral, Llama 3 via Ollama)
- Offline fallback mode

**Physical expressiveness**
- LED ring for mood and confidence
- Servo that turns toward the speaker
- OLED face for expressions, waveforms or info
- Proximity and motion sensing

## Hardware plan

- Raspberry Pi 5 (or Jetson Nano, or a local API node)
- ReSpeaker 2-Mic Array or a USB microphone
- Speaker (wired or Bluetooth)
- 0.96" I2C OLED display, optional webcam
- Servo, RGB LED strip, optional NFC tag switch

## Planned software stack

Python for the core, Node.js for hardware bridges if needed, OpenAI or Ollama for the LLM, Whisper and Coqui TTS for speech, MQTT for hardware messages, and Flask or FastAPI for a local API.

## Roadmap

- [x] Main application loop and component interfaces (`main.py`)
- [ ] Core modules: wake word, STT, TTS, LLM interface
- [ ] Hardware drivers: LEDs, servo, OLED
- [ ] Config file and dependency list
- [ ] Local LLM fallback
- [ ] Long-term memory via a vector database
- [ ] Mood switching and personalities
- [ ] Demo video

## Contributing

The quickest way to get this talking is to implement the four `core/` modules with simple backends (for example `openai-whisper`, `pyttsx3` and an OpenAI or Ollama client) and stub out the hardware classes so it can run on a laptop first.
