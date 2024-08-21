
import marshal

# Исходный код как строка
source_code = """
def greet(name):
    return f'Hello, {name}!'
"""
with open('src/modules/file.py', 'r') as f:
    source_code = f.read()
# Компилируем код
print('compilling')
compiled_code = compile(source_code, '<string>', 'exec')

# Записываем скомпилированный код в файл
with open('modules/file.rpycm', 'wb') as f: 
    marshal.dump(compiled_code, f)

print('done')  