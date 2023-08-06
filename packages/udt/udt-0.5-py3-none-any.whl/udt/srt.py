from .finder import find, strip_dir
from .translate import get_google_access_token, trans_zh
import yaml
from os import path, mkdir, makedirs
import re
import glob

lesson_pat = re.compile(r'Lesson (\d+) ([\w\s]+)')

def read_csv(csv):
    r = []
    with open(csv) as f:
        for line in f:
            line = line.strip()
            if line:
                fields = line.split(',')
                r.append(fields)
    return r

def read_srt(srt):
    with open(srt) as f:
        content = f.read()
        paragraphs = re.split(r'\n\n', content)
        paragraphs = [re.split(r'\n', p.strip()) for p in paragraphs if p.strip() != '']
    return paragraphs

def get_lessons(root_dir, out_dir, silent=False, translate=False, google_access_token=None):
    lesson_csvs = find('*ubtitle*/*.csv', root_dir)

    lessons = list()
    srt_count = 0
    loss_count = 0
    para_count = 0
    for csv in lesson_csvs:
        r = lesson_pat.search(csv)
        lesson_num, lesson_title = int(r.group(1)), r.group(2)
        lesson_label = 'Lesson{}-{}'.format(lesson_num, lesson_title)
        lesson_dir = path.dirname(csv)
        lesson_srts = read_csv(csv)
        lesson_texts = list()

        lesson_out_dir = _mkdir(out_dir, 'Lesson{}'.format(lesson_num))

        lesson_readme = path.join(lesson_out_dir, 'README.md')
        with open(lesson_readme, 'w') as f:
            f.write('## Lesson{}\n'.format(lesson_num))
        # lesson_srts = find('*.srt', lesson_dir)
        # lesson_srts = [path.basename(srt) for srt in lesson_srts]
        for i, srt in enumerate(lesson_srts):
            srt_title = srt[0]
            srt_file = '{}.srt'.format(srt[1])
            srt_path = path.join(lesson_dir, srt_file)

            if not path.isfile(srt_path):
                if not silent:
                    print('lossing {}/{}'.format(lesson_label, srt_file))
                loss_count += 1
            else:
                srt_data = read_srt(srt_path)
                lesson_texts.append(srt_data)
                out_file = path.join(lesson_out_dir, '{}-{}.md'.format(i+1, srt[1]))
                with open(lesson_readme, 'a') as f:
                    f.write('* [{}]({})\n'.format(i+1, out_file.replace('udtout/', '')))
                with open(out_file, 'w') as f:
                    pass
                with open(out_file, 'a') as f:
                    for s in srt_data:
                        en_text = s[2]
                        if translate:
                            cn_text = trans_zh(en_text, google_access_token)
                            print("en: {}\ncn: {}\n".format(en_text, cn_text))
                        else:
                            cn_text = '请在此填写中文翻译'
                        md_para = "#### {}\nCN: {}\n\n".format(en_text, cn_text)
                        f.write(md_para)
                        para_count += 1

        lessons.append((lesson_num, lesson_label, lesson_dir, lesson_srts, lesson_texts))
        srt_count += len(lesson_srts)
    lessons = sorted(lessons, key=lambda x: x[0])

    if not silent:
        print()
        print(yaml.dump(
            [[lesson[1], lesson[3]] for lesson in lessons]
        ))

        print('lesson total: {}'.format(len(lessons)))
        print('   srt total: {}'.format(srt_count))
        print('  loss count: {}'.format(loss_count))
        print('  text count: {}'.format(para_count))

    return lessons

def get_lesson_srt(lessons, lesson_th, srt_th):
    lesson_num = len(lessons)
    if lesson_th > lesson_num:
        return []
    lesson = lessons[lesson_th-1]
    srt_num = len(lesson[4])
    if srt_th > srt_num:
        return []
    srt_title = lesson[3][srt_th-1][0].strip('b|\'')
    print('{}/{}'.format(lesson[1], srt_title))
    return lesson[4][srt_th-1]

def srt2md(srt):
    pass

def _mkdir(root_dir, sub_dir):
    _dir = path.join(root_dir, sub_dir)
    if not path.isdir(_dir):
        makedirs(_dir)
    return _dir

def makeout(sub_dir=''):
    out_dir = 'udtout'
    if not path.isdir(out_dir):
        mkdir(out_dir)
    out_dir = path.join(out_dir, sub_dir)
    if not path.isdir(out_dir):
        makedirs(out_dir)
    return out_dir

def run(root_dir, lesson_th=None, srt_th=None, translate=False, google_access_token=None):
    out_dir = makeout(root_dir.replace(' ', ''))

    silent = False
    if lesson_th and srt_th:
        silent = True

    lessons = get_lessons(root_dir, out_dir, silent, translate=translate, google_access_token=google_access_token)

    if silent:
        print(yaml.dump(
            get_lesson_srt(lessons, lesson_th, srt_th)
        ))

def srt(argv):
    root_dir = ''
    lesson_th = None
    srt_th = None
    if len(argv) > 0: root_dir = argv[0]
    if len(argv) > 1: lesson_th = int(argv[1])
    if len(argv) > 2: srt_th = int(argv[2])

    if root_dir != '':
        run(root_dir, lesson_th, srt_th)
    else:
        parts = glob.glob('Part*')
        for part in parts:
            run(part)

def tsrt(argv):
    google_access_token = get_google_access_token()
    parts = glob.glob('Part*')
    for part in parts:
        run(part, translate=True, google_access_token=google_access_token)
