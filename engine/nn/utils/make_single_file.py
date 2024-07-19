import h5py
import numpy as np

input_files = ['../data/chess_data1.h5', '../data/chess_data2.h5', '../data/chess_data3.h5']

output_file = '../data/merged_chess_dataset.h5'

with h5py.File(output_file, 'w') as out_h5:
    for input_file in input_files:
        with h5py.File(input_file, 'r') as in_h5:
            if 'features' not in out_h5:
                in_h5.copy('features', out_h5)
            else:
                in_features = in_h5['features'][:]
                out_features = out_h5['features']
                combined_features = np.concatenate((out_features, in_features), axis=0)
                del out_h5['features']
                out_h5.create_dataset('features', data=combined_features)

            if 'labels' not in out_h5:
                in_h5.copy('labels', out_h5)
            else:
                in_labels = in_h5['labels'][:]
                out_labels = out_h5['labels']
                combined_labels = np.concatenate((out_labels, in_labels), axis=0)
                del out_h5['labels']
                out_h5.create_dataset('labels', data=combined_labels)

print(f'Merged HDF5 file saved as {output_file}')
