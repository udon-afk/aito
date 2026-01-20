import sys
import os

# Adjust path to find style_bert_vits2 package
sys.path.append("F:\\aisisterprogram.1\\sshpython\\SBV2\\Style-Bert-VITS2")

from style_bert_vits2.constants import Languages
from style_bert_vits2.nlp import bert_models
import torch

print("Starting independent load test...")
try:
    print("Loading BERT model (CPU)...")
    bert_models.load_model(Languages.JP, device_map="cpu")
    print("BERT model loaded successfully.")
except Exception as e:
    print(f"Error loading BERT model: {e}")
