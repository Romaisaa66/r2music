# استخدم صورة Python 3.10
FROM python:3.10

# إعداد مجلد العمل
WORKDIR /app

# تثبيت المكتبات اللازمة
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# نسخ متطلبات التطبيق
COPY requirements.txt .

# تحديث pip وتثبيت المتطلبات
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# نسخ بقية التطبيق
COPY . .

# الأمر الافتراضي لتشغيل التطبيق
CMD ["python", "r2music.py"]
