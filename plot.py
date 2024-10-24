import matplotlib.pyplot as plt

# لنفترض أنك حصلت على قيم الدقة
train_accuracy = 95.00  # دقة التدريب
validation_accuracy = 91.00  # دقة التحقق
testing_accuracy = 93.33  # دقة الاختبار
error_rate = 6.67  # معدل الخطأ

# البيانات لإظهارها في الرسم البياني
categories = ['Training Accuracy', 'Validation Accuracy', 'Testing Accuracy', 'Error Rate']
values = [train_accuracy, validation_accuracy, testing_accuracy, error_rate]

# إنشاء الرسم البياني
plt.figure(figsize=(10, 6))
bars = plt.bar(categories, values, color=['blue', 'orange', 'green', 'red'])

# إضافة القيم فوق الأعمدة
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, round(yval, 2), ha='center', va='bottom')

# إعدادات الرسم
plt.ylim(0, 100)
plt.ylabel('Percentage (%)')
plt.title('Model Performance: Accuracy and Error Rate')
plt.grid(axis='y', linestyle='--', alpha=0.7)

# عرض الرسم البياني
plt.show()
