# PHANTOMS Capstone Checkpoint

مشروع تطبيقي واحد بيجمع المهارات الأساسية من Week 1 لحد Week 5 في Pipeline واحدة من أول تحميل البيانات لحد اختيار النموذج النهائي.

## فكرة المشروع

المشروع بيستخدم **Titanic Dataset** للتنبؤ هل الراكب نجا أم لا (`Survived`).

الـpipeline بتنفذ المراحل المطلوبة كاملة:

1. **Data Collection + SQLite**
   تحميل الـdataset من Kaggle، وبعدها تخزين الـraw والـcleaned data في SQLite.

2. **Data Cleaning + Preparation**
   - معالجة Missing Values.
   - حذف الأعمدة غير المفيدة للموديل مثل `Name`, `Ticket`, `Cabin`, و`PassengerId`.
   - تحديد الـFeatures والـLabel بوضوح.
   - استخدام One-Hot Encoding للـCategorical Features.
   - Standard Scaling للـNumerical Features.

3. **Model Training + Comparison**
   نفس `Train/Test Split` مستخدم مع كل النماذج (`test_size=0.2`, `random_state=42`, stratified):
   - Logistic Regression
   - Decision Tree
   - Neural Network (MLP)

4. **Correct Evaluation**
   المقارنة مش مبنية على Accuracy بس، لكن على:
   - Accuracy
   - Precision
   - Recall
   - F1-Score
   - Confusion Matrix
   - 5-Fold Cross-Validation F1

5. **Deep Learning Decision**
   اتجرب Neural Network بسيطة على نفس البيانات. حققت Accuracy أعلى شوية، لكن الـF1 والـRecall ماقدموش تحسن يخلي التعقيد الإضافي مبرر. لذلك **Logistic Regression** هو الاختيار العملي النهائي.

## النتائج

| Model | Accuracy | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| Logistic Regression | 80.45% | 78.33% | 68.12% | 72.87% |
| Decision Tree | 80.45% | 80.36% | 65.22% | 72.00% |
| Neural Network | 82.12% | 87.76% | 62.32% | 72.88% |

### Confusion Matrices

- **Logistic Regression:** `[[97, 13], [22, 47]]`
- **Decision Tree:** `[[99, 11], [24, 45]]`
- **Neural Network:** `[[104, 6], [26, 43]]`

الـNeural Network كسبت في Accuracy وPrecision، لكن Recall أقل من Logistic Regression، والـF1 تقريبًا متساوي. عشان كده Accuracy الأعلى لوحدها مش كفاية لاختيارها.

النتائج التفصيلية محفوظة في `reports/metrics.json`.

## القرار النهائي

**Logistic Regression** هو الاختيار النهائي للمشكلة دي.

السبب إن النموذج الأبسط حقق F1 قريب جدًا من الـNeural Network مع Recall أفضل، ومن غير التعقيد الإضافي. ده مناسب لمشكلة Tabular Classification بالشكل ده، ومش محتاج Deep Learning كحل أساسي.

## Structure

```text
phantoms-capstone-checkpoint/
├── src/
│   ├── pipeline.py
│   └── train.py
├── tests/
│   └── test_pipeline.py
├── reports/
│   └── metrics.json
├── data/
│   └── .gitkeep
├── weekly_work/
│   └── README.md
├── requirements.txt
└── README.md
```

الـdataset والـSQLite database بيتعملوا وقت التشغيل ومش بيتحطوا في Git عشان نحافظ على حجم الـrepository.

## Run

```bash
pip install -r requirements.txt
python -m src.pipeline
python -m src.train
pytest
```

## Previous Weekly Work

الـCapstone ده مبني على شغل الأسابيع السابقة، والـrepositories الأصلية محفوظة ومذكورة في [weekly_work/README.md](weekly_work/README.md) بدل تكرار نفس الملفات داخل المشروع.

## Status

**Complete — implementation ready for submission.**