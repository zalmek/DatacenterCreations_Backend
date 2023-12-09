import redis

# создаем инстанс и указываем координаты БД на локальной машине
r = redis.Redis(
    host= '127.0.0.1',
    port= '6379')

# r.set('key', 'value1') # сохраняем ключ 'somekey' с значением '1000-7!'
value = r.get('key1') # получаем значение по ключу
print(value)
