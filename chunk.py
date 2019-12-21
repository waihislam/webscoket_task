import os
import gzip


# define the function to split the file into smaller chunks
def split_file(input_file: str, chunk_size: int):
    # read the contents of the file
    with open(input_file, 'rb') as f:
        data = f.read()  # read the entire content of the file

    # get the length of data, ie size of the input file in bytes
    _bytes = len(data)

    # calculate the number of chunks to be created
    no_of_chunks = _bytes / chunk_size
    if _bytes % chunk_size:
        no_of_chunks += 1

    chunk_names = []
    counter = 0
    for i in range(0, _bytes + 1, chunk_size):
        fn1 = "abc-" + "{0:0=7d}".format(counter)
        chunk_names.append(fn1)
        with open(fn1, 'wb') as f:
            f.write(data[i:i + chunk_size])

        with open(fn1, 'rb') as f_in, gzip.open(fn1 + '.gz', 'wb') as f_out:
            f_out.writelines(f_in)
        counter += 1

    # create a done file for writing size
    size = os.path.getsize(input_file)
    with open('abc.done', 'w') as f:
        f.write(str(size))


# call the file splitting function
split_file('text.txt', 100)
