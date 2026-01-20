import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.abspath("F:/aisisterprogram.1/sshpython/SBV2/Style-Bert-VITS2"))

try:
    from style_bert_vits2.nlp.japanese.g2p import g2p
    from style_bert_vits2.nlp.japanese.normalizer import normalize_text

    text = "わあ！兄さんも遊びに来てくださったの？"
    norm_text = normalize_text(text)
    print(f"Normalized text: {norm_text}")

    phones, tones, word2ph = g2p(norm_text)
    print("g2p Successful!")
    print(f"Phones: {phones}")

except ImportError as e:
    print(f"ImportError: {e}")
except Exception as e:
    print(f"Error: {e}")
