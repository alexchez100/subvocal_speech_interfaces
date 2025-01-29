import tkinter as tk
from tkinter import simpledialog
import random
import os
from datetime import datetime
import csv

class LightSequenceApp:
    def __init__(self, root):
        # Создаем папку res, если она не существует
        if not os.path.exists('res'):
            os.makedirs('res')
        
        # Запрашиваем имя файла через диалоговое окно
        file_name = simpledialog.askstring("Input", "Enter file name:", parent=root)
        if file_name:
            # Создаем файл с текущей датой и временем
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.result_file = os.path.join('res', f"{current_time}_{file_name}.csv")
            # Создаем файл и записываем заголовки
            with open(self.result_file, 'w', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['time', 'word', 'status'])
        
        self.root = root
        self.root.title("Sequential Light Activation")
        
        # Устанавливаем тёмный фон
        self.root.configure(bg='#202020')
        
        # Инициализируем счетчик последовательностей
        self.sequence_count = 0
        
        # Создаем метку для отображения счетчика
        self.counter_label = tk.Label(root, text="Repetition count: 0", 
                                    font=('Arial', 14), bg='#202020', fg='white')
        self.counter_label.pack(pady=20)
        
        # Разворачиваем окно на весь экран, сохраняя строку заголовка
        self.root.state('zoomed')
        
        # Загружаем слова из файла
        try:
            with open('words.txt', 'r', encoding='utf-8') as file:
                self.words = [line.strip() for line in file if line.strip()]
            # Создаем счетчик для каждого слова
            self.word_counts = {word: 0 for word in self.words}
        except FileNotFoundError:
            self.words = ["Файл words.txt не найден"]
            self.word_counts = {self.words[0]: 0}
        
        # Создаем фрейм для лампочек
        self.lights_frame = tk.Frame(root, bg='#202020')
        self.lights_frame.pack(pady=(40, 0))  # Отступ только сверху
        
        # Создаем 6 лампочек (круглых кнопок) увеличенного размера
        self.lights = []
        for i in range(6):
            light = tk.Canvas(self.lights_frame, width=200, height=200, bg='#202020', highlightthickness=0)
            light.create_oval(20, 20, 180, 180, fill='gray', tags='light')
            light.pack(side=tk.LEFT, padx=20)
            self.lights.append(light)
        
        # Создаем фрейм для центрирования слова
        self.word_frame = tk.Frame(root, bg='#202020')
        self.word_frame.pack(expand=True, fill='both')
        
        # Создаем метку для отображения слова
        self.word_label = tk.Label(self.word_frame, text="", font=('Arial', 100), 
                                 bg='#202020', fg='white')
        self.word_label.place(relx=0.5, rely=0.5, anchor='center')
        
        # Создаем фрейм для кнопок
        self.button_frame = tk.Frame(root, bg='#202020')
        self.button_frame.pack(pady=(0, 40))  # Отступ только снизу
        
        # Кнопка для запуска последовательности
        self.start_button = tk.Button(self.button_frame, text="Word", command=self.start_sequence, 
                                    font=('Arial', 21), bg='#404040', fg='white',
                                    activebackground='#505050', activeforeground='white',
                                    height=4, width=30,  # Уменьшена высота с 5 до 4
                                    relief=tk.GROOVE,
                                    borderwidth=3)
        self.start_button.pack(side=tk.LEFT, padx=20)
        
        # Кнопка Skip
        self.skip_button = tk.Button(self.button_frame, text="Skip", command=self.skip_last_record,
                                   font=('Arial', 21), bg='#404040', fg='white',
                                   activebackground='#505050', activeforeground='white',
                                   height=4, width=15,  # Уменьшена высота с 5 до 4
                                   relief=tk.GROOVE,
                                   borderwidth=3)
        self.skip_button.pack(side=tk.LEFT, padx=20)
        
        self.current_light = 0
        self.sequence_running = False

        # Центрируем окно для ввода текста
        self.center_window()

    def center_window(self):
        # Получаем размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Получаем размеры окна
        window_width = 400
        window_height = 200
        
        # Вычисляем координаты для центрирования
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        
        # Устанавливаем размеры и позицию окна
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def get_balanced_random_word(self):
        # Находим слова с минимальным количеством показов
        min_count = min(self.word_counts.values())
        candidates = [word for word, count in self.word_counts.items() if count == min_count]
        # Выбираем случайное слово из кандидатов
        chosen_word = random.choice(candidates)
        # Увеличиваем счетчик для выбранного слова
        self.word_counts[chosen_word] += 1
        return chosen_word
    
    def start_sequence(self):
        if self.sequence_running:
            return
        
        # Выбираем и отображаем случайное слово
        word = self.get_balanced_random_word()
        self.word_label.config(text=word)
            
        # Сбрасываем все лампочки в серый цвет
        for light in self.lights:
            light.itemconfig('light', fill='gray')
        
        self.sequence_running = True
        self.current_light = 0
        
        # Визуально нажимаем кнопку
        self.start_button.config(relief=tk.SUNKEN)
        # Делаем кнопку неактивной
        self.start_button.config(state=tk.DISABLED)
        
        self.light_next()
    
    def light_next(self):
        if self.current_light < len(self.lights):
            # Зажигаем текущую лампочку зеленым цветом
            self.lights[self.current_light].itemconfig('light', fill='green')
            self.current_light += 1
            # Устанавливаем интервал в 800 мс
            self.root.after(800, self.light_next)
        else:
            # Сразу меняем цвет на тёмно-красный без задержки
            for light in self.lights:
                light.itemconfig('light', fill='#8B0000')  # Тёмно-красный цвет
            self.sequence_running = False
            
            # Записываем данные в CSV файл
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            current_word = self.word_label.cget("text")
            status = 1
            
            with open(self.result_file, 'a', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current_time, current_word, status])
            
            # Увеличиваем счетчик и обновляем отображение
            self.sequence_count += 1
            self.counter_label.config(text=f"Repetition count: {self.sequence_count}")
            
            # Через 3 секунды возвращаем кнопку в нормальное состояние
            self.root.after(3000, self.reset_button)
    
    def reset_button(self):
        # Возвращаем кнопку в нормальное состояние
        self.start_button.config(relief=tk.GROOVE)
        self.start_button.config(state=tk.NORMAL)

    def skip_last_record(self):
        try:
            # Читаем все строки из файла
            rows = []
            with open(self.result_file, 'r', encoding='utf-8-sig', newline='') as file:
                reader = csv.reader(file)
                rows = list(reader)
            
            if len(rows) > 1:  # Проверяем, есть ли строки кроме заголовка
                # Меняем статус последней строки на 0
                rows[-1][-1] = '0'
                
                # Записываем обновленные данные обратно в файл
                with open(self.result_file, 'w', encoding='utf-8-sig', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
        except Exception as e:
            print(f"Ошибка при обновлении статуса: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LightSequenceApp(root)
    root.mainloop()
