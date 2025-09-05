# TOC Extraction Fine-Tuning Pipeline

This project focuses on using fine-tuning to improve the performance of a small LLM (0.6B parameters) on a challenging task: producing structured output. Specifically, the model is trained to extract relevant information from books’ tables of contents—including title, start page, and end page—in JSON format. This task is particularly difficult for small models due to the high variability in the layout of books’ tables of contents.

This repository provides a complete pipeline for fine-tuning language models to extract structured tables of contents (TOC) from noisy, real-world documents. Using parameter-efficient LoRA fine-tuning, the project transforms imperfect TOC text into clean, structured JSON format.

## What It Does

Fine-tunes **Qwen3-0.6B** to robustly parse messy table of contents and extract:
- Chapter numbers and titles
- Start and end page ranges  
- Clean JSON structure from noisy inputs

The model learns to handle OCR artifacts, formatting inconsistencies, random characters, and missing information commonly found in real document TOCs.

## Results

**Before Fine-tuning**: Base model struggles with page ranges and noisy inputs
```json
{"chapter_number": 1, "start_page": 25, "end_page": 25}  // ❌ Missing page range
```

**After Fine-tuning**: Properly calculates page ranges and handles noise
```json
{"chapter_number": "1", "start_page": 25, "end_page": 67}  // ✅ Correct end_page calculation
```

## Pipeline Overview

### 1. **Data Processing** (`load_distilled_data.ipynb`)
- Converts LLM-distilled `.docx` files to structured JSON
- Processes chapter-based content with consistent formatting

### 2. **Synthetic Data Generation** (`generate_synthetic_data.ipynb`)  
- Creates 15,000 training examples with configurable noise parameters
- Applies realistic document extraction errors (OCR artifacts, formatting issues)
- Generates paired examples: noisy TOC → clean JSON

### 3. **Model Fine-Tuning** (`finetuning.ipynb`) 
- Uses **LoRA** (Low-Rank Adaptation) for parameter-efficient training
- Optimized for **Google Colab** with 4-bit quantization
- Exports models in multiple formats:
  - 16-bit merged model for maximum quality
  - 4-bit GGUF for efficient deployment

### 4. **Benchmarking** (`models_benchmarking.ipynb`)
- Side-by-side comparison of base vs fine-tuned models
- Demonstrates improved page range calculation and noise handling

## Quick Start

### Prerequisites
- Google Colab account with GPU runtime
- Hugging Face account (for model access)

### Option 1: Use Pre-generated Data
Pre-generated synthetic training data is available in the `data/` folder. You can directly proceed to fine-tuning.

### Option 2: Generate New Data
Run `generate_synthetic_data.ipynb` locally to create custom training data with your own noise parameters.

### Fine-tuning & Benchmarking (Colab Optimized)

**Important**: The following notebooks are optimized for Google Colab and should be run there:

1. **Fine-tune the Model**:
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DavidePanza/finetuning_LLM_for_Chapter_Extraction/blob/main/notebooks/finetuning.ipynb)

2. **Benchmark Performance**:
   [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/DavidePanza/finetuning_LLM_for_Chapter_Extraction/blob/main/notebooks/models_benchmarking.ipynb)

### Pre-trained Model

A fine-tuned 16-bit merged version is available on Hugging Face:
🤗 [Fine-tuned TOC Extractor Model](https://huggingface.co/davidepanza/qwen3-0.6b-instruct-chapter-extraction)

## Project Structure

```
├── notebooks/
│   ├── load_distilled_data.ipynb       # DOCX → JSON processing
│   ├── generate_synthetic_data.ipynb   # Synthetic training data
│   ├── finetuning.ipynb               # LoRA fine-tuning (Colab optimized)
│   └── models_benchmarking.ipynb      # Performance comparison (Colab optimized)
├── src/                               # Supporting Python modules
├── data/                              # Pre-generated training data
├── synthetic_data/                    # Generated data and models
└── README.md
```

## Use Cases

- **Document Processing Pipelines**: Extract chapter structure from academic papers, technical manuals
- **Digital Library Systems**: Automatically structure document collections  
- **Publishing Workflows**: Process manuscripts with inconsistent formatting
- **Research Applications**: Handle noisy OCR outputs from scanned documents

## Technical Details

- **Base Model**: Qwen3-0.6B (4-bit quantization)
- **Training Method**: LoRA adapters (r=16, α=32)
- **Dataset**: 15,000 synthetic examples with configurable noise
- **Training Time**: ~1-2 hours on Colab T4 GPU
- **Memory Efficient**: 4-bit quantization + gradient checkpointing

## Performance Improvements

The fine-tuned model demonstrates significant improvements:
- ✅ **Accurate page range calculation** (end_page = next_start_page - 1)
- ✅ **Noise resistance** to formatting inconsistencies and OCR errors  
- ✅ **Consistent JSON output** with required fields
- ✅ **Content filtering** ignores exercises, decorative elements, standalone numbers

<!-- ## 🤝 Contributing

Contributions welcome! You can:
- Add your own `.docx` files to extend the dataset
- Adjust noise parameters for different use cases
- Experiment with other base models or fine-tuning approaches

---

**Ready to fine-tune?** Click the Colab badges above to get started! 🚀 -->