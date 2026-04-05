#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple

def parse_conversations(json_file: str, output_dir: str) -> None:
    """
    Парсит conversations.json и сохраняет каждую беседу в отдельный txt файл.
    Каждая беседа разбита на вопросы пользователя и ответы DeepSeek.
    
    Args:
        json_file: путь к файлу conversations.json
        output_dir: директория для сохранения txt файлов
    """
    
    # Удаляем старую директорию если она есть
    if os.path.exists(output_dir):
        import shutil
        shutil.rmtree(output_dir)
    
    # Создаем директорию для выходных файлов
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Читаем JSON файл
    with open(json_file, 'r', encoding='utf-8') as f:
        conversations = json.load(f)
    
    print(f"Найдено {len(conversations)} бесед")
    
    success_count = 0
    error_count = 0
    
    # Обрабатываем каждую беседу
    for idx, conv in enumerate(conversations, 1):
        try:
            title = conv.get('title', f'untitled_{idx}').strip()
            conversation_text = extract_conversation(conv)
            
            # Генерируем безопасное имя файла
            filename = sanitize_filename(title)
            if not filename:
                filename = f'conversation_{idx}'
            
            filepath = os.path.join(output_dir, f'{filename}.txt')
            
            # Избегаем дублей имен файлов
            counter = 1
            base_filepath = filepath
            while os.path.exists(filepath):
                name, ext = os.path.splitext(base_filepath)
                filepath = f'{name}_{counter}{ext}'
                counter += 1
            
            # Сохраняем в файл
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(conversation_text)
            
            success_count += 1
            if idx % 50 == 0:
                print(f"[{idx}/{len(conversations)}] Обработано")
        except Exception as e:
            error_count += 1
            if error_count <= 5:  # Выводим первые 5 ошибок
                print(f"[{idx}/{len(conversations)}] ОШИБКА: {e}")
    
    print(f"\n✓ Всего обработано: {success_count}")
    if error_count > 0:
        print(f"⚠ Ошибок: {error_count}")


def extract_conversation(conv: Dict) -> str:
    """
    Извлекает беседу из объекта conversation и форматирует её.
    
    Args:
        conv: объект conversation из JSON
        
    Returns:
        отформатированный текст беседы
    """
    
    title = conv.get('title', 'Untitled').strip()
    mapping = conv.get('mapping', {})
    
    # Строим дерево сообщений
    messages = extract_messages(mapping)
    
    # Форматируем текст
    output = []
    output.append(f"{'='*80}")
    output.append(f"Тема: {title}")
    output.append(f"{'='*80}\n")
    
    for msg in messages:
        role = msg['role']
        content = msg['content']
        
        if role == 'user':
            output.append("━" * 80)
            output.append("МОЙ ВОПРОС:")
            output.append("━" * 80)
        else:
            output.append("━" * 80)
            output.append("ОТВЕТ DEEPSEEK:")
            output.append("━" * 80)
        
        output.append(content)
        output.append("")
    
    return "\n".join(output)


def extract_messages(mapping: Dict) -> List[Dict[str, str]]:
    """
    Извлекает сообщения из mapping структуры в порядке следования.
    
    Args:
        mapping: mapping объект из conversation
        
    Returns:
        список сообщений с role и content
    """
    
    messages = []
    
    # Начинаем с root и идем по цепочке children
    visited = set()
    to_process = ['root']
    
    while to_process:
        current_id = to_process.pop(0)
        
        if current_id in visited or current_id not in mapping:
            continue
        
        visited.add(current_id)
        node = mapping[current_id]
        
        # Если есть сообщение, добавляем его
        if node.get('message'):
            msg_data = extract_message_content(node['message'])
            if msg_data:
                messages.append(msg_data)
        
        # Добавляем детей в очередь
        children = node.get('children', [])
        to_process.extend(children)
    
    return messages


def extract_message_content(message: Dict) -> Dict[str, str] or None:
    """
    Извлекает содержимое из объекта message.
    
    Args:
        message: объект message из mapping
        
    Returns:
        словарь с role и content или None если сообщение пусто
    """
    
    # Извлекаем содержимое из fragments
    fragments = message.get('fragments', [])
    if not fragments:
        return None
    
    content_parts = []
    fragment_type = None
    
    for fragment in fragments:
        if isinstance(fragment, dict):
            # Определяем тип сообщения (REQUEST = пользователь, RESPONSE = AI)
            if fragment_type is None:
                fragment_type = fragment.get('type', '')
            
            content = fragment.get('content', '')
            if content:
                content_parts.append(content)
    
    if not content_parts:
        return None
    
    content = '\n'.join(content_parts)
    
    # Пропускаем сообщения об ошибках сервера
    if 'server is busy' in content.lower() or 'try again later' in content.lower():
        return None
    
    # Определяем role на основе типа фрагмента
    role = 'user' if fragment_type == 'REQUEST' else 'assistant'
    
    return {
        'role': role,
        'content': content.strip()
    }


def sanitize_filename(filename: str) -> str:
    """
    Преобразует строку в безопасное имя файла.
    
    Args:
        filename: исходное имя файла
        
    Returns:
        безопасное имя файла
    """
    
    # Заменяем символы новых строк и табуляции
    filename = filename.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
    
    # Удаляем недопустимые символы (включая все управляющие символы)
    invalid_chars = r'<>:"/\|?*' + ''.join(chr(i) for i in range(32))  # Все управляющие символы
    for char in invalid_chars:
        filename = filename.replace(char, '')
    
    # Заменяем пробелы на подчеркивание
    filename = filename.replace(' ', '_')
    
    # Убираем дублирующиеся подчеркивания
    while '__' in filename:
        filename = filename.replace('__', '_')
    
    # Ограничиваем длину
    filename = filename[:200]
    
    # Удаляем пустую строку
    filename = filename.strip('_')
    
    return filename


if __name__ == '__main__':
    # Путь к файлу conversations.json
    input_file = r'd:\projects\morev.pro\blog\Компенсация авиакомпания\deepseek_data-2026-04-06\conversations.json'
    
    # Директория для сохранения результатов
    output_dir = r'd:\projects\morev.pro\blog\Компенсация авиакомпания\deepseek_data-2026-04-06\parsed_conversations'
    
    # Запускаем парсер
    parse_conversations(input_file, output_dir)
    
    print(f"\n✓ Готово! Беседы сохранены в: {output_dir}")
