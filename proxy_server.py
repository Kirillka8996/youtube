import random
import asyncio

BLOCKED = set(line.rstrip().encode() for line in open('blacklist.txt', 'r', encoding='utf-8'))
TASKS = []

async def main(host, port):
    server = await asyncio.start_server(new_conn, host, port)
    await server.serve_forever()

async def pipe(reader, writer):
    try:
        while not reader.at_eof() and not writer.is_closing():
            data = await reader.read(8192)  # Увеличиваем размер буфера
            if not data:
                break
            writer.write(data)
            await writer.drain()
    finally:
        writer.close()

async def new_conn(local_reader, local_writer):
    http_data = await local_reader.read(8192)  # Увеличиваем размер буфера

    try:
        type, target = http_data.split(b"\r\n")[0].split(b" ")[0:2]
        host, port = target.split(b":")
    except:
        local_writer.close()
        return

    if type != b"CONNECT":
        local_writer.close()
        return

    local_writer.write(b'HTTP/1.1 200 OK\n\n')
    await local_writer.drain()

    try:
        remote_reader, remote_writer = await asyncio.open_connection(host, port)
    except:
        local_writer.close()
        return

    if port == b'443':
        await fragment_data(local_reader, remote_writer)

    TASKS.append(asyncio.create_task(pipe(local_reader, remote_writer)))
    TASKS.append(asyncio.create_task(pipe(remote_reader, local_writer)))

async def fragment_data(local_reader, remote_writer):
    head = await local_reader.read(5)
    data = await local_reader.read(8192)  # Увеличиваем размер буфера

    if all(site not in data for site in BLOCKED):  # Оптимизированная проверка
        remote_writer.write(head + data)
        await remote_writer.drain()
        return

    parts = []
    while data:
        part_len = random.randint(1, len(data))
        parts.append(bytes.fromhex("1603") + bytes([random.randint(0, 255)]) + int(
            part_len).to_bytes(2, byteorder='big') + data[:part_len])
        data = data[part_len:]

    remote_writer.write(b''.join(parts))
    await remote_writer.drain()

print("Прокси сервер запущен, приятного использования")

asyncio.run(main(host='127.0.0.1', port=8881))