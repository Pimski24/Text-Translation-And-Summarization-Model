
#!/bin/bash

# Train a SentencePiece model for subword tokenization
cd /project/Text-Translation-And-Summarization-Model/nmt
python3 MT-Preparation/subwording/1-train_unigram.py summary.txt JRC-Acquis.en-nl.en-filtered.en

# Subword the dataset
python3 MT-Preparation/subwording/2-subword.py source.model target.model summary.txt JRC-Acquis.en-nl.en-filtered.en

# First 3 lines before subwording
head -n 3 summary.txt && echo "-----" && head -n 3 JRC-Acquis.en-nl.en-filtered.en

# First 3 lines after subwording
head -n 3 summary.txt.subword && echo "---" && head -n 3 JRC-Acquis.en-nl.en-filtered.en.subword

# Check if the GPU is active
nvidia-smi -L

# Translate the "subworded" source file of the test dataset
# Change the model name, if needed.
onmt_translate -model models/model.fren_step_15000.pt -src summary.txt.subword -output summary.translated -gpu 0 -min_length 1

# This one is just for reference
# Check the first 5 lines of the translation file
head -n 5 summary.translated

# Desubword the translation file
python3 MT-Preparation/subwording/3-desubword.py target.model summary.translated

# Check the first 5 lines of the desubworded translation file
head -n 5 summary.translated.desubword

# Evaluate the translation (without subwording)
python3 compute-bleu.py summary.txt summary.translated.desubword
