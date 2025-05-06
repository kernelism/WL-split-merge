import os
from pathlib import Path

class Config:
    # Base paths
    BASE_DIR = Path(__file__).parent.absolute()
    
    # Input/Output paths
    GRAPHS_DIR = os.path.join(BASE_DIR, "graphs")  # Directory containing graph files
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")  # Directory for output files
    
    # Processing settings
    NUM_SUBSETS = 10  # Number of subsets to split the data into
    GRAPH_PATTERN = "*.graphml"  # Pattern to match graph files
    
    # Logging settings
    LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories if they don't exist"""
        os.makedirs(cls.GRAPHS_DIR, exist_ok=True)
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
    
    @classmethod
    def get_graph_files(cls):
        """Get list of graph files using the configured pattern"""
        return list(Path(cls.GRAPHS_DIR).rglob(cls.GRAPH_PATTERN))
    
    @classmethod
    def get_total_graphs(cls):
        """Get total number of graphs"""
        return len(cls.get_graph_files()) 