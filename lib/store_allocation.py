
import pickle
import base64

default_filename = 'allocations'
extension = '.ssalloc'

def encode_data(allocations:dict, filename=default_filename):
    # Append the extension if it is not present
    if not filename.endswith(extension):
        filename += extension

    # Pickle the allocations and encode them
    pickled_allocations = pickle.dumps(allocations)
    encoded_allocations = base64.b64encode(pickled_allocations)

    # Write the encoded allocations to the file
    if filename:
        with open(filename, 'wb') as f:
            f.write(encoded_allocations)

    print('Allocations saved to {}'.format(filename))
    return encoded_allocations

    
def decode_data(filename=default_filename):
    # Append the extension if it is not present
    if not filename.endswith(extension):
        filename += extension

    # Read the encoded allocations from the file
    with open(filename, 'rb') as f:
        encoded_allocations = f.read()

    # Decode the allocations
    pickled_allocations = base64.b64decode(encoded_allocations)
    allocations = pickle.loads(pickled_allocations)

    return allocations