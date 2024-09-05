from fastapi import FastAPI
from transformers import AutoTokenizer, BartForConditionalGeneration
from typing import List, Dict
import torch

app = FastAPI()

model = BartForConditionalGeneration.from_pretrained("sshleifer_distilbart_cnn_12_6_dialoguesum")
tokenizer = AutoTokenizer.from_pretrained("sshleifer_distilbart_cnn_12_6_dialoguesum")
device = "cuda" if torch.cuda.is_available() else "cpu"

def generate_summaries(dialogue):
    model.eval()
    inputs = tokenizer(dialogue, return_tensors="pt", max_length=864, truncation=True).to(device)
    summary_ids = model.generate(inputs['input_ids'], max_length=160, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

@app.post("/summarize")
async def translate(dialogues: List[str]) -> Dict[str, List[str]]:
    summaries = []
    for dialogue in dialogues: summaries.append(generate_summaries(dialogue=dialogue))
    return {"summaries": summaries}