import pyautogui
import cv2
import numpy as np
import mss
from utils import screen_width, screen_height, scaling_factor, to_relative, to_absolute, to_absolute_size

# Получаем разрешение экрана
screen_width, screen_height = pyautogui.size()

class EnemyDetector:
    def __init__(self, reference_image_path):
        self.enemy_frame_position = (
            to_relative(1368, 696),  # Преобразование координат x и y
            to_relative(6, 12)       # Преобразование ширины и высоты
        )
        self.reference_image = cv2.imread(reference_image_path)

    def capture_enemy_frame(self):
        # Получаем относительные координаты области врага и преобразуем их обратно в абсолютные
        (rel_x, rel_y), (rel_w, rel_h) = self.enemy_frame_position
        x, y = to_absolute(rel_x, rel_y)
        w, h = to_absolute_size(rel_w, rel_h)  # Используем отдельную функцию для размеров

        with mss.mss() as sct:
            monitor = {"top": y, "left": x, "width": w, "height": h}
            screenshot = np.array(sct.grab(monitor))
            return screenshot[:, :, :3]

    def detect_enemy(self):
        enemy_frame = self.capture_enemy_frame()
        if enemy_frame is None or self.reference_image is None:
            print("Ошибка: не удалось захватить изображение или эталонное изображение отсутствует.")
            return False

        # Изменяем размер эталонного изображения, чтобы оно совпадало с текущим размером
        if enemy_frame.shape != self.reference_image.shape:
            self.reference_image = cv2.resize(self.reference_image, (enemy_frame.shape[1], enemy_frame.shape[0]))

        diff = cv2.absdiff(enemy_frame, self.reference_image)
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        non_zero_count = np.count_nonzero(diff_gray)
        total_pixels = diff_gray.size

        similarity_percentage = 100 - (non_zero_count / total_pixels * 100)
        print(f"Процент схожести с эталонным изображением врага: {similarity_percentage}%")

        return similarity_percentage > 10  # Порог обнаружения врага, можно настроить
