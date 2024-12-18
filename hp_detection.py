import cv2
import numpy as np
import mss
import pyautogui
from utils import screen_width, screen_height, scaling_factor, to_relative, to_absolute, to_absolute_size

class HealthDetector:
    def __init__(self, reference_image_path):
        # Установленные координаты области здоровья на экране в относительных значениях
        self.health_bar_position = (
            to_relative(491, 694),  # Координаты x и y
            to_relative(64, 22)     # Ширина и высота
        )
        self.reference_image = cv2.imread(reference_image_path)

    def capture_health_bar(self):
        # Получаем относительные координаты области здоровья и преобразуем их обратно в абсолютные
        (rel_x, rel_y), (rel_w, rel_h) = self.health_bar_position
        x, y = to_absolute(rel_x, rel_y)
        w, h = to_absolute_size(rel_w, rel_h)  # Используем отдельную функцию для размеров

        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": w, "height": h}
            screenshot = np.array(sct.grab(monitor))
            return screenshot[:, :, :3]  # Убираем альфа-канал

    def compare_health(self):
        health_bar = self.capture_health_bar()
        if health_bar is None or self.reference_image is None:
            print("Ошибка: не удалось захватить изображение или эталонное изображение отсутствует.")
            return 0.0

        # Приведение к одному размеру, если необходимо
        if health_bar.shape != self.reference_image.shape:
            self.reference_image = cv2.resize(self.reference_image, (health_bar.shape[1], health_bar.shape[0]))

        # Сравниваем захваченное изображение с эталонным
        diff = cv2.absdiff(health_bar, self.reference_image)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        non_zero_count = np.count_nonzero(diff_gray)
        total_pixels = diff_gray.size

        # Рассчитываем процент оставшегося здоровья
        similarity_percentage = 100 - (non_zero_count / total_pixels * 100)
        print(f"Процент схожести с эталонным изображением: {similarity_percentage}%")

        return similarity_percentage
