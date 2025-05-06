from combination_kmatrix import *
from config import Config
import pickle
import numpy as np
import logging
import argparse
from itertools import combinations
import os

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL), 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_kernel_matrix(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
        
def merge_kernel_matrices():
    n_subsets = Config.NUM_SUBSETS
    # Initialize an empty kernel matrix
    complete_kernel_matrix = np.zeros((Config.get_total_graphs(), Config.get_total_graphs()))

    # List of all graph files
    file_subsets = np.array_split(Config.get_graph_files(), n_subsets)

    file_to_index = {}
    for i in range(n_subsets):
        for j, file in enumerate(file_subsets[i]):
            file_to_index[file] = (i, j)

    kernel_matrices = {}
    for i, j in combinations(range(n_subsets), 2):
        kernel_matrix = load_kernel_matrix(os.path.join(Config.OUTPUT_DIR, f'kernel_matrix_{i}_{j}.pkl'))
        kernel_matrices[(i, j)] = kernel_matrix

    logging.info('Loaded all kernel matrices')
    for i in range(Config.get_total_graphs()):
        for j in range(Config.get_total_graphs()):
            if i == j or i > j or complete_kernel_matrix[i, j] != 0:
                continue

            file_i = Config.get_graph_files()[i]
            file_j = Config.get_graph_files()[j]
            subset_i, index_i = file_to_index[file_i]
            subset_j, index_j = file_to_index[file_j]

            print(f'Processing {i} and {j} with subsets {subset_i} and {subset_j}')
            if subset_i == subset_j:
                if subset_i < n_subsets - 1:
                    kernel_matrix = kernel_matrices[(subset_i, subset_i + 1)]
                    complete_kernel_matrix[i, j] = kernel_matrix[index_i, index_j]
                else:
                    kernel_matrix = kernel_matrices[(0, subset_i)]
                    complete_kernel_matrix[i, j] = kernel_matrix[index_i, index_j]
            elif subset_i < subset_j:
                kernel_matrix = kernel_matrices[(subset_i, subset_j)]
                complete_kernel_matrix[i, j] = kernel_matrix[index_i, index_j]
            else:
                kernel_matrix = kernel_matrices[(subset_j, subset_i)]
                complete_kernel_matrix[i, j] = kernel_matrix[index_j, index_i]

            complete_kernel_matrix[j, i] = complete_kernel_matrix[i, j]

    np.fill_diagonal(complete_kernel_matrix, 1)
    return complete_kernel_matrix

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Graph Kernel merging Tool")
    parser.add_argument("--force", action="store_true",
                       help="Force recomputation even if output exists")
    
    args = parser.parse_args()
    
    # Setup directories
    Config.setup_directories()
    
    ckm = merge_kernel_matrices()
    output_file = os.path.join(Config.OUTPUT_DIR, "final_matrix.pkl")
    with open(output_file, 'wb') as f:
        pickle.dump(ckm, f)
    
    logger.info(f"The final kernel matrix has been saved at {output_file}")
