# DeepSeek Conversation Parser English

A parser for exporting and formatting DeepSeek AI conversations from JSON into text files with clear question-answer markup.

## 📋 Description

This tool automatically converts a `conversations.json` file (conversations exported from DeepSeek) into a set of individual text files where each conversation:

- ✅ Is saved in a separate file named after the conversation title
- ✅ Is split into clear sections: **MY QUESTION** and **DEEPSEEK ANSWER**
- ✅ Is formatted for readability with separators for clarity
- ✅ Is protected from filename character errors

## 🚀 Quick Start

### Requirements
- Python 3.6+
- `conversations.json` file with exported conversations

### Installation

```bash
git clone https://github.com/MorevPro/deepseek-conversation-parser.git
cd deepseek-conversation-parser
```

### Usage

1. Place the `conversations.json` file in the script directory
2. Run the parser:

```bash
python parser.py
```

3. Results will be saved in the `parsed_conversations/` folder

### Configuration Example

Edit the variables at the end of `parser.py`:

```python
if __name__ == '__main__':
    input_file = r'path/to/conversations.json'
    output_dir = r'path/to/parsed_conversations'
    parse_conversations(input_file, output_dir)
```

## 📁 Output File Structure

Each file follows this structure:

```
================================================================================
Topic: Conversation Title
================================================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MY QUESTION:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
User's question text...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEEPSEEK ANSWER:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI answer text...
```

## 🔧 Features

### Core Functions
- **Automatic processing** – parses all conversations with a single command
- **Safe filenames** – removes/replaces invalid characters
- **Duplicate protection** – automatically numbers files with identical names
- **Error filtering** – skips server error messages
- **UTF-8 support** – handles Russian text correctly

### Filtering

The parser automatically:
- Skips empty messages
- Filters out server error messages (`"server is busy"`, `"try again later"`)
- Determines message type by the `fragment.type` field (`REQUEST` = question, `RESPONSE` = answer)

## 📊 Statistics

Example from processing 351 conversations:
- ✅ Processed: 351 files
- 📦 Total size: 16.3 MB
- 📄 Average file size: 22.7 KB

## 🏗️ Architecture

### Main Functions

#### `parse_conversations(json_file, output_dir)`
Main function for processing all conversations.

#### `extract_conversation(conv)`
Formats a single conversation into readable text.

#### `extract_messages(mapping)`
Extracts messages from the `mapping` structure in correct order.

#### `extract_message_content(message)`
Parses an individual message, determining the role (user/assistant) and content.

#### `sanitize_filename(filename)`
Converts a string into a safe filename.

## 📝 Input JSON Format

Expected structure:

```json
[
  {
    "id": "conversation-id",
    "title": "Conversation Title",
    "mapping": {
      "root": { "id": "root", "parent": null, "children": ["1"], "message": null },
      "1": {
        "id": "1",
        "parent": "root",
        "children": ["2"],
        "message": {
          "fragments": [
            {
              "type": "REQUEST",
              "content": "User's question text"
            }
          ],
          "model": "deepseek-reasoner"
        }
      }
    }
  }
]
```

## 🐛 Error Handling

The parser handles:
- Invalid characters in filenames
- Control characters (`\n`, `\r`, `\t`)
- Duplicate filenames
- Empty messages
- Missing fields in the JSON structure

## 📄 License

MIT License

## 👤 Author

**Morev** – [GitHub](https://github.com/MorevPro)

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## ⭐ If this helped – give it a star!



将 DeepSeek AI 的对话从 JSON 导出并格式化为带有清晰问答标记的文本文件。

## 📋 简介

该工具可自动将 `conversations.json` 文件（从 DeepSeek 导出的对话）转换为一组独立的文本文件，每个对话：

- ✅ 以对话标题命名并保存为单独文件
- ✅ 划分为清晰的部分：**我的问题** 和 **DEEPSEEK 回答**
- ✅ 使用分隔线格式化，易于阅读
- ✅ 自动处理文件名中的非法字符，避免出错

## 🚀 快速开始

### 环境要求
- Python 3.6 及以上版本
- 包含导出对话的 `conversations.json` 文件

### 安装

```bash
git clone https://github.com/MorevPro/deepseek-conversation-parser.git
cd deepseek-conversation-parser
```

### 使用方法

1. 将 `conversations.json` 文件放到脚本所在目录
2. 运行解析器：

```bash
python parser.py
```

3. 结果将保存在 `parsed_conversations/` 文件夹中

### 配置示例

编辑 `parser.py` 文件末尾的变量：

```python
if __name__ == '__main__':
    input_file = r'path/to/conversations.json'
    output_dir = r'path/to/parsed_conversations'
    parse_conversations(input_file, output_dir)
```

## 📁 输出文件结构

每个文件的结构如下：

```
================================================================================
主题：对话标题
================================================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
我的问题：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
用户提问内容...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEEPSEEK 回答：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AI 回答内容...
```

## 🔧 功能特点

### 核心功能
- **自动处理** – 一条命令解析所有对话
- **安全文件名** – 移除或替换非法字符
- **防重复** – 自动为同名文件添加序号
- **错误过滤** – 跳过服务器错误消息
- **UTF-8 支持** – 完美处理中文及俄文等文本

### 过滤机制

解析器会自动：
- 跳过空消息
- 过滤服务器错误消息（如 `"server is busy"`、`"try again later"`）
- 根据 `fragment.type` 字段判断消息类型（`REQUEST` = 问题，`RESPONSE` = 回答）

## 📊 统计示例

处理 351 个对话的示例数据：
- ✅ 已处理文件：351 个
- 📦 总大小：16.3 MB
- 📄 平均文件大小：22.7 KB

## 🏗️ 架构说明

### 主要函数

#### `parse_conversations(json_file, output_dir)`
处理所有对话的主函数。

#### `extract_conversation(conv)`
将单个对话格式化为可读文本。

#### `extract_messages(mapping)`
按正确顺序从 `mapping` 结构中提取消息。

#### `extract_message_content(message)`
解析单条消息，判断角色（用户/助手）及内容。

#### `sanitize_filename(filename)`
将字符串转换为安全的文件名。

## 📝 输入 JSON 格式

期望的结构如下：

```json
[
  {
    "id": "conversation-id",
    "title": "对话标题",
    "mapping": {
      "root": { "id": "root", "parent": null, "children": ["1"], "message": null },
      "1": {
        "id": "1",
        "parent": "root",
        "children": ["2"],
        "message": {
          "fragments": [
            {
              "type": "REQUEST",
              "content": "用户提问内容"
            }
          ],
          "model": "deepseek-reasoner"
        }
      }
    }
  }
]
```

## 🐛 错误处理

解析器可处理以下情况：
- 文件名中的非法字符
- 控制字符（`\n`、`\r`、`\t`）
- 重复的文件名
- 空消息
- JSON 结构中缺失的字段

## 📄 许可证

MIT License

## 👤 作者

**Morev** – [GitHub](https://github.com/MorevPro)

## 🤝 贡献

欢迎提交 Pull Request！如有重大更改，请先开启 Issue 讨论。

## ⭐ 如果对您有帮助，请给个 Star！




# DeepSeek Conversation Parser RU

Парсер для экспорта и форматирования бесед с DeepSeek AI из JSON в текстовые файлы с четкой разметкой вопросов и ответов.

## 📋 Описание

Этот инструмент автоматически преобразует файл `conversations.json` (экспортированные беседы из DeepSeek) в набор отдельных текстовых файлов, где каждая беседа:

- ✅ Сохраняется в отдельный файл с именем по заголовку беседы
- ✅ Разбивается на четкие секции: **МОЙ ВОПРОС** и **ОТВЕТ DEEPSEEK**
- ✅ Отформатирована читаемо с разделителями для наглядности
- ✅ Защищена от ошибок с символами в именах файлов

## 🚀 Быстрый старт

### Требования
- Python 3.6+
- Файл `conversations.json` с экспортированными беседами

### Установка

```bash
git clone https://github.com/MorevPro/deepseek-conversation-parser.git
cd deepseek-conversation-parser
```

### Использование

1. Поместите файл `conversations.json` в директорию со скриптом
2. Запустите парсер:

```bash
python parser.py
```

3. Результаты будут сохранены в папке `parsed_conversations/`

### Пример конфигурации

Отредактируйте переменные в конце `parser.py`:

```python
if __name__ == '__main__':
    input_file = r'путь/к/conversations.json'
    output_dir = r'путь/к/parsed_conversations'
    parse_conversations(input_file, output_dir)
```

## 📁 Структура выходных файлов

Каждый файл имеет следующую структуру:

```
================================================================================
Тема: Название беседы
================================================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
МОЙ ВОПРОС:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Текст вопроса пользователя...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ОТВЕТ DEEPSEEK:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Текст ответа AI...
```

## 🔧 Возможности

### Основные функции
- **Автоматическая обработка** - парсит все беседы в одну команду
- **Безопасные имена файлов** - удаляет/заменяет недопустимые символы
- **Защита от дублей** - автоматически нумерует файлы с одинаковыми именами
- **Фильтрация ошибок** - пропускает сообщения об ошибках сервера
- **UTF-8 поддержка** - корректно работает с русским текстом

### Фильтрация

Парсер автоматически:
- Пропускает пустые сообщения
- Отфильтровывает сообщения об ошибках сервера (`"server is busy"`, `"try again later"`)
- Определяет тип сообщения по полю `fragment.type` (`REQUEST` = вопрос, `RESPONSE` = ответ)

## 📊 Статистика

Пример обработки 351 беседы:
- ✅ Обработано: 351 файл
- 📦 Общий размер: 16.3 MB
- 📄 Средний размер файла: 22.7 KB

## 🏗️ Архитектура

### Основные функции

#### `parse_conversations(json_file, output_dir)`
Главная функция для обработки всех бесед.

#### `extract_conversation(conv)`
Форматирует одну беседу в читаемый текст.

#### `extract_messages(mapping)`
Извлекает сообщения из структуры `mapping` в правильном порядке.

#### `extract_message_content(message)`
Парсит отдельное сообщение, определяет роль (user/assistant) и содержимое.

#### `sanitize_filename(filename)`
Преобразует строку в безопасное имя файла.

## 📝 Формат входного JSON

Ожидается структура вида:

```json
[
  {
    "id": "conversation-id",
    "title": "Название беседы",
    "mapping": {
      "root": { "id": "root", "parent": null, "children": ["1"], "message": null },
      "1": {
        "id": "1",
        "parent": "root",
        "children": ["2"],
        "message": {
          "fragments": [
            {
              "type": "REQUEST",
              "content": "Текст вопроса пользователя"
            }
          ],
          "model": "deepseek-reasoner"
        }
      }
    }
  }
]
```

## 🐛 Обработка ошибок

Парсер обрабатывает:
- Недопустимые символы в именах файлов
- Управляющие символы (`\n`, `\r`, `\t`)
- Дублирующиеся имена файлов
- Пустые сообщения
- Отсутствующие поля в структуре JSON

## 📄 Лицензия

MIT License

## 👤 Автор

**Морев** - [GitHub](https://github.com/MorevPro)

## 🤝 Контрибьютинг

Приветствуются pull requests! Для больших изменений откройте issue.

## ⭐ Если помогло - поставьте звезду!

---

**Версия:** 1.0  
**Дата обновления:** 2026-04-05
