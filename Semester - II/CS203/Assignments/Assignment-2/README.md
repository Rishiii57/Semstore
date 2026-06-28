# **Assignment 2: The "Smart Labeling Pipeline" Challenge**

**Total Marks: 20**

**Deadline: 7:00 PM, 15th February, 2026**

Build a cost-effective, high-quality labeling pipeline using human annotation, programmatic rules, and LLMs before funding runs out.

**Dataset:** Set of 300 reviews from the provided IMDB dataset. 

**Reference Notebook:** Find the jupyter notebook, hosted at github. 

**Tools:** Label Studio, Python (pandas, numpy, sklearn, snorkel, modAL, cleanlab).

---

## **Task 1: The Human as Annotator**

**Objective:** Establish a "Gold Standard" dataset and measure human consensus.

1. **Label Studio Setup:**  
   * Host Label Studio locally. Create a folder, and make a virtual environment in that folder. Install Label Studio in your virtual environment and launch it (`label-studio start`). Label studio should open in your default browser; if not, paste the localhost URL provided in the console into your favourite browser.  
   * Create a project in Local Studio (name it as “Movie\_Sentiments”).  
   * Import the provided movie\_reviews\_300.csv.  
   * Choose an NLP template task named “Text Classification”. Write an XML config such that the available labels are (single choice): Positive, Negative, and Neutral, and the review texts come from the review column in movie\_reviews\_300.csv. You can do this directly in the GUI (do not change the column names in your provided CSV).  
2. **Distributed Annotation:**  
   * **Roles:** Since your group has at least 3 members, assign among yourselves as Annotator A (Student 1), Annotator B (Student 2), and Annotator C (Student 3).  
   * **Action:** Annotators A, B & C label the **first 100 reviews** independently.  
   * **Deliverable:** Export all annotation sets as CSV annotator\_a.csv, annotator\_b.csv, annotator\_c.csv  
3. **Metrics Implementation (Coding):**  
   * Write a script (Python function) to parse csv file into Pandas DataFrames.  
   * Implement **Fleiss’ Kappa** from scratch (no library) to measure agreement between 3 raters.  
   * Compare the result with the statsmodels implementation.  
4. **Conflict Resolution (Coding):**  
* Compare labels from Annotator A, B, and C for the same movie.  
* **Identify Conflicts:** Any review where the three annotators do not unanimously agree.  
* **Print Samples:** Display 5 examples of conflicting reviews (show what A, B, and C each said).  
* **Adjudication Logic (Automated):**  
  * **Majority Vote:** If 2 annotators agree, use their label.  
  * **Tie-Breaker:** If all 3 differ (e.g., Positive vs. Negative vs. Neutral), assign **"Neutral"**.  
* **Outcome:** Save the final resolved labels to `gold_standard_100.csv`

**\[Refer to Jupyter Notebook Section: Task 1\]**

---

## **Task 2: Weak Supervision (The "Lazy" Labeler)**

**Objective:** Label the next 200 reviews programmatically to save time.

1. **Heuristic Development:**  
   * Analyze gold\_standard\_100.csv for patterns.  
   * Write at least **3 Python Heuristic Functions** (e.g., regex for "horrible", length checks).  
   * **Action:** Apply to the **remaining** 200 unlabeled reviews.  
2. **Snorkel Implementation:**  
   * Wrap heuristics as Snorkel @labeling\_functions.  
   * **Metric:** Report **Coverage** (percentage of data labeled) and **Conflict Rate** ( If Rule A says "Positive" and Rule B says "Negative" for the same review, that is a conflict.).  
3. **Adjudication:**  
   * Use Majority Vote to generate probabilistic labels (weak labels) for the 200 reviews.  
   * **Deliverable:** weak\_labels\_200.csv.

**\[Refer to Jupyter Notebook Section: Task 2\]**

---

## **Task 3: Active Learning (The Budget Optimizer)**

**Objective:** Simulate cost savings by training a model iteratively.

1. **Setup:**  
   * **Seed:** Use gold\_standard\_100.csv.  
   * **Pool:** The 200 weakly labeled reviews (treat labels as hidden/unknown for simulation).  
2. **Query Strategy Implementation (Coding):**  
   * Implement **Least Confidence (uncertainty)** and **Entropy Sampling** from scratch.  
3. **Iterative Loop:**  
   * Train LogisticRegression on Seed.  
   * **Loop (5 iterations):**  
     * Select top 10 uncertain samples from Pool using your strategy.  
     * "Label" them (reveal ground truth from dataset).  
     * Add to Train set, Retrain model.  
     * Log Test Accuracy.  
4. **Visualization:**  
   * Plot **Learning Curve**: Number of Labels (X) vs. Accuracy (Y).  
   * Compare **Active Learning** vs. **Random Sampling**.

**\[Refer to Jupyter Notebook Section: Task 3\]**

---

## **Task 4: AI vs. AI (LLM & Noise Detection)**

**Objective:** Use LLMs for bulk labeling and detect hallucinations.

1. **LLM Pipeline:**  
   * **Prompt Engineering:** Design a **Few-Shot Prompt** (include 3 examples from gold\_standard\_100).  
   * **Action:** Send remaining unlabeled samples from Pool (approx 150\) to Gemini API (Free Tier) and extract labels in a csv file.  
   * **Output:** llm\_labels\_150.csv.  
2. **Noise Hunting (Cleanlab Logic):**  
   * Train your simple Logistic Regression on the llm\_labels\_150.csv  
   * **Coding:** Identify "High Confidence Disagreements".  
   * **Criteria:** Model Probability \> 0.90 for Class A, but LLM Label is Class B.  
   * **Deliverable:** Print the top 5 suspicious reviews.

**\[Refer to Jupyter Notebook Section: Task 4\]**

**\[Submission\]**

* Submit the completed **Jupyter Notebook**.  
* Include, your label-studio annotation interface screenshot.  
* Include annotator\_a.csv, annotator\_b.csv, annotator\_c.csv, gold\_standard\_100.csv , weak\_labels\_200.csv and llm\_labels\_150.csv.  
* **Zip** all resources as a single file and submit it to the asked google form (It will be circulated towards the end of deadline)

