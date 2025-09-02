import os
import sys
import shutil
import json
import sqlite3
from pathlib import Path
from datetime import datetime
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

class UpdateManager:
    def __init__(self):
        self.current_version = self.get_current_version()
        self.data_dir = self.get_data_directory()
        self.backup_dir = os.path.join(self.data_dir, 'backup')
        
    def get_current_version(self):
        """Получает текущую версию приложения"""
        try:
            # Сначала пытаемся получить из встроенного файла
            if getattr(sys, 'frozen', False):
                # Если приложение собрано в exe
                base_path = sys._MEIPASS
                version_file = os.path.join(base_path, 'version.txt')
            else:
                # Если запущено из исходного кода
                version_file = 'version.txt'
            
            if os.path.exists(version_file):
                with open(version_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
        except:
            pass
        
        # Если не удалось получить версию, возвращаем по умолчанию
        return "1.0.0"
    
    def get_data_directory(self):
        """Получает директорию с данными"""
        if getattr(sys, 'frozen', False):
            # Если приложение собрано в exe
            base_path = os.path.dirname(sys.executable)
            data_dir = os.path.join(base_path, 'data')
        else:
            # Если запущено из исходного кода
            data_dir = 'data'
        
        # Создаем директорию, если её нет
        os.makedirs(data_dir, exist_ok=True)
        return data_dir
    
    def backup_database(self):
        """Создает резервную копию базы данных"""
        try:
            # Создаем папку для резервных копий
            os.makedirs(self.backup_dir, exist_ok=True)
            
            # Путь к базе данных
            db_path = os.path.join(self.data_dir, 'abonent.db')
            
            if os.path.exists(db_path):
                # Создаем имя файла резервной копии с временной меткой
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"abonent_backup_{timestamp}.db"
                backup_path = os.path.join(self.backup_dir, backup_name)
                
                # Копируем базу данных
                shutil.copy2(db_path, backup_path)
                print(f"✅ Резервная копия создана: {backup_name}")
                return backup_path
            else:
                print("⚠️ База данных не найдена для резервного копирования")
                return None
        except Exception as e:
            print(f"❌ Ошибка при создании резервной копии: {e}")
            return None
    
    def restore_database(self, backup_path):
        """Восстанавливает базу данных из резервной копии"""
        try:
            if backup_path and os.path.exists(backup_path):
                db_path = os.path.join(self.data_dir, 'abonent.db')
                shutil.copy2(backup_path, db_path)
                print(f"✅ База данных восстановлена из: {os.path.basename(backup_path)}")
                return True
            else:
                print("❌ Файл резервной копии не найден")
                return False
        except Exception as e:
            print(f"❌ Ошибка при восстановлении базы данных: {e}")
            return False
    
    def check_database_integrity(self):
        """Проверяет целостность базы данных"""
        try:
            db_path = os.path.join(self.data_dir, 'abonent.db')
            if not os.path.exists(db_path):
                print("⚠️ База данных не найдена")
                return False
            
            # Подключаемся к базе данных и проверяем основные таблицы
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Проверяем наличие основных таблиц
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['abonents', 'monthly_data']
            missing_tables = [table for table in required_tables if table not in tables]
            
            if missing_tables:
                print(f"❌ Отсутствуют таблицы: {missing_tables}")
                conn.close()
                return False
            
            # Проверяем количество записей
            cursor.execute("SELECT COUNT(*) FROM abonents")
            abonents_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM monthly_data")
            monthly_data_count = cursor.fetchone()[0]
            
            print(f"📊 Проверка базы данных:")
            print(f"   - Абонентов: {abonents_count}")
            print(f"   - Записей месячных данных: {monthly_data_count}")
            
            conn.close()
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при проверке базы данных: {e}")
            return False
    
    def show_update_info(self):
        """Показывает информацию об обновлении"""
        try:
            # Получаем информацию об обновлении
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
                update_info_file = os.path.join(base_path, 'update_info.json')
            else:
                update_info_file = 'update_info.json'
            
            if os.path.exists(update_info_file):
                with open(update_info_file, 'r', encoding='utf-8') as f:
                    update_info = json.load(f)
                
                # Создаем окно с информацией
                self.create_info_window(update_info)
            else:
                print("⚠️ Файл информации об обновлении не найден")
                
        except Exception as e:
            print(f"❌ Ошибка при загрузке информации об обновлении: {e}")
    
    def create_info_window(self, update_info):
        """Создает окно с информацией об обновлении"""
        root = ctk.CTk()
        root.title("Информация об обновлении")
        root.geometry("500x400")
        root.resizable(False, False)
        
        # Основной контейнер
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Заголовок
        title_label = ctk.CTkLabel(main_frame, 
                                  text="🔄 Информация об обновлении",
                                  font=("Roboto", 18, "bold"))
        title_label.pack(pady=10)
        
        # Информация о версии
        version_frame = ctk.CTkFrame(main_frame)
        version_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(version_frame, 
                    text=f"📋 Версия: {update_info.get('version', 'Неизвестно')}",
                    font=("Roboto", 14, "bold")).pack(pady=5)
        
        build_date = update_info.get('build_date', 'Неизвестно')
        if build_date != 'Неизвестно':
            try:
                date_obj = datetime.fromisoformat(build_date)
                formatted_date = date_obj.strftime("%d.%m.%Y %H:%M")
                ctk.CTkLabel(version_frame, 
                            text=f"📅 Дата сборки: {formatted_date}",
                            font=("Roboto", 12)).pack(pady=2)
            except:
                pass
        
        # Новые функции
        features_frame = ctk.CTkFrame(main_frame)
        features_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(features_frame, 
                    text="🆕 Новые функции:",
                    font=("Roboto", 14, "bold")).pack(pady=5)
        
        features = update_info.get('features', [])
        for feature in features:
            ctk.CTkLabel(features_frame, 
                        text=f"• {feature}",
                        font=("Roboto", 12)).pack(pady=2, anchor="w")
        
        # Кнопка закрытия
        close_button = ctk.CTkButton(main_frame, 
                                   text="Закрыть",
                                   command=root.destroy,
                                   height=35)
        close_button.pack(pady=10)
        
        root.mainloop()
    
    def run_update_check(self):
        """Запускает проверку обновлений"""
        print(f"🔍 Проверка обновлений...")
        print(f"📋 Текущая версия: {self.current_version}")
        print(f"📁 Директория данных: {self.data_dir}")
        
        # Проверяем целостность базы данных
        if self.check_database_integrity():
            print("✅ База данных в порядке")
        else:
            print("❌ Проблемы с базой данных")
        
        # Создаем резервную копию
        backup_path = self.backup_database()
        
        # Показываем информацию об обновлении
        self.show_update_info()
        
        return backup_path

def main():
    """Главная функция"""
    print("🚀 Запуск системы обновлений ComunalKorm...")
    
    updater = UpdateManager()
    backup_path = updater.run_update_check()
    
    print("\n📋 Инструкция по обновлению:")
    print("1. Закройте приложение ComunalKorm")
    print("2. Замените файл ComunalKorm.exe на новую версию")
    print("3. Запустите приложение снова")
    print("4. Данные будут автоматически сохранены")
    
    if backup_path:
        print(f"💾 Резервная копия создана: {os.path.basename(backup_path)}")
    
    input("\nНажмите Enter для продолжения...")

if __name__ == "__main__":
    main() 