import asyncio
import functools
import websockets
import sys
import json
import gzip
import os


# define the function to join the chunks of files into a single file
async def join_files(gz_name, dir_path, no_of_chunks):
    data_list = []
    filename = gz_name.split("-")[0]

    same_files = [i for i in os.listdir(dir_path) if i.startswith(filename)]

    if len(same_files) == no_of_chunks and f'{filename}.done' not in os.listdir(dir_path):
        for each in sorted(same_files):
            with gzip.open(dir_path + each, 'rb') as f:
                data_list.append(f.read())

        with open(dir_path + filename, 'wb') as f:
            for data in data_list:
                f.write(data)

        # create a done file for writing size
        size = os.path.getsize(dir_path + filename)
        with open(dir_path + f'{filename}.done', 'w') as f:
            f.write(str(size))
        return True

    else:
        return False


async def response(websocket, ws_path, dir_path):
    message = await websocket.recv()
    json_data = json.loads(message)
    filename = json_data.get("filename")
    no_of_chunks = json_data.get("no_of_chunks")
    file = json_data.get("file").encode('utf-8')
    with gzip.open(dir_path + filename, 'wb') as f:
        f.write(file)

    print(f"We got the file from the client: {filename}")

    # call the function to join the splitted files
    result = await join_files(filename, dir_path, no_of_chunks)
    if result:
        print(f"{filename} - file is ready!")
    await websocket.send("I can confirm I got your message!")


try:
    port = int(sys.argv[1])
except:
    print("please set the port")
    sys.exit()
try:
    path = sys.argv[2]
except:
    print("please set the path to dir")
    sys.exit()

bound_handler = functools.partial(response, dir_path=path)
start_server = websockets.serve(bound_handler, 'localhost', port)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
