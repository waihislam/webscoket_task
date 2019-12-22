import asyncio
import websockets
import re
import os
import sys
import json
import gzip


async def check_dir(path):
    files_dict = {}
    pattern = re.compile(r"[a-z]+-\d{7}\.gz")
    for filepath in os.listdir(path):
        filename = filepath.split("-")[0]
        if pattern.match(filepath) and f'{filename}.done' in os.listdir(path):
            if files_dict.get(filename):
                files_dict[filename].append(filepath)
            else:
                print(f"Got new file {filename}")
                files_dict[filename] = [filepath]
    return files_dict


async def message(host, port, path):
    files_dict = await check_dir(path)
    if files_dict:
        for filename, files, in files_dict.items():
            print(f'sending {filename}..')
            for each in files:
                async with websockets.connect(f"ws://{host}:{port}") as socket:
                    with gzip.open(path + each, 'rb') as f:
                        data = f.read()
                    json_data = json.dumps({"file": data.decode("utf-8"), "filename": each,
                                            "no_of_chunks": len(files)})
                    await socket.send(json_data)
                    print(await socket.recv())

try:
    host = sys.argv[1]
except:
    print("please set the host")
    sys.exit()
try:
    port = sys.argv[2]
except:
    print("please set the port")
    sys.exit()
try:
    path = sys.argv[3]
except:
    print("please set the path to dir")
    sys.exit()
asyncio.get_event_loop().run_until_complete(message(host, port, path))
