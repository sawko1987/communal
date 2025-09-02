import PyInstaller.__main__
import os
import shutil

def build_simple():
    print("🚀 Простая сборка ComunalKorm...")
    
    # Создаем папку dist, если её нет
    if not os.path.exists('dist'):
        os.makedirs('dist')
    
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
    
    print("✅ Сборка завершена!")
    print("📦 Исполняемый файл: dist/ComunalKorm.exe")

if __name__ == '__main__':
    build_simple() 