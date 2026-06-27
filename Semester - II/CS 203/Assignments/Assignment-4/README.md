# Assignment 4: PropTech Startup Strategy - Rent Prediction Pipeline

**Course**: Software Tools and Techniques for AI

**Total Marks**: 20

**Submission**: Submit your GitHub repository link containing all code, logs, and screenshots.

## Problem Statement: UrbanNest Analytics

You have just been hired as the Lead MLOps Engineer at **UrbanNest Analytics**, a fast-growing Property Technology (PropTech) startup. The company wants to launch a **Dynamic House Rent Prediction Engine** for four key cities: Mumbai, Pune, Delhi, and Hisar. 

Currently, the data science team has built a basic Random Forest model to predict rent (`price`), but as user demand grows, the startup faces two challenges:
1. **Cloud Computing Budgets:** Training large models exhaustively is too expensive. The founders want you to rigorously compare Hyperparameter Optimization techniques (Grid Search vs. Random Search vs. Bayesian Optimization) to find the most cost-effective method for achieving high accuracy without wasting compute time.
2. **Seamless Deployment:** The model needs to be accessible to end-users via a clean UI and safely packaged into Docker containers to avoid "it works on my machine" issues.

Your objective is to finalize the model optimization, track your experiments, build a user-friendly frontend, and deploy it all using Docker and Hugging Face Spaces.

## Dataset
You are provided with a dataset in the `Dataset` folder:
*   `train.csv`: Use this to train and perform Cross-Validation hyperparameter tuning.
*   `test.csv`: Use this to report your final model metrics.

**Important Note on Data:** The data contains categorical features like `city`, `Status`, and `property_type`. You must appropriately encode these into numerical formats before feeding them to the Random Forest model and ensure your Streamlit frontend reverses this mapping properly.

---

## Tasks & Mark Distribution 

### Task 1: Data Preprocessing, Optimization & Tracking (8 Marks)
**Goal:** Prove to the founders which optimization strategy gives the best "bang for buck" and systematically track all experimental runs.
*   **Experiment Tracking:** You must explicitly initialize and utilize `trackio` in your notebook to track all evaluation metrics, parameter variations, and model versions systematically across your different experiments.
*   **Preprocessing:** You must keep all features from the dataset for the final UI predictions. Create a preprocessing pipeline that converts string categorical variables (like `city`, `location`, `Status`, `property_type`) into numbers. You must strictly use `sklearn.preprocessing.LabelEncoder` or manual mapping and **save these mappings** so your frontend can use them later.
*   **Optimization Comparison:** Using strictly `train.csv` and 5-fold Cross-Validation tune the hyperparameters of a **Random Forest Regressor** (`sklearn.ensemble.RandomForestRegressor`). You must strictly implement and compare:
    1. **Grid Search** (using `sklearn.model_selection.GridSearchCV`)
    2. **Random Search** (using `sklearn.model_selection.RandomizedSearchCV`)
    3. **Bayesian Optimization** (using the `optuna` library, specifically creating a study with `optuna.create_study` and calling `.optimize`)
*   **Search Space Definition:** You **must** define your search spaces as follows to ensure a fair 60-trial budgeted comparison:
    *   **Grid Search Space (exactly 60 combinations):**
        *   `n_estimators`: `[50, 100, 150, 200]`
        *   `max_depth`: `[10, 15, 20, 25, 30]`
        *   `min_samples_split`: `[2, 5, 8]`
    *   **Random Search & Bayesian Optimization Space:**
        *   Search across the full integer ranges between the min and max bounds (choose max iterations to 60-100):
        *   `n_estimators`: Integer values from `50` to `200`
        *   `max_depth`: Integer values from `10` to `30`
        *   `min_samples_split`: Integer values from `2` to `10`
*   **Evaluation & Plots:** You must generate and **save** (in the `plots/` folder) the following plots:
    1.  `trials_vs_error.png`: A line plot comparing the compute budget vs. the error. 
        *   **X-axis:** Number of iterations/trials.
        *   **Y-axis:** Best mean cross-validation error found up to that iteration. 
        *   *Plot all three strategies (Grid, Random, Bayesian) overlaid on the same graph.*
    2.  `optuna_hyperparameter_space.png`: A plot of the hyperparameter space (using `optuna.visualization.plot_optimization_history` or `optuna.visualization.plot_contour`) to demonstrate how the Bayesian method explored the parameters.
*   **Final Testing & Reporting:** 
    *   Clearly **print/report** the best hyperparameters found by each of the three methods in your notebook.
    *   Retrain your overall *best* model (the one with the lowest CV error) on the entire `train.csv`. 
    *   Predict on the untouched `test.csv` and report the final Mean Absolute Error (MAE). 

**Expected Outputs for Task 1:**
*   `train.ipynb` notebook containing your preprocessing, Cross-Validation tuning, `trackio` integration, final evaluation on `test.csv`, clearly reported best hyperparameters, and plot generating code.
*   The `models/` folder containing the final saved model file (e.g., `best_rf_model.pkl`) and necessary preprocessing encoders.
*   The `plots/` folder containing the two requested PNG plot images (`trials_vs_error.png` and `optuna_hyperparameter_space.png`).
*   A screenshot named `trackio_dashboard.png` (in the `screenshots/` folder) showing your logging dashboard/UI with the compared hyperparameters and scores.

---

### Task 2: Web Application Development (4 Marks)
**Goal:** Build a user-facing dashboard for real estate agents.
*   **Frontend (Streamlit):** Build a standalone Streamlit dashboard. 
    *   Use `st.selectbox`, `st.number_input`, or `st.slider` for ALL input features corresponding to the dataset.
    *   Load your saved model and Label Encoders using `pickle.load` directly in the script.
    *   Upon button click (`st.button("Predict")`), apply the necessary preprocessing via your loaded encoders and invoke your model to get the prediction.
    *   Display the result using `st.success` or `st.write`.

**Expected Outputs for Task 2:**
*   `app.py` (Streamlit application code).
*   `requirements.txt` containing all required libraries (e.g., `streamlit`, `scikit-learn`, `trackio`, `optuna`).

---

### Task 3: Docker Containerization & Networking (4 Marks)
**Goal:** Package the application so it can be easily scaled and run anywhere.
*   **Dockerfile:** Write a single `Dockerfile` in the root repository spanning a Python base image setup for the Streamlit app. Ensure it installs requirements and uses the correct `ENTRYPOINT` or `CMD` to run `streamlit run app.py`. Make sure the container exposes the correct Streamlit port (typically `8501`).
*   **Port Forwarding:** When building and running the container, you must bind your local machine's port to the container's exported Streamlit port so that it is accessible via `localhost` (e.g., via the `-p` flag).

**Expected Outputs for Task 3:**
*   `Dockerfile` in the root repository.
*   A folder named `screenshots/` explicitly containing the following **three screenshots**:
    1.  `docker_build.png`: A screenshot showing the successful output of running your `docker build` command sequentially in your terminal.
    2.  `docker_ps.png`: A screenshot of the `docker ps` terminal command showing the container actively running with the correct port mappings.
    3.  `streamlit_working.png`: A screenshot of your web browser accessing the Streamlit app at `localhost:8501` to successfully get a prediction.

---

### Task 4: Cloud Deployment via Hugging Face Spaces (4 Marks)
**Goal:** Show stakeholders a live, working distributed prototype.
*   **Streamlit App Deployment:** Deploy your Streamlit application using a **Docker Space template** on Hugging Face. The Space will build your container (using your root `Dockerfile`) and give you a public URL.
*   The final Streamlit Space application must be publicly accessible and return predictions.

**Expected Outputs for Task 4:**
*   The **Streamlit Space URL** prominently placed at the very top of your GitHub repository's README.

---

## Submission Guidelines
Create a GitHub repository and push all your files. **Your repository MUST strictly be Private**. You must add your respective TA as a collaborator who will be taking your viva on the day of your submission so they can review your code.

Your repository MUST strictly look like this:

```text
Assignment_4/
├── README.md                 # Project description and HF Space URL
├── requirements.txt          # Python dependencies
├── train.ipynb               # Task 1: Tuning, trackio tracking, and Evaluation
├── app.py                    # Task 2: Streamlit application code
├── Dockerfile                # Task 3: Streamlit Dockerfile
├── models/
│   └── best_rf_model.pkl     # Task 1: Saved model and encoders
├── plots/
│   ├── trials_vs_error.png          # Task 1 plot
│   └── optuna_hyperparameter_space.png  # Task 1 plot
├── Dataset/                  # Provided CSVs
└── screenshots/
    ├── trackio_dashboard.png # Task 1 screenshot
    ├── docker_build.png      # Task 3 screenshot
    ├── docker_ps.png         # Task 3 screenshot
    └── streamlit_working.png # Task 3 screenshot
```

Submit the link to your GitHub repository when the google form is shared. Good luck, Lead Engineer!
