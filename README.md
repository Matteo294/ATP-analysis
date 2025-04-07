# 🎾 ATP Data Analysis & Match Outcome Prediction

This repository presents an end-to-end data science project based on ATP tennis data.

The project is divided into two main parts:
- [Part One](#part-one-exploratory-data-analysis): exploratory data analysis (EDA) on player statistics.
- [Part Two](#part-two-machine-learning-model): building a machine learning model to study Novak Djokovic's performance and predict match outcomes.

---

## Part One – Exploratory Data Analysis

The goal of this section is to answer a few data-driven questions using ATP match statistics.

### ❓ Key Questions:
1. Which player has the most efficient serve?
2. How do players perform across different court surfaces? Does surface specialization affect rankings?
3. How have players’ performances evolved in recent years? Who has shown the greatest improvement or decline?

---

### 📊 Question 1 – Serve Efficiency
We explore serve statistics across a selected group of players.
  
![Serve stats](analysis/figures/serve_labeled.png "Serve stats")

---

### 📊 Question 2 – Surface Comparison & Match Distribution  
**Status: In progress**  
Exploration of win rates on different surfaces (hard, clay, grass) and their impact on overall performance and rankings.

![wr stats](analysis/figures/winrate_per_year.png "Win rate per year")  
![Court wr stats](analysis/figures/court_winrates.png "Court surface win rates")

---

### 📊 Question 3 – Performance Trends Over Time  
**Status: In progress**  
We aim to analyze year-over-year player evolution in performance metrics.

---

## Part Two – Machine Learning Model

This section focuses on training a binary classifier to predict match outcomes based on Novak Djokovic's historical stats.

### ⚙️ Model Summary

| Algorithm       | Train Accuracy | Test Accuracy |
|----------------|----------------|---------------|
| SVM             | 0.93           | 0.93          |
| Logistic Regression | 0.91      | 0.92          |
| Decision Tree   | 0.92           | 0.96          |

> 📌 Note: More models and cross-validation results may be added in future updates.

---

## 🛠️ Tools & Technologies

- Python, Pandas, Plotly
- Scikit-learn
- Jupyter Notebooks
- Git & GitHub

---

## 🚧 Work in Progress

Future updates will include:
- Full EDA for surface-based insights
- Feature importance analysis
- A simple API or dashboard to interact with the model

---

## 📂 Repository Structure
analysis/ ├── figures/ └── notebooks/ model/ ├── training/ └── evaluation/ README.md
