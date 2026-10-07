# [Phantoms | W5D3] DL Debugging: Fixing The Non-Learning Network

## الهدف

الهدف من التاسك هو تعلم **Deep Learning Debugging** بشكل منهجي بدل تغيير القيم عشوائيًا. المشكلة الأساسية هنا هي شبكة لا تتعلم، لذلك بنفحص 3 أسباب رئيسية بالترتيب:

1. **Learning Rate** — هل معدل التعلم مناسب للـ Convergence؟
2. **Data Normalization** — هل المدخلات على Scale مناسب للـ Backpropagation؟
3. **Input / Output Shapes** — هل أبعاد البيانات متوافقة مع طبقات الشبكة؟

---

## 1. اختبار الـ Learning Rate

لو الـ Learning Rate كبيرة جدًا، الـ optimizer ممكن يقفز بعيدًا عن الحل، والـ Loss يفضل متذبذب أو لا يستقر.

ولو صغيرة جدًا، الـ Loss ممكن ينخفض ببطء شديد وكأن الشبكة لا تتعلم.

لذلك بدل التخمين، نجرب قيم مختلفة ونراقب الـ Loss.

```python
learning_rates = [0.1, 0.01, 0.001]

for lr in learning_rates:
    model = SimpleNet()
    optimizer = torch.optim.SGD(model.parameters(), lr=lr)

    # train for a few epochs
    # compare the loss curve for each lr
```

في التجربة النهائية تم استخدام:

```python
lr = 0.001
```

لأنه معدل أكثر استقرارًا للتجربة بدل القفزات الكبيرة.

---

## 2. اختبار الـ Data Normalization

الـ Neural Network بتتعلم من الـ gradients. لو قيم الـ input كبيرة جدًا أو المقاييس مختلفة بشكل كبير، الـ optimization ممكن يبقى أصعب.

مثال على Normalization للصور:

```python
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])
```

هنا قيم MNIST بتتحول إلى Scale مناسب تقريبًا حول المتوسط صفر، وده يساعد الـ Backpropagation والـ optimizer على الوصول لحل بشكل أكثر استقرارًا.

**Debug check:**

```python
print(x_train.mean())
print(x_train.std())
print(x_train.shape)
```

مش بنفترض إن الـ data سليمة؛ بنقيسها قبل التدريب.

---

## 3. اختبار Input / Output Shapes

لازم الـ shape الداخل للشبكة يطابق أول Layer، والـ output يطابق عدد الـ classes.

بالنسبة لـ MNIST:

```
Input image: 1 × 28 × 28
Flatten:     784
Output:      10 classes
```

مثال:

```python
class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(28 * 28, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        return self.fc2(x)
```

لو دخلنا صورة بشكل `[batch, 1, 28, 28]` من غير Flatten قبل الـ Linear Layer، هيحصل **Shape Mismatch**.

ولو آخر Layer طلعت عدد outputs مختلف عن عدد الـ classes، هيكون فيه مشكلة في الـ model/loss setup.

---

## 4. الإصلاح والاختبار

بعد فحص الفرضيات، بنثبت الإعدادات الصحيحة ثم نعيد التدريب:

```python
model = SimpleNet()

optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.001
)

criterion = nn.CrossEntropyLoss()
```

أثناء التدريب نتابع:

```python
for epoch in range(epochs):
    model.train()

    for images, labels in train_loader:
        optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch + 1}: Loss = {loss.item():.4f}")
```

**معيار نجاح الـ Debugging:**  
الـ Loss لا يظل ثابتًا؛ المفروض يبدأ في الانخفاض تدريجيًا مع التدريب، مع تحسن أداء النموذج على بيانات الـ validation/test بدل الاعتماد على قيمة Loss واحدة فقط.

---

## السبب الحقيقي وطريقة اكتشافه

الخطأ هنا لا يتم تشخيصه بتغيير كل حاجة مرة واحدة. الطريقة الصح هي **Hypothesis → Test → Observe → Fix → Re-test**.

أبدأ بالـ Learning Rate، وبعدها أتأكد من الـ Scaling/Normalization، وبعدها أراجع الـ Input/Output Shapes. كل خطوة لها اختبار واضح.

**السبب العملي الذي يتم إصلاحه في التجربة:** استخدام إعداد تدريب غير مناسب للـ optimization مع ضرورة التأكد من تجهيز البيانات والـ shapes قبل الحكم على الـ network.

الأهم إننا ما نقولش "الموديل وحش" قبل ما نتأكد إن الـ pipeline نفسه سليم.

---

## Debugging Checklist

- [x] فحص Learning Rate
- [x] فحص Data Normalization
- [x] فحص Input Shape
- [x] فحص Output Shape
- [x] تعديل إعدادات التدريب
- [x] إعادة اختبار الـ Loss
- [x] توثيق خطوات التشخيص

## الخلاصة

**Deep Learning Debugging** مش معناه نجرب أرقام عشوائية. معناه نمسك المشكلة كمهندس: نحدد فرضية، نعمل اختبار صغير، نقرأ النتيجة، وبعدها نغير حاجة واحدة بس.

وده بيساعدنا نعرف هل المشكلة في **Optimization**، ولا **Data**، ولا **Model Architecture / Shapes**.

### Status

**Complete**
