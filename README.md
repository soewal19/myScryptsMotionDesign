# AutoSub Reels for After Effects

Профессиональный набор инструментов для создания субтитров в стиле Reels/Shorts/TikTok.

## В состав входит:
1. **AutoSub_Reels.jsx** - Скрипт для After Effects (ScriptUI Panel).
2. **transcribe.py** - Python-скрипт для транскрибации видео с использованием OpenAI Whisper.
3. **Transcribe_Video.bat** - Быстрый запуск транскрибации через Drag-and-Drop.
4. **autosub.ico** - Профессиональная иконка для инструментов.
5. **ai_upscale.py** - Скрипт для ИИ-апскейлинга изображений до 4K.
6. **ai_outpaint.py** - Скрипт для ИИ-ресайзинга (outpainting) 9:16 -> 16:9.
7. **hook_swapper.jsx** - Автоматическая сборка вариаций видео с разными хуками (в папке task2).
8. **localization_pipeline.jsx** - Автоматизация локализации на основе CSV-таблиц (в папке task2).

## Видео-Автоматизация (Workflow & Task 2)
Для подробного описания процессов автоматизации и инструкций по развертыванию перейдите в папку `task2/`:
- [README.md](file:///e:/Teach/Scelar/Scelar2026/MyScripts/task2/README.md) - **Главная документация Task 2** (English).
- [C4_Architecture.md](file:///e:/Teach/Scelar/Scelar2026/MyScripts/task2/C4_Architecture.md) - Архитектурная документация (C4 Model).
- [C4_ComfyUI.md](file:///e:/Teach/Scelar/Scelar2026/MyScripts/task2/C4_ComfyUI.md) - Архитектурная документация для интеграции с ComfyUI.
- [C4_Advanced_AI.md](file:///e:/Teach/Scelar/Scelar2026/MyScripts/task2/C4_Advanced_AI.md) - Архитектура продвинутых ИИ-сервисов.
- [DEPLOYMENT_RU.md](file:///e:/Teach/Scelar/Scelar2026/MyScripts/task2/DEPLOYMENT_RU.md) - Инструкция по развертыванию (Русский).
- [DEPLOYMENT_EN.md](file:///e:/Teach/Scelar/Scelar2026/MyScripts/task2/DEPLOYMENT_EN.md) - Deployment Guide (English).

## AI Image Tools (Advanced)
Для работы с ИИ-инструментами (апскейлинг и ресайзинг) ознакомьтесь с отдельной документацией на английском языке:
- [README_AI.md](file:///e:/Teach/Scelar/Scelar2026/MyScripts/README_AI.md) - Инструкция по использованию ИИ-инструментов.
- [C4_Architecture.md](file:///e:/Teach/Scelar/Scelar2026/MyScripts/C4_Architecture.md) - Архитектурная документация (C4 Model).

## Как пользоваться:

### Шаг 0: Установка иконки (Опционально)
1. Установите Pillow: `pip install Pillow`
2. Запустите `python generate_icon.py`, чтобы создать файл `autosub.ico`.
3. Создайте **ярлык** для `Transcribe_Video.bat` (правой кнопкой -> Create shortcut).
4. Зайдите в Свойства ярлыка -> Change Icon -> выберите созданный `autosub.ico`.
5. Теперь вы можете закрепить ярлык на панели задач или рабочем столе.

### Шаг 1: Транскрибация (Drag-and-Drop)
1. Установите Whisper: `pip install openai-whisper`
2. Просто **перетащите ваше видео** на файл `Transcribe_Video.bat`.
3. Скрипт автоматически создаст `.srt` файл рядом с видео.

### Шаг 2: Создание субтитров в After Effects
1. Откройте After Effects.
2. Запустите `AutoSub_Reels.jsx` через `File > Scripts > Run Script File...` или положите его в папку `ScriptUI Panels`.
3. Настройте параметры:
   - **Font Size**: Размер шрифта (рекомендуется 120+).
   - **Split into individual words**: Создает отдельный слой для каждого слова (эффект Reels).
   - **Apply Pop Animation**: Добавляет анимацию "подпрыгивания" при появлении.
   - **Add Background Box**: Автоматически создает подложку под текст.
4. Нажмите **Import SRT & Generate** и выберите ваш `.srt` файл.

## Особенности (Senior Best Practices):
- **Word Splitting**: Умная разбивка длинных фраз из SRT на отдельные слова для динамичного монтажа.
- **Auto-Sizing BG**: Подложка (Shape Layer) автоматически подстраивается под длину слова с помощью выражений.
- **Expressions-based**: Все анимации сделаны на выражениях, что позволяет легко менять тайминги.
- **Uppercase**: Скрипт автоматически переводит текст в верхний регистр (стандарт Reels).
