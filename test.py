from transformers import AutoTokenizer, BartForConditionalGeneration
from datasets import load_dataset
from rouge_score import rouge_scorer
import numpy as np

# Load the tokenizer and model from your local path
model_path = "sshleifer_distilbart_cnn_12_6_dialoguesum"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = BartForConditionalGeneration.from_pretrained(model_path)

dialogsum = load_dataset("knkarthick/dialogsum")

samples = dialogsum['validation'][:30]  # Adjust index to sample specific rows if needed

def evaluate_summaries(samples):
    references = [sample for sample in samples['summary']]
    inputs = [sample for sample in samples['dialogue']]
    
    summaries = []
    for input_text in inputs:
        inputs_tokenized = tokenizer.encode(input_text, return_tensors="pt", truncation=True, max_length=1024)
        summary_ids = model.generate(inputs_tokenized, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        summaries.append(summary)
    
    # Calculate ROUGE scores
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge_scores = [scorer.score(ref, hyp) for ref, hyp in zip(references, summaries)]
    
    # Calculate average ROUGE scores
    avg_rouge1 = np.mean([score['rouge1'].fmeasure for score in rouge_scores])
    avg_rouge2 = np.mean([score['rouge2'].fmeasure for score in rouge_scores])
    avg_rougeL = np.mean([score['rougeL'].fmeasure for score in rouge_scores])
    
    print(f"Average ROUGE-1 Score: {avg_rouge1:.4f}")
    print(f"Average ROUGE-2 Score: {avg_rouge2:.4f}")
    print(f"Average ROUGE-L Score: {avg_rougeL:.4f}")

evaluate_summaries(samples)
