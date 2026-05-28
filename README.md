# 🇵🇰 Urdu LLM — Pakistan's First Fine-tuned Urdu Language Model

> Fine-tuned Llama 3.2 on a Pakistani corpus — Urdu news, literature, Islamic knowledge, history & culture

[![HuggingFace](https://img.shields.io/badge/HuggingFace-Model-yellow)](https://huggingface.co/nimra-pixel/urdu-llama-pakistan)
[![Streamlit](https://img.shields.io/badge/Streamlit-Demo-red)](https://streamlit.io)
[![Colab](https://img.shields.io/badge/Google_Colab-Notebook-orange)](https://colab.research.google.com)

## What is this?

Pakistan's first open-source Urdu LLM — Llama 3.2-1B fine-tuned on a Pakistani corpus using QLoRA.

## Training Data
- 📰 Urdu news articles
- 📚 Urdu literature & poetry (Iqbal, Ghalib, Mir, Faiz)
- 🕌 Islamic knowledge (Quran, Hadith, jurisprudence)
- 🏛️ Pakistani history & culture
- 💬 Code-switching (Urdu+English)
- 🎓 Pakistani education (CSS, MDCAT)

## Fine-tuning Method
- **Base model:** meta-llama/Llama-3.2-1B-Instruct
- **Method:** QLoRA (4-bit quantization + LoRA)
- **LoRA rank:** r=16, alpha=32
- **Epochs:** 3
- **Platform:** Google Colab (free T4 GPU)

## Files
| File | Purpose |
|---|---|
| `urdu_llm_finetune.ipynb` | Google Colab fine-tuning notebook |
| `app.py` | Streamlit demo — chat with the model |
| `requirements.txt` | Demo app dependencies |

## Quick Start (Demo)
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Fine-tune yourself
1. Open `urdu_llm_finetune.ipynb` in Google Colab
2. Set Runtime → GPU (T4)
3. Run all cells
4. Model pushed to your HuggingFace automatically

## Use the model
```python
from transformers import pipeline
pipe = pipeline('text-generation', model='nimra-pixel/urdu-llama-pakistan')
print(pipe('پاکستان کی تاریخ بتائیں'))
```

## Built by
**Nimra** — AI Engineer & Assistant Professor, Superior University
