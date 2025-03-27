# main_app.py (предполагается, что database_module.py находится в том же каталоге)
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, filedialog
from database_module import DatabaseManager
import base64
import io # Для работы с байтами изображения в памяти
from PIL import Image, ImageTk # Убедитесь, что установлен Pillow: pip install Pillow

# --- UserInputDialog остаётся без изменений ---
class UserInputDialog(tk.Toplevel):
    def __init__(self, parent, title, user_data=None):
        super().__init__(parent)
        self.transient(parent) # Make it a transient window
        self.grab_set()      # Grab focus
        self.title(title)
        self.geometry('400x300')
        self.result = None
        self.configure(bg='#f0f0f0')

        frame = tk.Frame(self, bg='#f0f0f0')
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Стили для виджетов
        label_style = {'bg': '#f0f0f0', 'font': ('Arial', 10)}
        entry_style = {'width': 40, 'font': ('Arial', 10)}

        tk.Label(frame, text='ФИО:', **label_style).pack(anchor='w')
        self.name_entry = tk.Entry(frame, **entry_style)
        self.name_entry.pack(pady=(0,10))

        tk.Label(frame, text='Телефон:', **label_style).pack(anchor='w')
        self.phone_entry = tk.Entry(frame, **entry_style)
        self.phone_entry.pack(pady=(0,10))

        tk.Label(frame, text='Email:', **label_style).pack(anchor='w')
        self.email_entry = tk.Entry(frame, **entry_style)
        self.email_entry.pack(pady=(0,10))

        # Заполнение данными если редактирование
        if user_data:
            self.name_entry.insert(0, user_data[1])
            self.phone_entry.insert(0, user_data[2] or '')
            self.email_entry.insert(0, user_data[3] or '')

        # Кнопки
        btn_frame = tk.Frame(frame, bg='#f0f0f0')
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text='Сохранить', command=self.save,
                  bg='#4CAF50', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text='Отмена', command=self.cancel, # Use cancel for clarity
                  bg='#f44336', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)

        # Focus on the first entry
        self.name_entry.focus_set()

        # Bind Enter key to save
        self.bind('<Return>', lambda event: self.save())
        # Bind Escape key to cancel
        self.bind('<Escape>', lambda event: self.cancel())

    def save(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if not name:
            messagebox.showerror("Ошибка", "ФИО обязательно для заполнения!", parent=self) # Set parent for messagebox
            return

        self.result = (name, phone, email)
        self.destroy()

    def cancel(self):
        self.result = None # Ensure result is None on cancel
        self.destroy()


# --- AnimalInputDialog Обновлено ---
class AnimalInputDialog(tk.Toplevel):
    def __init__(self, parent, title, animal_data=None):
        super().__init__(parent)
        self.transient(parent)
        self.grab_set()
        self.title(title)
        # Увеличим высоту окна для кнопки и превью изображения
        self.geometry('450x550') # Adjusted height
        self.result = None
        self.image_base64 = None # Хранение base64 строки изображения
        self.preview_image_tk = None # Хранение ссылки на PhotoImage для превью
        self.configure(bg='#f0f0f0')

        frame = tk.Frame(self, bg='#f0f0f0')
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        label_style = {'bg': '#f0f0f0', 'font': ('Arial', 10)}
        entry_style = {'width': 40, 'font': ('Arial', 10)}

        tk.Label(frame, text='Имя:', **label_style).pack(anchor='w')
        self.name_entry = tk.Entry(frame, **entry_style)
        self.name_entry.pack(pady=(0,10))

        tk.Label(frame, text='Вид:', **label_style).pack(anchor='w')
        self.type_entry = tk.Entry(frame, **entry_style)
        self.type_entry.pack(pady=(0,10))

        tk.Label(frame, text='Порода:', **label_style).pack(anchor='w')
        self.breed_entry = tk.Entry(frame, **entry_style)
        self.breed_entry.pack(pady=(0,10))

        tk.Label(frame, text='Возраст:', **label_style).pack(anchor='w')
        self.age_entry = tk.Entry(frame, **entry_style)
        self.age_entry.pack(pady=(0,10))

        # --- Элементы для изображения ---
        tk.Button(frame, text="Выбрать фото", command=self.choose_image,
                  bg='#2196F3', fg='white', font=('Arial', 10)).pack(pady=(5, 5))

        # Место для превью изображения
        self.image_preview_label = tk.Label(frame, bg='#cccccc', width=20, height=10) # Placeholder background
        self.image_preview_label.pack(pady=(0, 10))

        # Кнопка для удаления фото
        tk.Button(frame, text="Удалить фото", command=self.remove_image,
                  bg='#FF9800', fg='white', font=('Arial', 9)).pack(pady=(0, 10))


        # --- Заполнение данными, если редактирование ---
        if animal_data:
            # Индексы animal_data: 0:id, 1:user_id, 2:name, 3:type, 4:breed, 5:age, 6:image_base64
            self.name_entry.insert(0, animal_data[2])
            self.type_entry.insert(0, animal_data[3] or '')
            self.breed_entry.insert(0, animal_data[4] or '')
            self.age_entry.insert(0, str(animal_data[5]) if animal_data[5] is not None else '')
            # Загрузка существующего изображения
            self.image_base64 = animal_data[6]
            if self.image_base64:
                self._display_preview_image(self.image_base64)

        # Кнопки Сохранить/Отмена
        btn_frame = tk.Frame(frame, bg='#f0f0f0')
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text='Сохранить', command=self.save,
                  bg='#4CAF50', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text='Отмена', command=self.cancel,
                  bg='#f44336', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)

        self.name_entry.focus_set()
        self.bind('<Return>', lambda event: self.save())
        self.bind('<Escape>', lambda event: self.cancel())

    def choose_image(self):
        """Открывает диалог выбора файла и кодирует изображение в base64."""
        file_path = filedialog.askopenfilename(
            title="Выберите фото питомца",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("All Files", "*.*")]
        )
        if not file_path:
            return # Пользователь отменил выбор

        try:
            # Рекомендуется изменить размер перед кодированием, если изображения большие
            img = Image.open(file_path)
            # img.thumbnail((800, 800)) # Опционально: ограничить макс. размер

            # Конвертировать в формат, который точно поддерживается (например, PNG или JPEG)
            # Это также помогает убрать EXIF и другие метаданные
            output_format = 'PNG' if img.mode == 'RGBA' else 'JPEG'

            buffered = io.BytesIO()
            img.save(buffered, format=output_format, quality=85) # quality для JPEG
            img_bytes = buffered.getvalue()

            self.image_base64 = base64.b64encode(img_bytes).decode('utf-8')
            self._display_preview_image(self.image_base64)

        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл не найден: {file_path}", parent=self)
            self.image_base64 = None
            self._clear_preview_image()
        except UnidentifiedImageError: # Requires Pillow >= 8.0.0
             messagebox.showerror("Ошибка", "Не удалось распознать файл как изображение.", parent=self)
             self.image_base64 = None
             self._clear_preview_image()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось обработать изображение: {e}", parent=self)
            self.image_base64 = None
            self._clear_preview_image()

    def _display_preview_image(self, b64_string):
        """Отображает превью изображения из строки base64."""
        if not b64_string:
            self._clear_preview_image()
            return
        try:
            img_data = base64.b64decode(b64_string)
            img = Image.open(io.BytesIO(img_data))
            img.thumbnail((150, 150)) # Размер превью
            self.preview_image_tk = ImageTk.PhotoImage(img)

            self.image_preview_label.config(image=self.preview_image_tk, width=self.preview_image_tk.width(), height=self.preview_image_tk.height())
        except Exception as e:
            print(f"Ошибка отображения превью: {e}")
            self._clear_preview_image()

    def _clear_preview_image(self):
        """Очищает превью изображения."""
        self.image_preview_label.config(image='', text="Нет фото", bg='#cccccc', width=20, height=10)
        self.preview_image_tk = None # Очистить ссылку

    def remove_image(self):
        """Удаляет выбранное/существующее изображение."""
        self.image_base64 = None
        self._clear_preview_image()
        messagebox.showinfo("Фото удалено", "Фото будет удалено при сохранении.", parent=self)


    def save(self):
        name = self.name_entry.get().strip()
        type_animal = self.type_entry.get().strip()
        breed = self.breed_entry.get().strip()
        age_str = self.age_entry.get().strip()
        age = None

        if age_str:
             try:
                 age = int(age_str)
                 if age < 0:
                     messagebox.showerror("Ошибка", "Возраст не может быть отрицательным!", parent=self)
                     return
             except ValueError:
                 messagebox.showerror("Ошибка", "Возраст должен быть целым числом!", parent=self)
                 return

        if not name or not type_animal:
            messagebox.showerror("Ошибка", "Имя и вид обязательны для заполнения!", parent=self)
            return

        # Теперь результат включает и image_base64
        self.result = (name, type_animal, breed, age, self.image_base64)
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()


# --- VetClinicApp Обновлено ---
class VetClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Ветеринарная Клиника')
        # Увеличим ширину окна для колонки с фото
        self.root.geometry('1400x800') # Adjusted width
        self.root.configure(bg='#f0f0f0')

        # --- Добавим Placeholder Image ---
        self.placeholder_image = self._create_placeholder_image(200, 200, text="Нет фото")
        self.current_animal_photo = None # Для хранения ссылки на PhotoImage

        try:
            self.db_manager = DatabaseManager()
        except Exception as e:
            messagebox.showerror("Ошибка Базы Данных", f"Не удалось подключиться или инициализировать базу данных:\n{e}")
            self.root.destroy()
            return

        self.main_frame = tk.Frame(root, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_users_column()
        self.create_user_details_column()
        self.create_animal_details_column() # Этот метод будет обновлен

        self.load_users()
        self.current_user_id = None
        self.current_animal_id = None

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _create_placeholder_image(self, width, height, text="Placeholder"):
        """Создает простое изображение-заполнитель с текстом"""
        try:
            img = Image.new('RGB', (width, height), color = (200, 200, 200))
            # Можно добавить текст, но это требует настройки шрифтов, для простоты оставим серый квадрат
            # from PIL import ImageDraw, ImageFont
            # d = ImageDraw.Draw(img)
            # try:
            #     # Попытка загрузить стандартный шрифт
            #     font = ImageFont.truetype("arial.ttf", 15)
            # except IOError:
            #     font = ImageFont.load_default()
            # d.text((10,10), text, fill=(0,0,0), font=font)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Не удалось создать placeholder: {e}")
            return None # В случае ошибки вернем None

    def create_users_column(self):
        # Левая колонка - список пользователей (без изменений)
        left_frame = tk.Frame(self.main_frame, bg='#e0e0e0', bd=1, relief=tk.SUNKEN, width=300) # Fixed width example
        left_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=5, pady=5) # Fill Y, don't expand X
        left_frame.pack_propagate(False)

        tk.Label(left_frame, text='Клиенты',
                 font=('Arial', 14, 'bold'), bg='#e0e0e0').pack(pady=(10, 5))

        search_frame = tk.Frame(left_frame, bg='#e0e0e0')
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(search_frame, text='Поиск:', bg='#e0e0e0').pack(side=tk.LEFT)
        self.user_search_var = tk.StringVar()
        self.user_search_entry = tk.Entry(search_frame, textvariable=self.user_search_var)
        self.user_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.user_search_var.trace_add('write', self.filter_users)

        list_frame = tk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        user_scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.users_listbox = tk.Listbox(list_frame,
                                        font=('Arial', 10),
                                        selectbackground='#a6a6a6',
                                        exportselection=False,
                                        yscrollcommand=user_scrollbar.set)
        user_scrollbar.config(command=self.users_listbox.yview)
        user_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.users_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.users_listbox.bind('<<ListboxSelect>>', self.show_user_details)
        self.users_listbox.bind('<Double-Button-1>', self.edit_user)

        users_button_frame = tk.Frame(left_frame, bg='#e0e0e0')
        users_button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(users_button_frame, text='Добавить', command=self.add_user, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'), width=8).pack(side=tk.LEFT, expand=True, padx=2)
        tk.Button(users_button_frame, text='Изменить', command=self.edit_user, bg='#FFC107', fg='black', font=('Arial', 10, 'bold'), width=8).pack(side=tk.LEFT, expand=True, padx=2)
        tk.Button(users_button_frame, text='Удалить', command=self.delete_user, bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=8).pack(side=tk.RIGHT, expand=True, padx=2)


    def create_user_details_column(self):
        # Центральная колонка - информация о пользователе (без изменений)
        center_frame = tk.Frame(self.main_frame, bg='#e8e8e8', bd=1, relief=tk.SUNKEN, width=350) # Fixed width example
        center_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False, padx=5, pady=5) # Fill Y, don't expand X
        center_frame.pack_propagate(False)

        tk.Label(center_frame, text='Информация о клиенте',
                 font=('Arial', 14, 'bold'), bg='#e8e8e8').pack(pady=(10, 5))

        self.user_info_frame = tk.Frame(center_frame, bg='#e8e8e8')
        self.user_info_frame.pack(fill=tk.X, padx=10, pady=5)

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        info_style = {'font': ('Arial', 11), 'bg': '#e8e8e8', 'anchor': 'w', 'pady': 2}

        tk.Label(self.user_info_frame, text="ФИО:", font=('Arial', 11, 'bold'), bg='#e8e8e8', anchor='w').grid(row=0, column=0, sticky='w')
        tk.Label(self.user_info_frame, textvariable=self.name_var, **info_style).grid(row=0, column=1, sticky='w', padx=5)
        tk.Label(self.user_info_frame, text="Телефон:", font=('Arial', 11, 'bold'), bg='#e8e8e8', anchor='w').grid(row=1, column=0, sticky='w')
        tk.Label(self.user_info_frame, textvariable=self.phone_var, **info_style).grid(row=1, column=1, sticky='w', padx=5)
        tk.Label(self.user_info_frame, text="Email:", font=('Arial', 11, 'bold'), bg='#e8e8e8', anchor='w').grid(row=2, column=0, sticky='w')
        tk.Label(self.user_info_frame, textvariable=self.email_var, **info_style).grid(row=2, column=1, sticky='w', padx=5)

        # Список животных пользователя
        tk.Label(center_frame, text='Питомцы клиента',
                 font=('Arial', 14, 'bold'), bg='#e8e8e8').pack(pady=(15, 5))

        anim_list_frame = tk.Frame(center_frame)
        anim_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        animal_scrollbar = tk.Scrollbar(anim_list_frame, orient=tk.VERTICAL)
        self.animals_listbox = tk.Listbox(anim_list_frame,
                                          font=('Arial', 10),
                                          selectbackground='#a6a6a6',
                                          exportselection=False,
                                          yscrollcommand=animal_scrollbar.set)
        animal_scrollbar.config(command=self.animals_listbox.yview)
        animal_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.animals_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.animals_listbox.bind('<<ListboxSelect>>', self.show_animal_details)
        self.animals_listbox.bind('<Double-Button-1>', self.edit_animal)

        animals_button_frame = tk.Frame(center_frame, bg='#e8e8e8')
        animals_button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(animals_button_frame, text='Добавить', command=self.add_animal, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'), width=8).pack(side=tk.LEFT, expand=True, padx=2)
        tk.Button(animals_button_frame, text='Изменить', command=self.edit_animal, bg='#FFC107', fg='black', font=('Arial', 10, 'bold'), width=8).pack(side=tk.LEFT, expand=True, padx=2)
        tk.Button(animals_button_frame, text='Удалить', command=self.delete_animal, bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=8).pack(side=tk.RIGHT, expand=True, padx=2)

    def create_animal_details_column(self):
        # Правая колонка - информация о животном и комментарии (Обновлено)
        right_frame = tk.Frame(self.main_frame, bg='#f0f0f0', bd=1, relief=tk.SUNKEN)
        # Эта колонка теперь будет расширяться, чтобы вместить остальное пространство
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        # right_frame.pack_propagate(False) # Убрали, чтобы контент мог её расширять

        tk.Label(right_frame, text='Информация о питомце',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=(10, 5))

        # --- Разделим на две части: инфо слева, фото справа ---
        top_animal_frame = tk.Frame(right_frame, bg='#f0f0f0')
        top_animal_frame.pack(fill=tk.X, padx=10, pady=5)

        self.animal_info_frame = tk.Frame(top_animal_frame, bg='#f0f0f0')
        self.animal_info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10)) # Инфо слева

        # --- Место для фотографии питомца ---
        self.animal_image_label = tk.Label(top_animal_frame, image=self.placeholder_image, bg='#f0f0f0')
        self.animal_image_label.pack(side=tk.RIGHT, padx=(10, 0), pady=5, anchor='n') # Фото справа

        # --- Переменные и метки для информации о питомце ---
        self.animal_name_var = tk.StringVar()
        self.animal_type_var = tk.StringVar()
        self.animal_breed_var = tk.StringVar()
        self.animal_age_var = tk.StringVar()

        info_style = {'font': ('Arial', 11), 'bg': '#f0f0f0', 'anchor': 'w', 'pady': 2}
        bold_info_style = {'font': ('Arial', 11, 'bold'), 'bg': '#f0f0f0', 'anchor': 'w'}

        tk.Label(self.animal_info_frame, text="Имя:", **bold_info_style).grid(row=0, column=0, sticky='w')
        tk.Label(self.animal_info_frame, textvariable=self.animal_name_var, **info_style).grid(row=0, column=1, sticky='w', padx=5)
        tk.Label(self.animal_info_frame, text="Вид:", **bold_info_style).grid(row=1, column=0, sticky='w')
        tk.Label(self.animal_info_frame, textvariable=self.animal_type_var, **info_style).grid(row=1, column=1, sticky='w', padx=5)
        tk.Label(self.animal_info_frame, text="Порода:", **bold_info_style).grid(row=2, column=0, sticky='w')
        tk.Label(self.animal_info_frame, textvariable=self.animal_breed_var, **info_style).grid(row=2, column=1, sticky='w', padx=5)
        tk.Label(self.animal_info_frame, text="Возраст:", **bold_info_style).grid(row=3, column=0, sticky='w')
        tk.Label(self.animal_info_frame, textvariable=self.animal_age_var, **info_style).grid(row=3, column=1, sticky='w', padx=5)

        # --- Список комментариев (остается ниже) ---
        tk.Label(right_frame, text='История посещений / Комментарии',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=(15, 5))

        comment_list_frame = tk.Frame(right_frame)
        comment_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        comment_scrollbar = tk.Scrollbar(comment_list_frame, orient=tk.VERTICAL)
        self.comments_listbox = tk.Listbox(comment_list_frame,
                                           font=('Arial', 10),
                                           selectbackground='#a6a6a6',
                                           exportselection=False,
                                           yscrollcommand=comment_scrollbar.set)
        comment_scrollbar.config(command=self.comments_listbox.yview)
        comment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.comments_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.comments_listbox.bind('<Double-Button-1>', self.edit_comment)

        comments_button_frame = tk.Frame(right_frame, bg='#f0f0f0')
        comments_button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(comments_button_frame, text='Добавить', command=self.add_comment, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'), width=8).pack(side=tk.LEFT, expand=True, padx=2)
        tk.Button(comments_button_frame, text='Изменить', command=self.edit_comment, bg='#FFC107', fg='black', font=('Arial', 10, 'bold'), width=8).pack(side=tk.LEFT, expand=True, padx=2)
        tk.Button(comments_button_frame, text='Удалить', command=self.delete_comment, bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=8).pack(side=tk.RIGHT, expand=True, padx=2)


    def load_users(self, filter_term=""):
        # (без изменений)
        try:
            self.users_listbox.delete(0, tk.END)
            self.clear_user_details()
            users = self.db_manager.get_users()
            self.all_users_data = users

            filter_term = filter_term.lower()
            for user in users:
                user_id, name, phone, email = user
                display_phone = phone or 'Без телефона'
                list_string = f"{user_id}. {name} ({display_phone})"
                if not filter_term or filter_term in name.lower() or (phone and filter_term in phone):
                    self.users_listbox.insert(tk.END, list_string)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пользователей: {e}")
            self.all_users_data = []

    def filter_users(self, *args):
        # (без изменений)
        search_term = self.user_search_var.get()
        self.load_users(filter_term=search_term)

    def get_selected_user_data(self):
        # (без изменений)
        selected_indices = self.users_listbox.curselection()
        if not selected_indices:
            return None, None
        index = selected_indices[0]
        list_string = self.users_listbox.get(index)
        try:
            user_id = int(list_string.split('.')[0])
            user_data = next((u for u in self.all_users_data if u[0] == user_id), None)
            return user_id, user_data
        except (ValueError, IndexError):
             messagebox.showerror("Ошибка", "Не удалось получить ID пользователя из списка.")
             return None, None

    def show_user_details(self, event=None):
        # (без изменений)
        user_id, user_data = self.get_selected_user_data()
        if user_id is None:
             self.clear_user_details()
             return
        if user_data:
            self.current_user_id = user_id
            self.name_var.set(f"{user_data[1]}")
            self.phone_var.set(f"{user_data[2] or 'Не указан'}")
            self.email_var.set(f"{user_data[3] or 'Не указан'}")
            self.load_animals(user_id)
        else:
            self.clear_user_details()

    def load_animals(self, user_id):
        # (без изменений, но помним, что get_animals_by_user теперь возвращает и image_base64)
        self.animals_listbox.delete(0, tk.END)
        self.clear_animal_details()
        try:
            animals = self.db_manager.get_animals_by_user(user_id)
            self.current_user_animals = animals
            for animal in animals:
                # animal structure: (id, user_id, name, type, breed, age, image_base64)
                list_string = f"{animal[0]}. {animal[2]} ({animal[3]})"
                self.animals_listbox.insert(tk.END, list_string)
        except Exception as e:
             messagebox.showerror("Ошибка", f"Не удалось загрузить животных: {e}")
             self.current_user_animals = []

    def get_selected_animal_data(self):
        # (без изменений, но помним, что animal_data будет содержать и image_base64)
        selected_indices = self.animals_listbox.curselection()
        if not selected_indices:
            return None, None
        index = selected_indices[0]
        list_string = self.animals_listbox.get(index)
        try:
            animal_id = int(list_string.split('.')[0])
            animal_data = next((a for a in self.current_user_animals if a[0] == animal_id), None)
            return animal_id, animal_data
        except (ValueError, IndexError, AttributeError):
             return None, None

    # --- Обновлено: show_animal_details для отображения фото ---
    def show_animal_details(self, event=None):
        animal_id, animal_data = self.get_selected_animal_data()

        if animal_id is None:
            self.clear_animal_details()
            return

        if animal_data:
            # animal_data: (id, user_id, name, type, breed, age, image_base64)
            self.current_animal_id = animal_id
            self.animal_name_var.set(f"{animal_data[2]}")
            self.animal_type_var.set(f"{animal_data[3] or 'Не указан'}")
            self.animal_breed_var.set(f"{animal_data[4] or 'Не указана'}")
            age_display = str(animal_data[5]) if animal_data[5] is not None else 'Не указан'
            self.animal_age_var.set(f"{age_display}")

            # --- Отображение изображения ---
            image_b64 = animal_data[6]
            if image_b64:
                try:
                    img_data = base64.b64decode(image_b64)
                    img = Image.open(io.BytesIO(img_data))
                    # Масштабируем для отображения в UI, сохраняя пропорции
                    img.thumbnail((200, 200)) # Макс. размер отображения
                    self.current_animal_photo = ImageTk.PhotoImage(img)
                    self.animal_image_label.config(image=self.current_animal_photo)
                except Exception as e:
                    print(f"Ошибка загрузки фото питомца: {e}")
                    self.animal_image_label.config(image=self.placeholder_image) # Показать placeholder при ошибке
                    self.current_animal_photo = None # Сбросить ссылку
            else:
                # Если изображения нет, показываем placeholder
                self.animal_image_label.config(image=self.placeholder_image)
                self.current_animal_photo = None # Сбросить ссылку

            self.load_comments(animal_id)
        else:
             self.clear_animal_details()

    def load_comments(self, animal_id):
        # (без изменений)
        self.comments_listbox.delete(0, tk.END)
        try:
            comments = self.db_manager.get_comments_by_animal(animal_id)
            self.current_animal_comments = comments
            for comment in comments:
                # comment structure: (id, animal_id, text, timestamp)
                timestamp = comment[3]
                list_string = f"{comment[2]} ({timestamp})"
                self.comments_listbox.insert(tk.END, list_string)
        except Exception as e:
             messagebox.showerror("Ошибка", f"Не удалось загрузить комментарии: {e}")
             self.current_animal_comments = []

    def clear_user_details(self):
        # (без изменений)
        self.current_user_id = None
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.animals_listbox.delete(0, tk.END)
        self.current_user_animals = []
        self.clear_animal_details()

    # --- Обновлено: clear_animal_details для сброса фото ---
    def clear_animal_details(self):
        self.current_animal_id = None
        self.animal_name_var.set("")
        self.animal_type_var.set("")
        self.animal_breed_var.set("")
        self.animal_age_var.set("")
        # Сброс изображения к placeholder'у
        self.animal_image_label.config(image=self.placeholder_image)
        self.current_animal_photo = None # Сбросить ссылку
        self.comments_listbox.delete(0, tk.END)
        self.current_animal_comments = []

    # --- User Actions (add, edit, delete) - без изменений ---
    def add_user(self):
        dialog = UserInputDialog(self.root, "Добавить клиента")
        self.root.wait_window(dialog)
        if dialog.result:
            name, phone, email = dialog.result
            try:
                user_id = self.db_manager.add_user(name, phone, email)
                self.load_users(filter_term=self.user_search_var.get())
                for i in range(self.users_listbox.size()):
                    if self.users_listbox.get(i).startswith(f"{user_id}."):
                        self.users_listbox.selection_clear(0, tk.END)
                        self.users_listbox.selection_set(i)
                        self.users_listbox.see(i)
                        self.show_user_details()
                        break
            except Exception as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось добавить пользователя: {e}")

    def edit_user(self, event=None):
        user_id, user_data = self.get_selected_user_data()
        if not user_data:
            messagebox.showinfo("Изменение", "Выберите пользователя для изменения.")
            return
        dialog = UserInputDialog(self.root, "Изменить данные клиента", user_data=user_data)
        self.root.wait_window(dialog)
        if dialog.result:
            name, phone, email = dialog.result
            try:
                self.db_manager.update_user(user_id, name, phone, email)
                selected_indices = self.users_listbox.curselection()
                self.load_users(filter_term=self.user_search_var.get())
                reselected = False
                for i in range(self.users_listbox.size()):
                    if self.users_listbox.get(i).startswith(f"{user_id}."):
                        self.users_listbox.selection_clear(0, tk.END)
                        self.users_listbox.selection_set(i)
                        self.users_listbox.see(i)
                        self.show_user_details()
                        reselected = True
                        break
                if not reselected and selected_indices:
                     try:
                         self.users_listbox.selection_set(selected_indices[0])
                         self.show_user_details()
                     except tk.TclError: pass
            except Exception as e:
                 messagebox.showerror("Ошибка базы данных", f"Не удалось обновить пользователя: {e}")

    def delete_user(self):
        user_id, user_data = self.get_selected_user_data()
        if not user_data:
            messagebox.showinfo("Удаление", "Выберите пользователя для удаления.")
            return
        confirm = messagebox.askyesno("Удаление клиента", f"Вы уверены, что хотите удалить клиента '{user_data[1]}'?\nЭто также удалит всех его питомцев и комментарии к ним.", icon='warning')
        if confirm:
            try:
                self.db_manager.delete_user(user_id)
                self.load_users(filter_term=self.user_search_var.get())
                self.clear_user_details()
            except Exception as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось удалить пользователя: {e}")

    # --- Animal Actions (add, edit, delete) - Обновлено ---
    def add_animal(self):
        if not self.current_user_id:
            messagebox.showinfo("Информация", "Сначала выберите клиента для добавления питомца.")
            return
        _, user_data = self.get_selected_user_data()
        user_name = user_data[1] if user_data else f"ID {self.current_user_id}"

        dialog = AnimalInputDialog(self.root, f"Добавить питомца для {user_name}")
        self.root.wait_window(dialog)

        if dialog.result:
            # dialog.result теперь = (name, type_animal, breed, age, image_base64)
            name, type_animal, breed, age, image_base64 = dialog.result
            try:
                # Передаем image_base64 в метод db_manager
                animal_id = self.db_manager.add_animal(self.current_user_id, name, type_animal, breed, age, image_base64)
                self.load_animals(self.current_user_id)
                for i in range(self.animals_listbox.size()):
                    if self.animals_listbox.get(i).startswith(f"{animal_id}."):
                         self.animals_listbox.selection_clear(0, tk.END)
                         self.animals_listbox.selection_set(i)
                         self.animals_listbox.see(i)
                         self.show_animal_details()
                         break
            except Exception as e:
                 messagebox.showerror("Ошибка базы данных", f"Не удалось добавить питомца: {e}")

    def edit_animal(self, event=None):
        animal_id, animal_data = self.get_selected_animal_data()
        if not animal_data:
            messagebox.showinfo("Изменение", "Выберите питомца для изменения.")
            return
        _, user_data = self.get_selected_user_data()
        user_name = user_data[1] if user_data else f"ID {self.current_user_id}"

        # Передаем все данные animal_data (включая image_base64 в [6]) в диалог
        dialog = AnimalInputDialog(self.root, f"Изменить питомца для {user_name}", animal_data=animal_data)
        self.root.wait_window(dialog)

        if dialog.result:
            name, type_animal, breed, age, image_base64 = dialog.result
            try:
                # Передаем image_base64 в метод db_manager
                self.db_manager.update_animal(animal_id, name, type_animal, breed, age, image_base64)
                selected_indices = self.animals_listbox.curselection()
                self.load_animals(self.current_user_id)
                reselected = False
                for i in range(self.animals_listbox.size()):
                    if self.animals_listbox.get(i).startswith(f"{animal_id}."):
                        self.animals_listbox.selection_clear(0, tk.END)
                        self.animals_listbox.selection_set(i)
                        self.animals_listbox.see(i)
                        self.show_animal_details()
                        reselected = True
                        break
                if not reselected and selected_indices:
                     try:
                         self.animals_listbox.selection_set(selected_indices[0])
                         self.show_animal_details()
                     except tk.TclError: pass
            except Exception as e:
                 messagebox.showerror("Ошибка базы данных", f"Не удалось обновить питомца: {e}")

    def delete_animal(self):
        # (без изменений)
        animal_id, animal_data = self.get_selected_animal_data()
        if not animal_data:
            messagebox.showinfo("Удаление", "Выберите питомца для удаления.")
            return
        confirm = messagebox.askyesno("Удаление питомца", f"Вы уверены, что хотите удалить питомца '{animal_data[2]} ({animal_data[3]})'?\nЭто также удалит все комментарии к нему.", icon='warning')
        if confirm:
            try:
                self.db_manager.delete_animal(animal_id)
                self.load_animals(self.current_user_id)
                self.clear_animal_details()
            except AttributeError:
                 messagebox.showerror("Ошибка Кода", "Метод 'delete_animal' не найден в DatabaseManager.")
            except Exception as e:
                 messagebox.showerror("Ошибка базы данных", f"Не удалось удалить питомца: {e}")

    # --- Comment Actions (get_selected, add, edit, delete) - без изменений ---
    def get_selected_comment_data(self):
        selected_indices = self.comments_listbox.curselection()
        if not selected_indices:
            return None, None
        index = selected_indices[0]
        try:
            comment_data = next((c for i, c in enumerate(self.current_animal_comments) if i == index), None)
            if comment_data:
                return comment_data[0], comment_data # comment_id, full_comment_tuple
            else: return None, None
        except (ValueError, IndexError, AttributeError):
            return None, None

    def add_comment(self):
        if not self.current_animal_id:
            messagebox.showinfo("Информация", "Выберите питомца для добавления комментария.")
            return
        _, animal_data = self.get_selected_animal_data()
        animal_name = animal_data[2] if animal_data else f"ID {self.current_animal_id}"
        comment = simpledialog.askstring("Добавить комментарий", f"Комментарий для {animal_name}:", parent=self.root)
        if comment:
            comment = comment.strip()
            if comment:
                try:
                    comment_id = self.db_manager.add_comment(self.current_animal_id, comment)
                    self.load_comments(self.current_animal_id)
                    last_index = self.comments_listbox.size() - 1
                    if last_index >= 0:
                         self.comments_listbox.selection_clear(0, tk.END)
                         self.comments_listbox.selection_set(last_index)
                         self.comments_listbox.see(last_index)
                except Exception as e:
                    messagebox.showerror("Ошибка базы данных", f"Не удалось добавить комментарий: {e}")

    def edit_comment(self, event=None):
        comment_id, comment_data = self.get_selected_comment_data()
        if not comment_data:
             messagebox.showinfo("Изменение", "Выберите комментарий для изменения.")
             return
        old_comment_text = comment_data[2]
        new_comment = simpledialog.askstring("Изменить комментарий", "Новый текст комментария:",
                                            initialvalue=old_comment_text, parent=self.root)
        if new_comment:
             new_comment = new_comment.strip()
             if new_comment and new_comment != old_comment_text:
                 try:
                     self.db_manager.update_comment(comment_id, new_comment)
                     selected_indices = self.comments_listbox.curselection()
                     self.load_comments(self.current_animal_id)
                     if selected_indices:
                         try:
                             self.comments_listbox.selection_set(selected_indices[0])
                             self.comments_listbox.see(selected_indices[0])
                         except tk.TclError: pass
                 except AttributeError:
                    messagebox.showerror("Ошибка Кода", "Метод 'update_comment' не найден в DatabaseManager.")
                 except Exception as e:
                     messagebox.showerror("Ошибка базы данных", f"Не удалось обновить комментарий: {e}")

    def delete_comment(self):
        comment_id, comment_data = self.get_selected_comment_data()
        if not comment_data:
            messagebox.showinfo("Удаление", "Выберите комментарий для удаления.")
            return
        confirm = messagebox.askyesno("Удаление комментария", f"Вы уверены, что хотите удалить комментарий?", icon='warning')
        if confirm:
            try:
                self.db_manager.delete_comment(comment_id)
                self.load_comments(self.current_animal_id)
            except AttributeError:
                 messagebox.showerror("Ошибка Кода", "Метод 'delete_comment' не найден в DatabaseManager.")
            except Exception as e:
                 messagebox.showerror("Ошибка базы данных", f"Не удалось удалить комментарий: {e}")

    # --- Closing ---
    def on_closing(self):
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            try:
                if hasattr(self, 'db_manager') and self.db_manager:
                    self.db_manager.close()
            except Exception as e:
                print(f"Error closing database connection: {e}")
            finally:
                self.root.destroy()

# --- Main Execution ---
def main():
    root = tk.Tk()
    # Установим иконку окна (опционально, нужен .ico файл)
    # try:
    #     root.iconbitmap('path/to/your/icon.ico') # Замените на реальный путь
    # except tk.TclError:
    #     print("Не удалось загрузить иконку окна. Убедитесь, что файл .ico существует.")

    app = VetClinicApp(root)
    if root.winfo_exists():
        root.mainloop()

if __name__ == '__main__':
    # Убедитесь, что Pillow установлен: pip install Pillow
    from PIL import Image, ImageTk, UnidentifiedImageError # Импортируем UnidentifiedImageError
    main()