import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from database_module import DatabaseManager

# UserInputDialog and AnimalInputDialog remain the same...
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


class AnimalInputDialog(tk.Toplevel):
    def __init__(self, parent, title, animal_data=None):
        super().__init__(parent)
        self.transient(parent) # Make it a transient window
        self.grab_set()      # Grab focus
        self.title(title)
        self.geometry('400x400')
        self.result = None
        self.configure(bg='#f0f0f0')

        frame = tk.Frame(self, bg='#f0f0f0')
        frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Стили для виджетов
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

        # Заполнение данными если редактирование
        if animal_data:
            self.name_entry.insert(0, animal_data[2])
            self.type_entry.insert(0, animal_data[3] or '')
            self.breed_entry.insert(0, animal_data[4] or '')
            self.age_entry.insert(0, str(animal_data[5]) if animal_data[5] is not None else '')

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
        type_animal = self.type_entry.get().strip()
        breed = self.breed_entry.get().strip()
        age_str = self.age_entry.get().strip()
        age = None

        if age_str:
             try:
                 age = int(age_str)
                 if age < 0: # Basic validation
                     messagebox.showerror("Ошибка", "Возраст не может быть отрицательным!", parent=self)
                     return
             except ValueError:
                 messagebox.showerror("Ошибка", "Возраст должен быть целым числом!", parent=self)
                 return

        if not name or not type_animal:
            messagebox.showerror("Ошибка", "Имя и вид обязательны для заполнения!", parent=self)
            return

        self.result = (name, type_animal, breed, age)
        self.destroy()

    def cancel(self):
        self.result = None # Ensure result is None on cancel
        self.destroy()


class VetClinicApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Ветеринарная Клиника')
        self.root.geometry('1200x800')
        self.root.configure(bg='#f0f0f0')

        try:
            self.db_manager = DatabaseManager()
        except Exception as e:
            messagebox.showerror("Ошибка Базы Данных", f"Не удалось подключиться или инициализировать базу данных:\n{e}")
            self.root.destroy() # Close app if DB fails
            return

        # Главный контейнер
        self.main_frame = tk.Frame(root, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Разделение на три колонки
        self.create_users_column()
        self.create_user_details_column()
        self.create_animal_details_column()

        # Загрузка пользователей при старте
        self.load_users()
        self.current_user_id = None
        self.current_animal_id = None

        # Add protocol for clean DB closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def create_users_column(self):
        # Левая колонка - список пользователей
        left_frame = tk.Frame(self.main_frame, bg='#e0e0e0', bd=1, relief=tk.SUNKEN) # Slightly different bg
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        left_frame.pack_propagate(False) # Prevent resizing based on content too much

        tk.Label(left_frame, text='Клиенты',
                 font=('Arial', 14, 'bold'), bg='#e0e0e0').pack(pady=(10, 5))

        # Add a search bar
        search_frame = tk.Frame(left_frame, bg='#e0e0e0')
        search_frame.pack(fill=tk.X, padx=10, pady=5)
        tk.Label(search_frame, text='Поиск:', bg='#e0e0e0').pack(side=tk.LEFT)
        self.user_search_var = tk.StringVar()
        self.user_search_entry = tk.Entry(search_frame, textvariable=self.user_search_var)
        self.user_search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        self.user_search_var.trace_add('write', self.filter_users) # Use trace_add for modern tkinter

        list_frame = tk.Frame(left_frame) # Frame for listbox and scrollbar
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        user_scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.users_listbox = tk.Listbox(list_frame, width=40,
                                        font=('Arial', 10),
                                        selectbackground='#a6a6a6',
                                        exportselection=False, # <--- FIX HERE
                                        yscrollcommand=user_scrollbar.set)
        user_scrollbar.config(command=self.users_listbox.yview)
        user_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.users_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.users_listbox.bind('<<ListboxSelect>>', self.show_user_details)
        self.users_listbox.bind('<Double-Button-1>', self.edit_user) # Add double-click to edit

        users_button_frame = tk.Frame(left_frame, bg='#e0e0e0')
        users_button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(users_button_frame, text='Добавить',
                  command=self.add_user,
                  bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'), width=10).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(users_button_frame, text='Изменить',
                  command=self.edit_user,
                  bg='#FFC107', fg='black', font=('Arial', 10, 'bold'), width=10).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(users_button_frame, text='Удалить',
                  command=self.delete_user,
                  bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=10).pack(side=tk.RIGHT, expand=True, padx=5)


    def create_user_details_column(self):
        # Центральная колонка - информация о пользователе
        center_frame = tk.Frame(self.main_frame, bg='#e8e8e8', bd=1, relief=tk.SUNKEN)
        center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        center_frame.pack_propagate(False)

        tk.Label(center_frame, text='Информация о клиенте',
                 font=('Arial', 14, 'bold'), bg='#e8e8e8').pack(pady=(10, 5))

        self.user_info_frame = tk.Frame(center_frame, bg='#e8e8e8')
        self.user_info_frame.pack(fill=tk.X, padx=10, pady=5) # Don't expand vertically

        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()

        info_style = {'font': ('Arial', 11), 'bg': '#e8e8e8', 'anchor': 'w', 'pady': 2} # Increased font size

        tk.Label(self.user_info_frame, text="ФИО:", font=('Arial', 11, 'bold'), bg='#e8e8e8', anchor='w').grid(row=0, column=0, sticky='w')
        tk.Label(self.user_info_frame, textvariable=self.name_var, **info_style).grid(row=0, column=1, sticky='w', padx=5)
        tk.Label(self.user_info_frame, text="Телефон:", font=('Arial', 11, 'bold'), bg='#e8e8e8', anchor='w').grid(row=1, column=0, sticky='w')
        tk.Label(self.user_info_frame, textvariable=self.phone_var, **info_style).grid(row=1, column=1, sticky='w', padx=5)
        tk.Label(self.user_info_frame, text="Email:", font=('Arial', 11, 'bold'), bg='#e8e8e8', anchor='w').grid(row=2, column=0, sticky='w')
        tk.Label(self.user_info_frame, textvariable=self.email_var, **info_style).grid(row=2, column=1, sticky='w', padx=5)

        # Список животных пользователя
        tk.Label(center_frame, text='Питомцы клиента',
                 font=('Arial', 14, 'bold'), bg='#e8e8e8').pack(pady=(15, 5))

        anim_list_frame = tk.Frame(center_frame) # Frame for listbox and scrollbar
        anim_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        animal_scrollbar = tk.Scrollbar(anim_list_frame, orient=tk.VERTICAL)
        self.animals_listbox = tk.Listbox(anim_list_frame, width=40,
                                          font=('Arial', 10),
                                          selectbackground='#a6a6a6',
                                          exportselection=False, # <--- FIX HERE
                                          yscrollcommand=animal_scrollbar.set)
        animal_scrollbar.config(command=self.animals_listbox.yview)
        animal_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.animals_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.animals_listbox.bind('<<ListboxSelect>>', self.show_animal_details)
        self.animals_listbox.bind('<Double-Button-1>', self.edit_animal) # Add double-click to edit

        animals_button_frame = tk.Frame(center_frame, bg='#e8e8e8')
        animals_button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(animals_button_frame, text='Добавить',
                  command=self.add_animal,
                  bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'), width=10).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(animals_button_frame, text='Изменить',
                  command=self.edit_animal,
                  bg='#FFC107', fg='black', font=('Arial', 10, 'bold'), width=10).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(animals_button_frame, text='Удалить',
                  command=self.delete_animal,
                  bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=10).pack(side=tk.RIGHT, expand=True, padx=5)


    def create_animal_details_column(self):
        # Правая колонка - информация о животном и комментарии
        right_frame = tk.Frame(self.main_frame, bg='#f0f0f0', bd=1, relief=tk.SUNKEN)
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        right_frame.pack_propagate(False)

        tk.Label(right_frame, text='Информация о питомце',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=(10, 5))

        self.animal_info_frame = tk.Frame(right_frame, bg='#f0f0f0')
        self.animal_info_frame.pack(fill=tk.X, padx=10, pady=5) # Don't expand vertically

        self.animal_name_var = tk.StringVar()
        self.animal_type_var = tk.StringVar()
        self.animal_breed_var = tk.StringVar()
        self.animal_age_var = tk.StringVar()

        info_style = {'font': ('Arial', 11), 'bg': '#f0f0f0', 'anchor': 'w', 'pady': 2} # Increased font size

        tk.Label(self.animal_info_frame, text="Имя:", font=('Arial', 11, 'bold'), bg='#f0f0f0', anchor='w').grid(row=0, column=0, sticky='w')
        tk.Label(self.animal_info_frame, textvariable=self.animal_name_var, **info_style).grid(row=0, column=1, sticky='w', padx=5)
        tk.Label(self.animal_info_frame, text="Вид:", font=('Arial', 11, 'bold'), bg='#f0f0f0', anchor='w').grid(row=1, column=0, sticky='w')
        tk.Label(self.animal_info_frame, textvariable=self.animal_type_var, **info_style).grid(row=1, column=1, sticky='w', padx=5)
        tk.Label(self.animal_info_frame, text="Порода:", font=('Arial', 11, 'bold'), bg='#f0f0f0', anchor='w').grid(row=2, column=0, sticky='w')
        tk.Label(self.animal_info_frame, textvariable=self.animal_breed_var, **info_style).grid(row=2, column=1, sticky='w', padx=5)
        tk.Label(self.animal_info_frame, text="Возраст:", font=('Arial', 11, 'bold'), bg='#f0f0f0', anchor='w').grid(row=3, column=0, sticky='w')
        tk.Label(self.animal_info_frame, textvariable=self.animal_age_var, **info_style).grid(row=3, column=1, sticky='w', padx=5)

        # Список комментариев о животном
        tk.Label(right_frame, text='История посещений / Комментарии',
                 font=('Arial', 14, 'bold'), bg='#f0f0f0').pack(pady=(15, 5))

        comment_list_frame = tk.Frame(right_frame) # Frame for listbox and scrollbar
        comment_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        comment_scrollbar = tk.Scrollbar(comment_list_frame, orient=tk.VERTICAL)
        self.comments_listbox = tk.Listbox(comment_list_frame, width=40,
                                           font=('Arial', 10),
                                           selectbackground='#a6a6a6',
                                           exportselection=False, # Keep selection visible
                                           yscrollcommand=comment_scrollbar.set)
        comment_scrollbar.config(command=self.comments_listbox.yview)
        comment_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.comments_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.comments_listbox.bind('<Double-Button-1>', self.edit_comment) # Add double-click to edit

        comments_button_frame = tk.Frame(right_frame, bg='#f0f0f0')
        comments_button_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Button(comments_button_frame, text='Добавить',
                  command=self.add_comment,
                  bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'), width=10).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(comments_button_frame, text='Изменить',
                  command=self.edit_comment,
                  bg='#FFC107', fg='black', font=('Arial', 10, 'bold'), width=10).pack(side=tk.LEFT, expand=True, padx=5)
        tk.Button(comments_button_frame, text='Удалить',
                  command=self.delete_comment,
                  bg='#f44336', fg='white', font=('Arial', 10, 'bold'), width=10).pack(side=tk.RIGHT, expand=True, padx=5)


    def load_users(self, filter_term=""):
        """Loads users into the listbox, optionally filtering by name or phone."""
        try:
            self.users_listbox.delete(0, tk.END)
            self.clear_user_details() # Clear details when reloading users
            users = self.db_manager.get_users()
            self.all_users_data = users # Store all users for filtering

            filter_term = filter_term.lower()
            for user in users:
                user_id, name, phone, email = user
                display_phone = phone or 'Без телефона'
                list_string = f"{user_id}. {name} ({display_phone})"
                # Filter logic
                if not filter_term or filter_term in name.lower() or (phone and filter_term in phone):
                    self.users_listbox.insert(tk.END, list_string)
                    # Store full user data associated with the listbox item for easier retrieval
                    # self.users_listbox.itemconfig(tk.END, {'data': user}) # <-- REMOVE THIS LINE
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пользователей: {e}")
            self.all_users_data = []

    def filter_users(self, *args):
        """Callback function for the search entry."""
        search_term = self.user_search_var.get()
        self.load_users(filter_term=search_term)


    def get_selected_user_data(self):
        """Helper to get full data tuple for the selected user."""
        selected_indices = self.users_listbox.curselection()
        if not selected_indices:
            return None, None
        
        index = selected_indices[0]
        list_string = self.users_listbox.get(index)
        try:
            user_id = int(list_string.split('.')[0])
            # Retrieve the stored data if available (more robust)
            # item_config = self.users_listbox.itemconfig(index) # Doesn't work as expected for data retrieval
            # A slightly less efficient but reliable way: find the user by ID in the stored list
            user_data = next((u for u in self.all_users_data if u[0] == user_id), None)
            return user_id, user_data
        except (ValueError, IndexError):
             messagebox.showerror("Ошибка", "Не удалось получить ID пользователя из списка.")
             return None, None


    def show_user_details(self, event=None):
        user_id, user_data = self.get_selected_user_data()

        if user_id is None:
             # This might happen if the list is empty or selection is cleared programmatically
             self.clear_user_details()
             return
        
        if user_data:
            self.current_user_id = user_id
            # self.name_var.set(f"ФИО: {user_data[1]}")
            # self.phone_var.set(f"Телефон: {user_data[2] or 'Не указан'}")
            # self.email_var.set(f"Email: {user_data[3] or 'Не указан'}")
            self.name_var.set(f"{user_data[1]}")
            self.phone_var.set(f"{user_data[2] or 'Не указан'}")
            self.email_var.set(f"{user_data[3] or 'Не указан'}")

            # Загрузка животных пользователя
            self.load_animals(user_id)
        else:
            # If user_data wasn't found (shouldn't happen with current load_users)
            self.clear_user_details()
            # messagebox.showwarning("Предупреждение", f"Не удалось найти данные для пользователя ID {user_id}.")


    def load_animals(self, user_id):
        """Loads animals for a given user ID into the animals listbox."""
        self.animals_listbox.delete(0, tk.END)
        self.clear_animal_details() # Clear animal details when loading new list
        try:
            animals = self.db_manager.get_animals_by_user(user_id)
            self.current_user_animals = animals # Store for later use
            for animal in animals:
                # animal structure: (animal_id, owner_id, name, type, breed, age)
                list_string = f"{animal[0]}. {animal[2]} ({animal[3]})"
                self.animals_listbox.insert(tk.END, list_string)
                # Store full animal data with the item
                # self.animals_listbox.itemconfig(tk.END, {'data': animal}) # <-- REMOVE THIS LINE

        except Exception as e:
             messagebox.showerror("Ошибка", f"Не удалось загрузить животных: {e}")
             self.current_user_animals = []


    def get_selected_animal_data(self):
        """Helper to get full data tuple for the selected animal."""
        selected_indices = self.animals_listbox.curselection()
        if not selected_indices:
            return None, None
            
        index = selected_indices[0]
        list_string = self.animals_listbox.get(index)
        try:
            animal_id = int(list_string.split('.')[0])
            # Find the animal by ID in the stored list for the current user
            animal_data = next((a for a in self.current_user_animals if a[0] == animal_id), None)
            return animal_id, animal_data
        except (ValueError, IndexError, AttributeError): # Added AttributeError check for self.current_user_animals
             # Don't show error here, might just be switching users
             # messagebox.showerror("Ошибка", "Не удалось получить ID животного из списка.")
             return None, None


    def show_animal_details(self, event=None):
        animal_id, animal_data = self.get_selected_animal_data()

        if animal_id is None:
            self.clear_animal_details()
            return

        if animal_data:
            self.current_animal_id = animal_id
            # self.animal_name_var.set(f"Имя: {animal_data[2]}")
            # self.animal_type_var.set(f"Вид: {animal_data[3] or 'Не указан'}")
            # self.animal_breed_var.set(f"Порода: {animal_data[4] or 'Не указана'}")
            # age_display = str(animal_data[5]) if animal_data[5] is not None else 'Не указан'
            # self.animal_age_var.set(f"Возраст: {age_display}")
            self.animal_name_var.set(f"{animal_data[2]}")
            self.animal_type_var.set(f"{animal_data[3] or 'Не указан'}")
            self.animal_breed_var.set(f"{animal_data[4] or 'Не указана'}")
            age_display = str(animal_data[5]) if animal_data[5] is not None else 'Не указан'
            self.animal_age_var.set(f"{age_display}")

            # Загрузка комментариев о животном
            self.load_comments(animal_id)
        else:
             self.clear_animal_details()
             # messagebox.showwarning("Предупреждение", f"Не удалось найти данные для животного ID {animal_id}.")


    def load_comments(self, animal_id):
        """Loads comments for a given animal ID into the comments listbox."""
        self.comments_listbox.delete(0, tk.END)
        try:
            comments = self.db_manager.get_comments_by_animal(animal_id)
            self.current_animal_comments = comments # Store for later use
            for comment in comments:
                # comment structure: (comment_id, animal_id, text, timestamp)
                timestamp = comment[3] # Assuming it's a string from DB
                list_string = f"{comment[2]} ({timestamp})" # Original format
                self.comments_listbox.insert(tk.END, list_string)
                # Store full comment data with the item
                # self.comments_listbox.itemconfig(tk.END, {'data': comment}) # <-- REMOVE THIS LINE

        except Exception as e:
             messagebox.showerror("Ошибка", f"Не удалось загрузить комментарии: {e}")
             self.current_animal_comments = []


    def clear_user_details(self):
        self.current_user_id = None
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.animals_listbox.delete(0, tk.END)
        self.current_user_animals = [] # Clear stored animal data
        self.clear_animal_details()

    def clear_animal_details(self):
        self.current_animal_id = None
        self.animal_name_var.set("")
        self.animal_type_var.set("")
        self.animal_breed_var.set("")
        self.animal_age_var.set("")
        self.comments_listbox.delete(0, tk.END)
        self.current_animal_comments = [] # Clear stored comment data


    def add_user(self):
        dialog = UserInputDialog(self.root, "Добавить клиента")
        self.root.wait_window(dialog)

        if dialog.result:
            name, phone, email = dialog.result
            try:
                user_id = self.db_manager.add_user(name, phone, email)
                self.load_users(filter_term=self.user_search_var.get()) # Reload with current filter
                # Optionally select the newly added user
                for i in range(self.users_listbox.size()):
                    if self.users_listbox.get(i).startswith(f"{user_id}."):
                        self.users_listbox.selection_clear(0, tk.END)
                        self.users_listbox.selection_set(i)
                        self.users_listbox.see(i) # Ensure visible
                        self.show_user_details()
                        break
            except Exception as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось добавить пользователя: {e}")

    def edit_user(self, event=None):
        """Opens the dialog to edit the selected user."""
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
                # Find current selection index before reloading
                selected_indices = self.users_listbox.curselection()
                
                self.load_users(filter_term=self.user_search_var.get()) # Reload list
                
                # Try to re-select the edited user by ID
                reselected = False
                for i in range(self.users_listbox.size()):
                    if self.users_listbox.get(i).startswith(f"{user_id}."):
                        self.users_listbox.selection_clear(0, tk.END)
                        self.users_listbox.selection_set(i)
                        self.users_listbox.see(i)
                        self.show_user_details() # Update details pane
                        reselected = True
                        break
                if not reselected and selected_indices: # Fallback to original index if ID search fails
                     try:
                         self.users_listbox.selection_set(selected_indices[0])
                         self.show_user_details()
                     except tk.TclError: # Index might be out of bounds if list changed size
                         pass

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
                self.db_manager.delete_user(user_id) # Assumes cascade delete is set up in DB or handled in method
                self.load_users(filter_term=self.user_search_var.get()) # Reload list
                self.clear_user_details() # Clear details as user is gone
            except Exception as e:
                messagebox.showerror("Ошибка базы данных", f"Не удалось удалить пользователя: {e}")


    def add_animal(self):
        if not self.current_user_id:
            messagebox.showinfo("Информация", "Сначала выберите клиента для добавления питомца.")
            return
            
        _, user_data = self.get_selected_user_data() # Get user name for context
        user_name = user_data[1] if user_data else f"ID {self.current_user_id}"

        dialog = AnimalInputDialog(self.root, f"Добавить питомца для {user_name}")
        self.root.wait_window(dialog)

        if dialog.result:
            name, type_animal, breed, age = dialog.result
            try:
                animal_id = self.db_manager.add_animal(self.current_user_id, name, type_animal, breed, age)
                # Reload animals for the current user and select the new one
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
        """Opens the dialog to edit the selected animal."""
        animal_id, animal_data = self.get_selected_animal_data()
        if not animal_data:
            messagebox.showinfo("Изменение", "Выберите питомца для изменения.")
            return
            
        _, user_data = self.get_selected_user_data() # Get user name for context
        user_name = user_data[1] if user_data else f"ID {self.current_user_id}"

        dialog = AnimalInputDialog(self.root, f"Изменить питомца для {user_name}", animal_data=animal_data)
        self.root.wait_window(dialog)

        if dialog.result:
            name, type_animal, breed, age = dialog.result
            try:
                self.db_manager.update_animal(animal_id, name, type_animal, breed, age)
                # Find current selection index before reloading
                selected_indices = self.animals_listbox.curselection()
                
                self.load_animals(self.current_user_id) # Reload list
                
                # Try to re-select the edited animal by ID
                reselected = False
                for i in range(self.animals_listbox.size()):
                    if self.animals_listbox.get(i).startswith(f"{animal_id}."):
                        self.animals_listbox.selection_clear(0, tk.END)
                        self.animals_listbox.selection_set(i)
                        self.animals_listbox.see(i)
                        self.show_animal_details() # Update details pane
                        reselected = True
                        break
                if not reselected and selected_indices: # Fallback to original index if ID search fails
                     try:
                         self.animals_listbox.selection_set(selected_indices[0])
                         self.show_animal_details()
                     except tk.TclError:
                         pass # Index might be out of bounds

            except Exception as e:
                 messagebox.showerror("Ошибка базы данных", f"Не удалось обновить питомца: {e}")


    def delete_animal(self):
        animal_id, animal_data = self.get_selected_animal_data()
        if not animal_data:
            messagebox.showinfo("Удаление", "Выберите питомца для удаления.")
            return

        confirm = messagebox.askyesno("Удаление питомца", f"Вы уверены, что хотите удалить питомца '{animal_data[2]} ({animal_data[3]})'?\nЭто также удалит все комментарии к нему.", icon='warning')
        if confirm:
            try:
                # Ensure you have a specific delete_animal method in db_manager
                self.db_manager.delete_animal(animal_id) # Assumes cascade or method handles comments
                self.load_animals(self.current_user_id) # Reload list for current user
                self.clear_animal_details() # Clear details as animal is gone
            except AttributeError:
                 messagebox.showerror("Ошибка Кода", "Метод 'delete_animal' не найден в DatabaseManager.")
            except Exception as e:
                 messagebox.showerror("Ошибка базы данных", f"Не удалось удалить питомца: {e}")

    # --- Comment Methods ---

    def get_selected_comment_data(self):
        """Helper to get full data tuple for the selected comment."""
        selected_indices = self.comments_listbox.curselection()
        if not selected_indices:
            return None, None
            
        index = selected_indices[0]
        # Need to retrieve the actual comment ID. Parsing the string is fragile.
        # Best to rely on the stored data if possible.
        try:
            # Find the comment data by matching the listbox string - less ideal
            # list_string = self.comments_listbox.get(index) # Example: "Comment text (timestamp)" or "ID. Timestamp: Text"
            # A better way using stored data:
            comment_data = next((c for i, c in enumerate(self.current_animal_comments) if i == index), None)

            if comment_data:
                return comment_data[0], comment_data # comment_id, full_comment_tuple
            else:
                 # Fallback: Try parsing ID if your format includes it reliably at the start
                 list_string = self.comments_listbox.get(index)
                 if '.' in list_string:
                     comment_id = int(list_string.split('.')[0])
                     comment_data_fallback = next((c for c in self.current_animal_comments if c[0] == comment_id), None)
                     return comment_id, comment_data_fallback
                 else:
                    return None, None # Cannot reliably get ID

        except (ValueError, IndexError, AttributeError):
            # Don't show error, selection might just be changing
            return None, None


    def add_comment(self):
        if not self.current_animal_id:
            messagebox.showinfo("Информация", "Выберите питомца для добавления комментария.")
            return
            
        _, animal_data = self.get_selected_animal_data()
        animal_name = animal_data[2] if animal_data else f"ID {self.current_animal_id}"

        comment = simpledialog.askstring("Добавить комментарий", f"Комментарий для {animal_name}:", parent=self.root)

        if comment: # Check if comment is not empty and not None (if cancelled)
            comment = comment.strip()
            if comment: # Check again after stripping whitespace
                try:
                    comment_id = self.db_manager.add_comment(self.current_animal_id, comment)
                    # Reload comments and select the new one
                    self.load_comments(self.current_animal_id)
                    for i in range(self.comments_listbox.size()):
                        # Need a reliable way to find the new comment, ID is best
                        # if self.comments_listbox.get(i).startswith(f"{comment_id}."): # If using ID format
                        # Find by matching text and timestamp (less reliable) or better: use stored data
                        list_data = self.comments_listbox.get(i) # Check based on your format
                        # This selection part is tricky without IDs in the listbox string.
                        # For now, just reloading might be sufficient.
                        pass # Simplified: just reload
                    # To select last item:
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
             
        # comment_data structure: (comment_id, animal_id, text, timestamp)
        old_comment_text = comment_data[2]
        
        new_comment = simpledialog.askstring("Изменить комментарий", "Новый текст комментария:",
                                            initialvalue=old_comment_text, parent=self.root)

        if new_comment: # Check if not None (cancelled)
             new_comment = new_comment.strip()
             if new_comment and new_comment != old_comment_text: # Check if changed and not empty
                 try:
                     # You need an update_comment method in db_manager
                     self.db_manager.update_comment(comment_id, new_comment)
                     # Find current selection index before reloading
                     selected_indices = self.comments_listbox.curselection()

                     self.load_comments(self.current_animal_id) # Reload list
                     
                     # Try to re-select the edited comment
                     if selected_indices:
                         try:
                             # Reselect based on index - might be wrong if order changed
                             self.comments_listbox.selection_set(selected_indices[0])
                             self.comments_listbox.see(selected_indices[0])
                         except tk.TclError:
                             pass # Index out of bounds
                 except AttributeError:
                    messagebox.showerror("Ошибка Кода", "Метод 'update_comment' не найден в DatabaseManager.")
                 except Exception as e:
                     messagebox.showerror("Ошибка базы данных", f"Не удалось обновить комментарий: {e}")


    def delete_comment(self):
        comment_id, comment_data = self.get_selected_comment_data()
        if not comment_data:
            messagebox.showinfo("Удаление", "Выберите комментарий для удаления.")
            return

        confirm = messagebox.askyesno("Удаление комментария", f"Вы уверены, что хотите удалить комментарий?", icon='warning') # Removed specific text for privacy/simplicity
        if confirm:
            try:
                # Ensure you have a specific delete_comment method in db_manager
                self.db_manager.delete_comment(comment_id)
                self.load_comments(self.current_animal_id) # Reload list
            except AttributeError:
                 messagebox.showerror("Ошибка Кода", "Метод 'delete_comment' не найден в DatabaseManager.")
            except Exception as e:
                 messagebox.showerror("Ошибка базы данных", f"Не удалось удалить комментарий: {e}")


    def on_closing(self):
        """Handles window closing event."""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            try:
                if hasattr(self, 'db_manager') and self.db_manager:
                    self.db_manager.close()
                    print("Database connection closed.")
            except Exception as e:
                print(f"Error closing database connection: {e}")
            finally:
                self.root.destroy()


# --- Main Execution ---
def main():
    root = tk.Tk()
    app = VetClinicApp(root)
    # Only run mainloop if app initialization didn't fail (e.g., DB connection error)
    if root.winfo_exists():
        root.mainloop()

if __name__ == '__main__':
    main()