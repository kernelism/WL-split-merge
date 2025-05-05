from combination_kmatrix import *
from constants import TOTAL_GRAPHS, LIST_OF_FILES, SIZES, FINAL_MATRIX_OP

def load_kernel_matrix(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
        
def merge_kernel_matrices(args):
    n_subsets = args.n_subsets
    KERNEL_MATRICES_BP = args.matrices_dir
    # Initialize an empty kernel matrix
    complete_kernel_matrix = np.zeros((TOTAL_GRAPHS, TOTAL_GRAPHS))

    # List of all graph files
    file_subsets = np.array_split(LIST_OF_FILES, n_subsets)

    file_to_index = {}
    for i in range(n_subsets):
        for j, file in enumerate(file_subsets[i]):
            file_to_index[file] = (i, j)

        
    kernel_matrices = {}
    for i, j in combinations(range(n_subsets), 2):
        kernel_matrix = load_kernel_matrix(f'{KERNEL_MATRICES_BP}/kernel_matrix_{i}_{j}.pkl')
        kernel_matrices[(i, j)] = kernel_matrix

    logging.info('Loaded all kernel matrices')
    for i in range(len(LIST_OF_FILES)):
        for j in range(len(LIST_OF_FILES)):
            if i == j or i > j or complete_kernel_matrix[i, j] != 0:
                continue

            file_i = LIST_OF_FILES[i]
            file_j = LIST_OF_FILES[j]
            subset_i, index_i = file_to_index[file_i]
            subset_j, index_j = file_to_index[file_j]

            print(f'Processing {i} and {j} with subsets {subset_i} and {subset_j}')
            if subset_i == subset_j:
                if subset_i < n_subsets - 1:
                    kernel_matrix = kernel_matrices[(subset_i, subset_i + 1)]
                    complete_kernel_matrix[i, j] = kernel_matrix[index_i, index_j]
                else:
                    kernel_matrix = kernel_matrices[(0, subset_i)]
                    complete_kernel_matrix[i, j] = kernel_matrix[(SIZES[0]) + index_i, (SIZES[0]) + index_j]
            elif subset_i < subset_j:
                kernel_matrix = kernel_matrices[(subset_i, subset_j)]
                complete_kernel_matrix[i, j] = kernel_matrix[index_i, (SIZES[subset_i]) + index_j]
            else:
                kernel_matrix = kernel_matrices[(subset_j, subset_i)]
                complete_kernel_matrix[i, j] = kernel_matrix[(SIZES[subset_j]) + index_i, index_j]

            complete_kernel_matrix[j, i] = complete_kernel_matrix[i, j]

    np.fill_diagonal(complete_kernel_matrix, 1)
    return complete_kernel_matrix

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Graph Kernel merging Tool")
    parser.add_argument("--n-subsets", type=int, default=10,
                help="Number of subsets to split the data into")
    parser.add_argument("--matrices-dir", type=str,
                    help="directory where kernel matrices are saved")

    
    args = parser.parse_args()
    ckm = merge_kernel_matrices(args)
    with open(FINAL_MATRIX_OP + "final_matrix.pkl", 'wb') as f:
        pickle.dump(ckm, f)
    
    logger.info(f"The final kernel matrix has been saved at {FINAL_MATRIX_OP}/final_matrix.pkl")
