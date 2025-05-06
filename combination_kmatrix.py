import numpy as np
import networkx as nx
import os
import logging
import pickle
from datetime import datetime
import concurrent.futures as mp
from grakel.kernels import WeisfeilerLehman, VertexHistogram
from itertools import combinations
import time
import argparse

from config import Config

# Configure logging
logging.basicConfig(level=getattr(logging, Config.LOG_LEVEL), 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_edge_dictionary(G):
    edge_dict = {}
    for node in G.nodes():
        edge_dict[node] = {}
        
        for neighbor in G.neighbors(node):
            edge_dict[node][neighbor] = 0
            
    return edge_dict

def create_node_labels(G):
    node_labels = {node: node for node in G.nodes()}
    return node_labels

def convert_to_grakel_format_with_edge_dict(G):
    edge_dict = create_edge_dictionary(G)
    node_labels = create_node_labels(G)
    return edge_dict, node_labels

def compute_isomorphism_subset(graph_subset):
    logger.info('Starting computation for a subset')
    kernel = WeisfeilerLehman(normalize=True, base_graph_kernel=VertexHistogram)
    kernel_matrix = kernel.fit_transform(graph_subset)
    logger.info('Finished computation for a subset')
    return kernel_matrix

def save_kernel_matrix(kernel_matrix, filename, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    full_path = os.path.join(output_dir, filename)
    with open(full_path, 'wb') as f:
        pickle.dump(kernel_matrix, f)
    logger.info(f'Saved kernel matrix to {full_path}')

def process_graph_parallel(graph_file):
    logger.info(f"Processing {graph_file}...")
    try:
        nx_graph = nx.read_graphml(graph_file)
        if nx_graph.number_of_nodes() == 0 or nx_graph.number_of_edges() == 0:
            return None
        graph = convert_to_grakel_format_with_edge_dict(nx_graph)
        return graph
    except Exception as e:
        logger.error(f"Error processing {graph_file}: {e}")
        return None

def graph_processor(all_graphs):
    start_time = datetime.now()
    logging.info(f"Starting at {start_time}")   

    logging.info(f"Found {len(all_graphs)} graphs")

    with mp.ProcessPoolExecutor() as executor:
        results = list(executor.map(process_graph_parallel, all_graphs))

    graphs = [graph for graph in results if graph is not None]
    end_time = datetime.now()   

    logging.info(f"Finished at {end_time}")
    logging.info(f"Total time taken: {end_time - start_time}")

    return graphs

def print_subset_sizes(file_list, n_subsets):
    file_subsets = np.array_split(file_list, n_subsets)

    # print size of each subset
    for i, subset in enumerate(file_subsets):
        print(f"Subset {i}: {len(subset)} files")


def load_subset(file_list, subset_index, n_subsets=10):
    file_subsets = np.array_split(file_list, n_subsets)
    graph_files = file_subsets[subset_index]
    all_graphs = graph_processor(graph_files)

    return all_graphs

def process_subset_pair(primary_subset, subset_index_i, subset_index_j, file_list, n_subsets, output_dir):
    secondary_subset = load_subset(file_list, subset_index_j, n_subsets=n_subsets)
    all_graphs = np.concatenate((primary_subset, secondary_subset))
    logger.info(f"Processing subset {subset_index_i} & {subset_index_j} with {len(all_graphs)} files")
    
    kernel_file = f'kernel_matrix_{subset_index_i}_{subset_index_j}.pkl'

    # Compute the kernel matrix
    kernel_matrix = compute_isomorphism_subset(all_graphs)
    save_kernel_matrix(kernel_matrix, kernel_file, output_dir)

def get_file_list():
    """Get a list of graph files from a directory with a specific pattern"""
    return Config.get_graph_files()


def run_all_pairs(args):
    """Run computation for all pairs of subsets"""
    file_list = get_file_list()
    logger.info(f"Found {len(file_list)} total graph files")
    
    times = []
    primary_subset = None
    primary_subset_idx = None
    
    for i, j in combinations(range(Config.NUM_SUBSETS), 2):
        output_file = os.path.join(Config.OUTPUT_DIR, f'kernel_matrix_{i}_{j}.pkl')
        if os.path.exists(output_file) and not args.force:
            logger.info(f"Skipping {i}_{j} as output already exists.")
            continue
            
        start_time = time.time()
        if primary_subset is None or primary_subset_idx != i:
            primary_subset = load_subset(file_list, i, Config.NUM_SUBSETS)
            primary_subset_idx = i
        
        process_subset_pair(primary_subset, i, j, file_list, Config.NUM_SUBSETS, Config.OUTPUT_DIR)
        
        end_time = time.time()
        elapsed = end_time - start_time
        times.append(elapsed)
        logger.info(f"Completed {i}_{j} in {elapsed:.2f} seconds")

    if times:
        logger.info(f"Total time taken: {sum(times):.2f} seconds")
        logger.info(f"Average time taken: {sum(times)/len(times):.2f} seconds")
    else:
        logger.info("No computations were performed.")

def main():
    parser = argparse.ArgumentParser(description="Graph Kernel Computation Tool")
    parser.add_argument("--force", action="store_true",
                       help="Force recomputation even if output exists")
    
    args = parser.parse_args()
    
    # Setup directories
    Config.setup_directories()
    
    # Get list of files
    file_list = Config.get_graph_files()
    logger.info(f"Found {len(file_list)} total graph files")
    
    print_subset_sizes(file_list, Config.NUM_SUBSETS)
    run_all_pairs(args)
        
if __name__ == '__main__':
    main()
