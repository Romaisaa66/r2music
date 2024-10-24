from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os

r2music = Flask(__name__)

@r2music.route('/')
def index():
    return render_template('index.html', accuracy=None, error_rate=None, validation_accuracy=None, testing_accuracy=None)

@r2music.route('/calculate', methods=['POST'])
def calculate():
    total_predictions = int(request.form['total'])
    correct_predictions = int(request.form['correct'])
    validation_total = int(request.form['validation_total'])
    validation_correct = int(request.form['validation_correct'])
    testing_total = int(request.form['testing_total'])
    testing_correct = int(request.form['testing_correct'])

    # حساب الدقة والخطأ
    accuracy = (correct_predictions / total_predictions) * 100  # نسبة الدقة
    error_rate = 100 - accuracy  # نسبة الخطأ
    validation_accuracy = (validation_correct / validation_total) * 100  # نسبة دقة التحقق
    testing_accuracy = (testing_correct / testing_total) * 100  # نسبة دقة الاختبار

    # رسم بياني
    plot_accuracy_error(accuracy, error_rate, validation_accuracy, testing_accuracy)

    return render_template('index.html', accuracy=accuracy, error_rate=error_rate,
                           validation_accuracy=validation_accuracy, testing_accuracy=testing_accuracy)

def plot_accuracy_error(accuracy, error_rate, validation_accuracy, testing_accuracy):
    # إعداد البيانات
    labels = ['Accuracy', 'Error Rate', 'Validation Accuracy', 'Testing Accuracy']
    values = [accuracy, error_rate, validation_accuracy, testing_accuracy]

    # إنشاء الرسم البياني
    plt.figure(figsize=(10, 5))
    plt.bar(labels, values, color=['green', 'red', 'blue', 'orange'])
    plt.ylim(0, 100)
    plt.ylabel('Percentage (%)')
    plt.title('Accuracy, Error Rate, Validation Accuracy, and Testing Accuracy')

    # حفظ الرسم البياني كصورة
    plot_path = os.path.join('static', 'plot.png')
    plt.savefig(plot_path)
    plt.close()

if __name__ == '__main__':
    r2music.run(debug=True)
