from deepface import DeepFace
import numpy as np

# مجموعة اختبار تحتوي على الصور الحقيقية مع مشاعرها المصنفة
test_data = [
    {"img_path": "C:/Users/rabah/Final/FER2013/test/happy/PrivateTest_2626531.jpg", "true_emotion": "happy"},
    {"img_path": "C:/Users/rabah/Final/FER2013/test/happy/PrivateTest_647018.jpg", "true_emotion": "happy"},
    {"img_path": "C:/Users/rabah/Final/FER2013/test/happy/PrivateTest_2626531.jpg", "true_emotion": "happy"},
    {"img_path": "C:/Users/rabah/Final/FER2013/train/sad/Training_423072.jpg",   "true_emotion": "sad"},
    {"img_path": "C:/Users/rabah/Final/FER2013/train/sad/Training_1362985.jpg", "true_emotion": "sad"},
    {"img_path": "C:/Users/rabah/Final/FER2013/test/sad/PublicTest_94416517.jpg", "true_emotion": "sad"},
    {"img_path": "C:/Users/rabah/Final/FER2013/train/angry/Training_97006335.jpg", "true_emotion": "angry"},
    {"img_path": "C:/Users/rabah/Final/FER2013/train/angry/Training_1951293.jpg", "true_emotion": "angry"},
    {"img_path": "C:/Users/rabah/Final/FER2013/train/angry/Training_98381033.jpg", "true_emotion": "angry"},
    {"img_path": "C:/Users/rabah/Final/FER2013/test/surprise/PrivateTest_2034433.jpg",  "true_emotion": "surprise"},
    {"img_path": "C:/Users/rabah/Final/FER2013/test/surprise/PrivateTest_2264189.jpg",  "true_emotion": "surprise"},
    {"img_path": "C:/Users/rabah/Final/FER2013/test/surprise/PrivateTest_1673508.jpg",  "true_emotion": "surprise"},
{"img_path": "C:/Users/rabah/Final/FER2013/test/neutral/PrivateTest_5186732.jpg", "true_emotion": "neutral"},
{"img_path": "C:/Users/rabah/Final/FER2013/test/neutral/PrivateTest_11752870.jpg", "true_emotion": "neutral"},
{"img_path": "C:/Users/rabah/Final/FER2013/test/neutral/PrivateTest_20544030.jpg", "true_emotion": "neutral"},
]

# متغيرات لحساب الدقة والخطأ
correct_predictions = 0
total_predictions = len(test_data)

# اختبار كل صورة من مجموعة البيانات
for data in test_data:
    img_path = data["img_path"]
    true_emotion = data["true_emotion"]

    # تحليل مشاعر الصورة باستخدام DeepFace
    try:
        prediction = DeepFace.analyze(img_path, actions=['emotion'], enforce_detection=False)
        print(f"Prediction result for {img_path}: {prediction}")  # طباعة نتيجة التحليل

        # الوصول إلى العنصر الأول من القائمة
        predicted_emotion = prediction[0]['dominant_emotion']

        # التحقق من صحة التوقع
        if predicted_emotion == true_emotion:
            correct_predictions += 1
        else:
            print(f"Incorrect prediction for {img_path}. Predicted: {predicted_emotion}, Actual: {true_emotion}")
    except Exception as e:
        print(f"Error processing image {img_path}: {e}")

# حساب الدقة والخطأ
accuracy = correct_predictions / total_predictions
error_rate = 1 - accuracy

print(f"Accuracy: {accuracy * 100:.2f}%")
print(f"Error Rate: {error_rate * 100:.2f}%")

