#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для создания обновлений программы ComunalKorm
"""

import os
import sys
import shutil
import json
import zipfile
from datetime import datetime
from pathlib import Path

def get_version():
    """Получает версию из файла version.txt"""
    try:
        with open('version.txt', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except:
        return "1.0.0"

def create_update_package():
    """Создает пакет обновления"""
    print("🚀 Создание пакета обновления...")
    
    version = get_version()
    print(f"📋 Версия: {version}")
    
    # Создаем папку для обновлений, если её нет
    updates_dir = "updates"
    os.makedirs(updates_dir, exist_ok=True)
    
    # Имя файла обновления
    update_filename = f"ComunalKorm_v{version}_update.zip"
    update_path = os.path.join(updates_dir, update_filename)
    
    try:
        # Создаем ZIP-архив с обновлением
        with zipfile.ZipFile(update_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            
            # Добавляем exe-файл
            exe_source = os.path.join("dist", "ComunalKorm.exe")
            if os.path.exists(exe_source):
                zipf.write(exe_source, "ComunalKorm.exe")
                print(f"📦 Добавлен exe-файл")
            else:
                print(f"❌ Файл {exe_source} не найден")
                return False
            
            # Добавляем файл версии
            version_file = "version.txt"
            if os.path.exists(version_file):
                zipf.write(version_file, "version.txt")
                print(f"📄 Добавлен файл версии")
            
            # Добавляем информацию об обновлении
            update_info_file = "update_info.json"
            if os.path.exists(update_info_file):
                zipf.write(update_info_file, "update_info.json")
                print(f"📋 Добавлена информация об обновлении")
            
            # Добавляем README с инструкциями
            readme_content = f"""# Обновление ComunalKorm v{version}

## Инструкция по установке

1. **Закройте приложение ComunalKorm** (если запущено)
2. **Создайте резервную копию** папки data (если есть важные данные)
3. **Распакуйте архив** в папку с программой
4. **Замените файл ComunalKorm.exe** на новый
5. **Запустите программу**

## Новые функции в версии {version}

- Генерация реестров по всем абонентам
- Улучшенный интерфейс с вкладками
- Система обновлений без потери данных
- Автоматическое резервное копирование

## Важно

- Все данные сохраняются в папке data
- При первом запуске новой версии создается резервная копия
- Если возникнут проблемы, восстановите данные из папки data/backup

## Поддержка

При возникновении проблем обратитесь к разработчику.
"""
            
            zipf.writestr("README_UPDATE.txt", readme_content)
            print(f"📖 Добавлена инструкция по обновлению")
        
        print(f"✅ Пакет обновления создан: {update_filename}")
        print(f"📁 Расположение: {update_path}")
        
        # Создаем файл с информацией о пакете
        package_info = {
            "version": version,
            "filename": update_filename,
            "size": os.path.getsize(update_path),
            "created": datetime.now().isoformat(),
            "files": [
                "ComunalKorm.exe",
                "version.txt",
                "update_info.json",
                "README_UPDATE.txt"
            ]
        }
        
        info_filename = f"package_info_v{version}.json"
        info_path = os.path.join(updates_dir, info_filename)
        
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(package_info, f, indent=2, ensure_ascii=False)
        
        print(f"📋 Информация о пакете сохранена: {info_filename}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании пакета обновления: {e}")
        return False

def create_installer_script():
    """Создает скрипт для автоматической установки обновления"""
    version = get_version()
    
    # Создаем bat-файл для Windows
    bat_content = f"""@echo off
echo ========================================
echo Обновление ComunalKorm v{version}
echo ========================================
echo.

echo Проверка наличия программы...
if not exist "ComunalKorm.exe" (
    echo ОШИБКА: Файл ComunalKorm.exe не найден!
    echo Убедитесь, что вы находитесь в папке с программой.
    pause
    exit /b 1
)

echo Создание резервной копии...
if not exist "data" mkdir data
if not exist "data\\backup" mkdir data\\backup

set timestamp=%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set timestamp=%timestamp: =0%

if exist "data\\abonent.db" (
    copy "data\\abonent.db" "data\\backup\\abonent_backup_%timestamp%.db" >nul
    echo Резервная копия создана: abonent_backup_%timestamp%.db
)

echo Установка обновления...
copy "ComunalKorm.exe" "ComunalKorm_old.exe" >nul
echo Старая версия сохранена как ComunalKorm_old.exe

echo.
echo ========================================
echo Обновление завершено успешно!
echo ========================================
echo.
echo Теперь вы можете запустить программу.
pause
"""
    
    bat_filename = f"update_installer_v{version}.bat"
    bat_path = os.path.join("updates", bat_filename)
    
    with open(bat_path, 'w', encoding='cp866') as f:
        f.write(bat_content)
    
    print(f"📜 Создан скрипт установки: {bat_filename}")
    return bat_path

def main():
    """Главная функция"""
    print("🔧 Создание пакета обновления ComunalKorm...")
    print("=" * 50)
    
    # Проверяем наличие собранного exe-файла
    exe_path = os.path.join("dist", "ComunalKorm.exe")
    if not os.path.exists(exe_path):
        print("❌ Ошибка: Файл ComunalKorm.exe не найден в папке dist")
        print("Сначала выполните сборку программы: python build.py")
        return
    
    # Создаем пакет обновления
    if create_update_package():
        # Создаем скрипт установки
        installer_path = create_installer_script()
        
        print("\n🎉 Пакет обновления создан успешно!")
        print("=" * 50)
        print("📦 Файлы для распространения:")
        print(f"   - updates/ComunalKorm_v{get_version()}_update.zip")
        print(f"   - updates/update_installer_v{get_version()}.bat")
        print("\n📋 Инструкция для пользователей:")
        print("1. Распакуйте ZIP-архив")
        print("2. Запустите bat-файл от имени администратора")
        print("3. Следуйте инструкциям на экране")
    else:
        print("❌ Ошибка при создании пакета обновления")

if __name__ == "__main__":
    main() 