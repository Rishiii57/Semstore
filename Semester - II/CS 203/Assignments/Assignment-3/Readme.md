# Assignment 3: The "Multimodal Sentiment Engine" Challenge

**Total Marks:** 20

**Deadline:** 7:00 PM, 22th March, 2026

**Submission:** A zip file of the folder containing this notebook, and the csv/image files you will create.

---

## Background Story


**[Continuation from Assignment 2]**

The Smart Labeling Pipeline from Assignment 2 was a very good. Using that, the data team has prepared:

* 100 gold-standard labeled reviews [`gold_standard_100.csv`](./gold_standard_100.csv)
* 200+ weakly labeled reviews [`weak_labels_200.csv`](./weak_labels_200.csv)
* 150 LLM-labeled reviews [`llm_labels_150.csv`](./llm_labels_150.csv)

**All three datasets are provided to you by the instructor -- use them as-is.**


But your manager just announced a **new challenge**: The company is launching:

1. **Voice Review Feature:** Users can submit reviews via voice (like Amazon Alexa reviews).
2. **Multilingual Platform:** Expanding to the Indian market where 40% of users prefer Hindi.
3. **Robust Training:** The current 300 labeled samples aren't enough for production-grade sentiment analysis.

**Your New Objectives:**

* **Data Augmentation:** Expand your labeled dataset from 300 to 1000+ samples without human annotation.
* **Multimodal Support:** Generate synthetic audio reviews for testing the voice feature.
* **Multilingual:** Translate reviews to Hindi and validate sentiment preservation.
* **Quality Assurance:** Ensure augmented data maintains quality and doesn't introduce noise.

---

## Input Files & Provided Assets


All input datasets and evaluation assets are **provided by the instructor**. You must use these files directly -- do **not** use your own outputs from Assignment 2 or generate your own versions of these files.

**Provided Datasets (Do not modify these):**

* `gold_standard_100.csv`: Human-annotated gold standard (100 reviews, columns: `review`, `label`)
* `weak_labels_200.csv`: Weakly labeled reviews via Snorkel-style weak supervision (columns: `review`, `label`)
* `llm_labels_150.csv`: LLM-generated labels (150 reviews, columns: `review`, `label`)

**Provided Evaluation Assets (Do not modify these):**

* [`text_embedder.pt`](https://drive.google.com/file/d/1Yu7YDA4a2CDVUmVjH9vWUIT2aJCfyBKN/view?usp=sharing):  A frozen PyTorch Deep Learning model that converts text to numerical features.
* `evaluator.py`:  A Python script containing the `BlackBoxEvaluator` class to test your final datasets.

**Starter Notebook:**

* [`starter.ipynb`](./starter.ipynb): You can use this notebook as a starter template. You may upload it to Google COlab, or run everything locally.


---

## Tools & Libraries


You **must** use the following packages. Install them via the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

| Category | Packages |
|---|---|
| **Data & ML** | `pandas`, `numpy`, `scikit-learn`, `matplotlib` |
| **NLP & Text** | `nltk` (WordNet, tokenizer, POS tagger, BLEU) |
| **Translation** | `deep-translator` (GoogleTranslator -- free, no API key) |
| **LLM API** | `openai` (used with **OpenRouter** base URL) |
| **TTS** | `gTTS` (Google Text-to-Speech -- free) |
| **Audio Processing** | `librosa`, `soundfile` |
| **Speech-to-Text** | `openai-whisper` (local Whisper model -- free, no API key) |
| **Deep Learning** | `torch`, `transformers` (for the provided evaluator) |
| **Environment** | `python-dotenv` (to load your `.env` file) |

**API Setup:** You will use the **OpenRouter API** (`https://openrouter.ai/api/v1`) with the `openai` Python package. Store your API key in a `.env` file:

```
OPENROUTER_API_KEY=sk-or-...
```

Load it in your code with:

```python
from dotenv import load_dotenv
load_dotenv()
# Use as:
key = os.environ.get('OPENROUTER_API_KEY')
```

---

## Task 1: Data Consolidation & Classical Augmentation (5 Marks)

First, merge the provided labeled datasets. Then, use augmentation techniques.



### Requirements:

1. **Dataset Merging (Coding):**
* Combine `gold_standard_100.csv` + `weak_labels_200.csv` + a subset of `llm_labels_150.csv`.
* **Selection Strategy:** From `llm_labels_150.csv`, train a simple Logistic Regression baseline on `gold_standard_100.csv` (using TF-IDF features), then only include reviews where this baseline model has prediction confidence $\ge 0.65$ **AND** agrees with the LLM label.
* Remove exact duplicates based on review text.
* **Output:** `consolidated_base.csv` (should have 300-350 unique reviews).


2. **Class Distribution Analysis:**
* Count samples per sentiment (Positive, Negative, Neutral). Identify the **minority class**.


3. **Classical Augmentation (2 Methods):**
Implement these augmentation functions:
* **a) Synonym Replacement (using WordNet):** Replace 15-20% of words with synonyms. Preserve sentiment-bearing words (amazing, terrible, awful, excellent).
* **b) Back Translation:** Translate English $\rightarrow$ Hindi $\rightarrow$ English using `deep-translator` (`GoogleTranslator`).


4. **Application Strategy:**
* Apply both methods **only to the minority class** to balance the dataset.
* Generate **2 augmented versions** per minority sample (one from each method).


5. **Quality Filtering (Coding):**
* Calculate **Jaccard Similarity** between original and augmented. Reject if similarity $> 0.95$ or $< 0.30$.



**Deliverables:** `consolidated_base.csv`, `augmented_classical.csv`, `class_distribution.png`

---

## Task 2: LLM-Based Synthetic Review Generation (5 Marks)

Generate completely new synthetic reviews to further expand your dataset, ensuring diversity and quality.



### Requirements:

1. **Prompt Engineering:**
Design a **Few-Shot Prompt** that includes 3-4 example reviews from your gold standard. Instruct the model to output as JSON: `[{"review": "...", "sentiment": "Positive", "movie": "..."}]`
2. **API Integration:**
* Use the **OpenRouter API** (via the `openai` Python package) to generate in **batches of 20**. Generate a total of **300 synthetic reviews** (~150 Positive, ~100 Negative, ~50 Neutral).


3. **Diversity Metrics (Coding):**
* **Self-BLEU:** Calculate for each sentiment class separately. Lower = more diverse. Target: $Self-BLEU < 0.7$ per class.


4. **Sentiment Consistency Check:**
* Use your trained logistic regression baseline model (from Task 1) to predict the sentiment of each LLM-generated review.
* **Flag mismatches:** Store flagged reviews in `llm_generated_flagged.csv`.



**Deliverables:** `llm_generated_300.csv`, `llm_generated_flagged.csv`, `prompt_template.txt`, `diversity_report.txt`

---

## Task 3: Multilingual Sentiment Translation (4 Marks)

Expanding to India requires Hindi support. Translate reviews while preserving sentiment.

### Requirements:

1. **Strategic Sampling:** Select **100 reviews** (40 Pos, 40 Neg, 20 Neu) from your consolidated dataset. Prioritize shorter reviews to save API credits.
2. **Translation Pipeline:** Use `deep-translator` (`GoogleTranslator`) to translate from English to Hindi. This is free and requires no API key.
3. **Sentiment Preservation Check (Back-Translation):**

* Translate Hindi to English.
* Compute BLEU between original and back-translated English (Threshold: BLEU $\ge 0.3$).
* Use your sentiment model to check if the back-translated English yields the same prediction.

4. **Human-Like Validation:** Manually verify 5 random samples and document any systematic errors.

**Deliverables:** `bilingual_reviews.csv` (must include `bleu_score` and `quality_flag` columns).

---

## Task 4: Multimodal Audio Generation (4 Marks)

Users want to submit voice reviews. Generate synthetic audio data to test the voice pipeline.



### Requirements:

1. **Text-to-Speech Generation:**
* Select **30 reviews** (10 per class) of varying lengths.
* Use **gTTS** to generate `.wav` audio files (e.g., `tld="com"`).
* Convert the gTTS `.mp3` output to `.wav` using `librosa` + `soundfile`.


2. **Audio Feature Extraction:** Use `librosa` to extract: Duration, Spectral Centroid, Zero Crossing Rate, and MFCC mean (13 coefficients, averaged).
3. **Speech-to-Text Validation (Round-Trip Test):**
* Use **OpenAI Whisper** (`openai-whisper` package, `tiny` model) to transcribe audio back to text. This runs locally -- no API key needed.
* Compute **Word Error Rate (WER)** using word-level Levenshtein distance. Flag samples with WER > 0.25.

**Deliverables:** `audio_samples/` folder (30 `.wav` files), `audio_features.csv`, `audio_validation.csv`

---
## Task 5: Final Dataset Assembly & Model Evaluation (2 Marks)

Consolidate everything and prove the augmented data improves model performance using the provided Black-Box Evaluator.



### Requirements:

- **Dataset Assembly:** Merge `consolidated_base.csv`, `augmented_classical.csv`, `llm_generated_300.csv` (excluding flagged), and the **back-translated English** versions from `bilingual_reviews.csv` (i.e., the `back_translated` column: these are paraphrases that act as additional augmented samples). Deduplicate and save as `final_augmented_dataset.csv`.
 
### **The Proof is in the Metrics:**
 
* Import the `BlackBoxEvaluator` from the provided `evaluator.py`.
* This script uses a frozen PyTorch model (`text_embedder.pt`) to extract deep linguistic features without you needing to write any neural network code.
* Run the evaluator twice. First, passing your small `consolidated_base.csv` as the training data. Second, passing your massive `final_augmented_dataset.csv` as the training data.
* For both runs, use `gold_standard_100.csv` as your test data.

> **Note:** The evaluator automatically removes any test reviews from the training set to prevent data leakage. Since `gold_standard_100.csv` is used as both the test set and is part of `consolidated_base.csv`, the baseline run effectively trains on only the non-gold reviews (weak + filtered LLM labels). The accuracy improvement therefore measures whether your augmented data adds value beyond the weak labels alone.

