import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath("F:/aisisterprogram.1/sshpython/SBV2/Style-Bert-VITS2"))

try:
    from style_bert_vits2.nlp.japanese import pyopenjtalk_worker as pyopenjtalk
    from style_bert_vits2.nlp.japanese.normalizer import normalize_text, replace_punctuation

    text = "わあ！兄さんも遊びに来てくださったの？"
    norm_text = normalize_text(text)
    print(f"Normalized text: {norm_text}")

    parsed = pyopenjtalk.run_frontend(norm_text)
    for parts in parsed:
        word = replace_punctuation(parts["string"])
        yomi = parts["pron"].replace("’", "")
        print(f"Word: {parts['string']} -> {word}, Yomi: {parts['pron']} -> {yomi}")

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
