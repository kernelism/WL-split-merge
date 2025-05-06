# Graph Kernel Matrix Computation Tool

A simple tool for computing and merging Weisfeiler-Lehman (WL) graph kernel matrices for large-scale graph datasets. This tool efficiently handles memory constraints by processing graphs in manageable batches and then combining the results into a final kernel matrix.

## 📋 Prerequisites

- Python 3.7+
- Required Python packages:
  - numpy
  - networkx
  - grakel
  - pathlib

## 🛠️ Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

### 1. Prepare Your Data

Place your graph files (in GraphML format) in the `graphs/` directory. The tool will automatically find all `.graphml` files in this directory.

### 2. Configure Settings

Edit `config.py` to adjust settings:
- `GRAPHS_DIR`: Directory containing your graph files
- `OUTPUT_DIR`: Where to save output files
- `NUM_SUBSETS`: Number of subsets to split the data into (default: 10)
- `LOG_LEVEL`: Logging level (default: "INFO")

### 3. Run the Computation

1. First, compute the kernel matrices for subsets:
```bash
python combination_kmatrix.py
```

2. Then, merge the results into a final matrix:
```bash
python generate_final_kmatrix.py
```

The final kernel matrix will be saved in the `output/` directory.

## ⚙️ Configuration Options

You can customize the processing by modifying `config.py`:

- **NUM_SUBSETS**: Controls how many subsets the data is split into
  - Too many subsets: More combinations to process
  - Too few subsets: Each combination contains more graphs
  - Recommended: Start with 10 and adjust based on your system's memory

- **GRAPH_PATTERN**: Pattern to match graph files (default: "*.graphml")

## 📊 Performance

This tool has been tested on:
- Dataset size: 4,000+ graphs
- Total nodes: 11 million+
- Memory usage: Optimized for large-scale processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT

## 🙏 Acknowledgments

- Based on the Weisfeiler-Lehman graph kernel algorithm
- Uses the grakel library for kernel computations

