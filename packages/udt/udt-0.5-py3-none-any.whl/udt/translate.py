import requests
import subprocess

def get_google_access_token():
    shell_cmd = "gcloud auth application-default print-access-token"
    try:
        # exit_code = subprocess.call(shell_cmd, shell=True)
        shell_out = subprocess.check_output(shell_cmd, shell=True)
    except CalledProcessError:
        print("未安装 google cloud cli !!!")
        exit(0)
    return str(shell_out).strip("b|'").replace('\\n', '')

def google_translate(q, google_access_token, target='zh', source='en'):
    url = 'https://translation.googleapis.com/language/translate/v2'
    headers = {
        'Authorization': 'Bearer {}'.format(google_access_token)
    }
    data = {
        'q': q,
        'source': source,
        'target': target,
        'format': 'text'
    }
    r = requests.post(url, data=data, headers=headers)

    if r.status_code != 200:
        print('http request failed!!!')
        exit(0)
    return r.json()['data']['translations'][0]['translatedText']

def translate(argv):
    if len(argv) > 0: q = argv[0]
    else:
        print('udt -t en_text')
        exit(0)

    google_access_token = get_google_access_token()

    translate_text = google_translate(q, google_access_token)

    print(translate_text)

    return translate_text

def trans_zh(en_text, google_access_token):
    translate_text = google_translate(en_text, google_access_token)

    return translate_text
