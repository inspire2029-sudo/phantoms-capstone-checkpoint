# PHANTOMS Capstone Checkpoint

Complete end-to-end ML checkpoint: Kaggle API → SQLite → cleaning → encoding → model comparison → evaluation → model decision.

## Models
- Logistic Regression
- Decision Tree
- Neural Network (MLP)

## Evaluation
Accuracy, Precision, Recall, F1, Confusion Matrix, and 5-fold CV F1 using the same split.

## Reference results
| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 80.45% | 78.33% | 68.12% | 72.87% |
| Decision Tree | 80.45% | 80.36% | 65.22% | 72.00% |
| Neural Network | 82.12% | 87.76% | 62.32% | 72.88% |

## Decision
Logistic Regression is the practical final choice. The neural network improved accuracy slightly, but did not provide a meaningful F1/Recall improvement to justify the extra complexity.

## Structure
```text
src/        pipeline + training code
tests/      tests
reports/    reference metrics
data/       generated dataset/database location
```

## Run
```bash
pip install -r requirements.txt
python -m src.pipeline
python -m src.train
pytest
```

Raw downloads and generated SQLite files are ignored by Git to keep the repository lightweight.