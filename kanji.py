from sudachipy import tokenizer
from sudachipy import dictionary
from wanakana import to_hiragana, is_japanese, is_katakana, is_hiragana
import string

tokenizer_obj = dictionary.Dictionary(dict="small").create()

def tokenize_furigana(text):
    tokens = [m for m in tokenizer_obj.tokenize(text, tokenizer.Tokenizer.SplitMode.C)]
    return tokens

JAPANESE_PUNCTUATION = '　〜！？。、（）：「」『』０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ'

def is_japanese_extended(text):
    return is_japanese(text) and text not in string.punctuation and text not in JAPANESE_PUNCTUATION

def get_tokens(text):
    token_parts = []
    for token in tokenize_furigana(text):
        should_parse = is_japanese_extended(token.surface()) and not is_katakana(token.surface()) and not is_hiragana(token.surface())
        if should_parse:
            token_parts.append(
                {
                    'token': token,
                    'begin': token.begin(),
                    'end': token.end(),
                    'surface': token.surface(),
                    'reading_form': token.reading_form(),
                    'hiragana': to_hiragana(token.reading_form())
                }
            )

    return token_parts
