import h5py

def check_h5_file(file_path):
    try:
        with h5py.File(file_path, 'r') as file:
            print(list(file.keys()))  # This should print the keys in the root of the HDF5 file
            return "File is readable"
    except Exception as e:
        return str(e)

# Check your model file
print(check_h5_file('eco-track.h5'))

def inspect_h5_file(file_path):
    try:
        with h5py.File(file_path, 'r') as file:
            print("Keys in the file:", list(file.keys()))
            print("Model config:", file.attrs.get('model_config'))
            print("Training config:", file.attrs.get('training_config'))
    except Exception as e:
        print("Failed to read file:", e)

inspect_h5_file('eco-track.h5')
