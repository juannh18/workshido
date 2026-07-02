# Generador de imagenes de worksheets con Gemini (Nano Banana) — tier gratuito.
# Uso:
#   python generate_worksheet_image.py "prompt del worksheet" nombre_salida
#   python generate_worksheet_image.py prompt.txt nombre_salida   (lee el prompt de un .txt)
# La imagen se guarda en C:\Users\juand\Downloads\<nombre_salida>.png

import sys, os, base64, json, requests
requests.packages.urllib3.disable_warnings()

GEMINI_API_KEY = 'AIzaSyD-rGuRCUjFKCIUk8yPAAw4EZOBLe4Q1Ao'
MODEL = 'gemini-2.5-flash-image'
DOWNLOADS = r'C:\Users\juand\Downloads'

def generate(prompt: str, out_name: str) -> None:
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_API_KEY}'
    body = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {
            'responseModalities': ['IMAGE', 'TEXT'],
            'imageConfig': {'aspectRatio': '2:3'},
        },
    }
    r = requests.post(url, json=body, timeout=300, verify=False)
    if r.status_code != 200:
        # reintento sin imageConfig por si el campo no esta soportado
        body['generationConfig'].pop('imageConfig', None)
        r = requests.post(url, json=body, timeout=300, verify=False)
    if r.status_code != 200:
        print(f'ERROR {r.status_code}: {r.text[:500]}')
        sys.exit(1)

    data = r.json()
    saved = False
    for cand in data.get('candidates', []):
        for part in cand.get('content', {}).get('parts', []):
            if 'inlineData' in part:
                img = base64.b64decode(part['inlineData']['data'])
                path = os.path.join(DOWNLOADS, f'{out_name}.png')
                with open(path, 'wb') as f:
                    f.write(img)
                print(f'OK imagen guardada: {path} ({len(img)//1024} KB)')
                saved = True
            elif 'text' in part:
                txt = part['text'].strip()
                if txt:
                    print(f'[texto del modelo] {txt[:300]}')
    if not saved:
        print('ERROR: la respuesta no trajo imagen.')
        print(json.dumps(data, indent=2)[:1000])
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(__doc__ or 'Uso: python generate_worksheet_image.py "<prompt>|prompt.txt" <nombre_salida>')
        sys.exit(1)
    arg, out = sys.argv[1], sys.argv[2]
    if arg.lower().endswith('.txt') and os.path.exists(arg):
        with open(arg, encoding='utf-8') as f:
            prompt = f.read()
    else:
        prompt = arg
    generate(prompt, out)
