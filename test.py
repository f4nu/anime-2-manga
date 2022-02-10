import cv2
import re
import json
from PIL import Image, ImageFont, ImageDraw
from kanji import get_tokens


def parse_time(time_string):
    hours = int(re.findall(r'(\d+):\d+:\d+,\d+', time_string)[0])
    minutes = int(re.findall(r'\d+:(\d+):\d+,\d+', time_string)[0])
    seconds = int(re.findall(r'\d+:\d+:(\d+),\d+', time_string)[0])
    milliseconds = int(re.findall(r'\d+:\d+:\d+,(\d+)', time_string)[0])

    return (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds


def parse_srt(srt_string):
    srt_list = []

    for line in srt_string.split('\n\n'):
        if line != '':
            index = int(re.match(r'\d+', line).group())

            pos = re.search(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+',
                            line).end() + 1
            content = line[pos:]
            start_time_string = re.findall(
                r'(\d+:\d+:\d+,\d+) --> \d+:\d+:\d+,\d+', line)[0]
            end_time_string = re.findall(
                r'\d+:\d+:\d+,\d+ --> (\d+:\d+:\d+,\d+)', line)[0]
            start_time = parse_time(start_time_string)
            end_time = parse_time(end_time_string)

            srt_list.append({
                'index': index,
                'content': content,
                'start': start_time,
                'end': end_time
            })

    return srt_list


srt = open('input/19.srt', 'r', encoding="utf-8").read()
subtitles = parse_srt(srt)

vidcap = cv2.VideoCapture('input/19.mkv')

if (vidcap.isOpened() == False):
    print("Error opening the video file")
else:
    # Get frame rate iformation
    width = int(vidcap.get(3))
    height = int(vidcap.get(4))
    fps = float(vidcap.get(5))
    print("Frame Rate:", fps, "frames per second")	
    print(width, "x", height)

    # Get frame count
    frame_count = int(vidcap.get(7))

    print("Frame count:", frame_count)

    font = ImageFont.truetype('fonts/NotoSansJP-Regular.otf', 48)
    furigana_font = ImageFont.truetype('fonts/NotoSansJP-Regular.otf', 18)
    stroke_width = 3
    furigana_stroke_width = 2
    spacing = 15
    count = 0
    for subtitle in subtitles:
        msToAdd = (subtitle['end'] - subtitle['start']) / 2
        subtitleContent = subtitle['content']
        tokens = get_tokens(subtitleContent)

        vidcap.set(cv2.CAP_PROP_POS_MSEC, subtitle['start'] + msToAdd)
        success, image = vidcap.read()
        fileName = "output/frame-%d.jpg" % count
        cv2.imwrite(fileName, image)

        with Image.open(fileName) as img:
            d = ImageDraw.Draw(img)
            w, h = d.textsize(subtitleContent, font)
            x = (width / 2) - (w / 2)
            y = height - (h) - (height / 20)
            print(subtitleContent, w, h, x, y)
            d.text(
                (x, y),
                subtitleContent,
                font=font,
                fill=(255, 255, 255),
                stroke_width=stroke_width,
                stroke_fill=(0, 0, 0),
                spacing=spacing,
            )

            for token in tokens:
                print(token)
                hiragana_text = token['hiragana']
                furigana_w, furigana_h = d.textsize(hiragana_text, furigana_font)
                morpheme_w, morpheme_h = d.textsize(token['surface'], font)
                string_until_morpheme = subtitleContent[:token['begin']]
                number_of_newlines = string_until_morpheme.count("\n")
                if number_of_newlines > 0:
                    regex = r'^(.*?\n){' + str(number_of_newlines) + '}'
                    regex_pattern = re.compile(regex) 
                    string_until_morpheme = re.sub(regex_pattern, '', string_until_morpheme)
                    print('text_after', string_until_morpheme);
                    print('regex', regex)

                start_x, start_y = d.textsize(string_until_morpheme, font)
                print('newlines', number_of_newlines)
                print('hiragana', hiragana_text)
                print('string_until', string_until_morpheme)
                print('furigana_w/h', furigana_w, furigana_h)
                print('morpheme_w/h', morpheme_w, morpheme_h)
                print('start_x/y', start_x, start_y)
                d.text(
                    (x + start_x + (morpheme_w / 2) - (furigana_w / 2), y - 15 + (morpheme_h * number_of_newlines) + ((spacing * 1.2) * number_of_newlines)),
                    hiragana_text,
                    font=furigana_font,
                    fill=(255, 255, 255),
                    stroke_width=furigana_stroke_width,
                    stroke_fill=(0, 0, 0),
                )
                print('')

            img.save("output/19-%d.jpg" % count)

        count += 1
        if count > 200:
            exit()

vidcap.release()
cv2.destroyAllWindows()
