import glob

FINAL_MATRIX_OP = "./final_kernel_matrix/"
GRAPHS_BP = "/Users/arjuns/Downloads/fyp/scraping/new/graphs"
LIST_OF_FILES = glob.glob(f'{GRAPHS_BP}/*/*.graphml')
TOTAL_GRAPHS = 204
FILES_WITH_NO_NODES = []
SIZES = [21,21,21,21,20,20,20,20,20,20]
