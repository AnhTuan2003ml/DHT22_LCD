from EmulatorGUI import GPIO
from DHT22 import readSensor  # Sử dụng mô-đun DHT22 giả lập
from pnhLCD1602 import LCD1602  # Sử dụng mô-đun giả lập màn hình LCD
import pygame
import time

# Thiết lập các chân GPIO
BUTTON_UP_PIN = 17  # Nút Up
BUTTON_DOWN_PIN = 27  # Nút Down
BUZZER_PIN = 22  # Chân kết nối còi chip
DHT_PIN = 4  # Pin kết nối cảm biến DHT22

# Khởi tạo GPIO (Sử dụng mô phỏng)
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Khởi tạo màn hình LCD
lcd = LCD1602()

# Biến mặc định
temp_limit = 30  # Giới hạn nhiệt độ mặc định

# Hàm hiển thị thông tin lên LCD
def update_lcd(temperature, humidity, limit):
    lcd.clear()
    lcd.write_string(f"Temp:{temperature}C")
    lcd.set_cursor(1, 0)
    lcd.write_string(f"Hum:{humidity}% |{limit}C")

# Cảnh báo quá nhiệt
def alert():
    GPIO.output(BUZZER_PIN, GPIO.HIGH)
    lcd.clear()
    lcd.write_string("ALERT!")
    lcd.set_cursor(1, 0)
    lcd.write_string("Temp exceeded!")
    pygame.time.delay(5000)  # Cảnh báo trong 5 giây
    GPIO.output(BUZZER_PIN, GPIO.LOW)

try:
    while True:
        # Đọc giá trị từ cảm biến DHT22
        temp, hum = readSensor(DHT_PIN)  # Cổng DHT_PIN đã được thiết lập
        if temp is not None and hum is not None:
            update_lcd(round(temp, 1), round(hum, 1), temp_limit)
            if temp > temp_limit:
                alert()

        # Kiểm tra trạng thái nút nhấn
        if GPIO.input(BUTTON_UP_PIN) == GPIO.LOW:  # Nút Up được nhấn
            temp_limit += 1
            lcd.clear()
            update_lcd(round(temp, 1), round(hum, 1), temp_limit)
            pygame.time.delay(10)  # Tránh nhấn liên tục
        if GPIO.input(BUTTON_DOWN_PIN) == GPIO.LOW:  # Nút Down được nhấn
            temp_limit -= 1
            lcd.clear()
            update_lcd(round(temp, 1), round(hum, 1), temp_limit)
            pygame.time.delay(10)  # Tránh nhấn liên tục

        time.sleep(2)

except KeyboardInterrupt:
    pass

finally:
    print("Cleaning up GPIO and exiting...")
    GPIO.cleanup()
    lcd.close()
