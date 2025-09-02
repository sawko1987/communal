import PyInstaller.__main__
import os
import shutil
import time
import sys
import tempfile
import json
from pathlib import Path
from datetime import datetime

def safe_remove_dir(dir_path):
    """Безопасное удаление директории с повторными попытками"""
    if os.path.exists(dir_path):
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                shutil.rmtree(dir_path)
                print(f"Успешно удалена директория: {dir_path}")
                return True
            except PermissionError:
                print(f"Попытка {attempt + 1}/{max_attempts}: Нет доступа к {dir_path}")
                if attempt < max_attempts - 1:
                    time.sleep(1)
            except Exception as e:
                print(f"Ошибка при удалении {dir_path}: {e}")
                return False
    return True

def get_version():
    """Получает версию из файла version.txt"""
    try:
        with open('version.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except:
        return "1.0.0"

def create_update_info():
    """Создает информацию об обновлении"""
    version = get_version()
    update_info = {
        "version": version,
        "build_date": datetime.now().isoformat(),
        "features": [
            "Генерация реестров по всем абонентам",
            "Улучшенный интерфейс с вкладками",
            "Система обновлений без потери данных"
        ]
    }
    
    # Сохраняем информацию об обновлении
    with open('update_info.json', 'w', encoding='utf-8') as f:
        json.dump(update_info, f, indent=2, ensure_ascii=False)
    
    return update_info

def build_exe():
    print("🚀 Начало сборки ComunalKorm...")
    
    # Получаем версию
    version = get_version()
    print(f"📋 Версия: {version}")
    
    # Получаем абсолютный путь к текущей директории
    current_dir = os.path.abspath(os.path.dirname(__file__))
    
    # Создаем временную директорию для сборки
    temp_dir = tempfile.mkdtemp()
    print(f"📁 Создана временная директория: {temp_dir}")
    
    try:
        # Копируем необходимые файлы во временную директорию
        files_to_copy = [
            'main.py', 'users_db.py', 'HistoryWindow.py', 'add_abonent_window.py', 
            'monthly_data_window.py', 'edit_abonent_window.py', 'settings_window.py',
            'updater.py', 'version.txt', 'requirements.txt'
        ]
        
        dirs_to_copy = ['image', 'data']
        
        for item in files_to_copy:
            src_path = os.path.join(current_dir, item)
            dst_path = os.path.join(temp_dir, item)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
                print(f"📄 Скопирован файл: {item}")
        
        for item in dirs_to_copy:
            src_path = os.path.join(current_dir, item)
            dst_path = os.path.join(temp_dir, item)
            if os.path.exists(src_path):
                shutil.copytree(src_path, dst_path)
                print(f"📁 Скопирована папка: {item}")
        
        # Создаем информацию об обновлении
        update_info = create_update_info()
        print(f"📝 Создана информация об обновлении: {update_info['version']}")
        
        # Переходим во временную директорию
        os.chdir(temp_dir)
        print("🔄 Переход во временную директорию")
        
        # Создаем папку data, если её нет
        if not os.path.exists('data'):
            os.makedirs('data')
            print("📁 Создана папка data")

        print("🔨 Запуск PyInstaller...")
        # Параметры сборки
        PyInstaller.__main__.run([
            'main.py',
            '--name=ComunalKorm',
            '--onefile',
            '--windowed',
            '--icon=image/korm.ico',
            '--add-data=image;image',
            '--add-data=data;data',
            '--add-data=version.txt;.',
            '--add-data=update_info.json;.',
            '--hidden-import=pandas',
            '--hidden-import=numpy',
            '--hidden-import=sqlite3',
            '--hidden-import=docx',
            '--hidden-import=CTkMessagebox',
            '--hidden-import=customtkinter',
            '--clean',
            '--noconfirm'
        ])
        
        # Возвращаемся в исходную директорию
        os.chdir(current_dir)
        
        # Копируем результат в оригинальную папку dist
        temp_dist = os.path.join(temp_dir, 'dist')
        original_dist = os.path.join(current_dir, 'dist')
        
        if os.path.exists(original_dist):
            safe_remove_dir(original_dist)
        
        if os.path.exists(temp_dist):
            shutil.copytree(temp_dist, original_dist)
            print(f"✅ Результат сборки скопирован в {original_dist}")
        else:
            print(f"❌ Ошибка: папка {temp_dist} не найдена")
            return
        
        # Создаем папку для обновлений
        updates_dir = os.path.join(current_dir, 'updates')
        if not os.path.exists(updates_dir):
            os.makedirs(updates_dir)
        
        # Копируем exe-файл в папку обновлений
        exe_name = f"ComunalKorm_v{version}.exe"
        exe_source = os.path.join(original_dist, 'ComunalKorm.exe')
        exe_dest = os.path.join(updates_dir, exe_name)
        
        if os.path.exists(exe_source):
            shutil.copy2(exe_source, exe_dest)
            print(f"💾 Создана версия для обновления: {exe_name}")
        
        print("\n🎉 Сборка успешно завершена!")
        print(f"📦 Исполняемый файл: dist/ComunalKorm.exe")
        print(f"🔄 Версия для обновления: updates/{exe_name}")
        print(f"📋 Версия: {version}")
        
    except Exception as e:
        print(f"\n❌ Ошибка при сборке: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        # Удаляем временную директорию
        try:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                print(f"🗑️ Временная директория удалена: {temp_dir}")
        except Exception as e:
            print(f"⚠️ Не удалось удалить временную директорию: {e}")

if __name__ == '__main__':
    build_exe() 