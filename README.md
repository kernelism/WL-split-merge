# Weisfeiler-Lehman Kernel Computation and Kernel Matrix Merging

This repository contains two Python scripts, `generate_final_kmatrix.py` and `combination_kmatrix.py`, designed to compute and merge Weisfeiler-Lehman (WL) graph kernel matrices for thousands of graphs. These scripts handle memory constraints by processing the data in manageable batches and then recombining the results into a final kernel matrix.

## Overview

The Weisfeiler-Lehman kernel is a widely used graph kernel that computes similarities between graphs based on their structure. Due to the large number of graphs and a large size for each graphs, directly computing the kernel matrix for all graphs was infeasible due to memory limitations. To address this, the computation was split into smaller subsets, and the results were merged into a complete kernel matrix.

This script was tested on a dataset of over 4k graphs consisting of 11 million nodes.

## How to use

- Update `constants.py` with relevant info.
- Run `combination_kmatrix.py`, with required args and it will generate combination comparisons of wl kernel in the said directory. A sample can be found in testset dir.
- Run `generate_finalk_matrix.py` to merge all the combination matrices to arrive at the final matrix which would be number of graphs x number of graphs size.

## Args
You can choose the number of subsets to use. Too large and there are too many combinations to process. Too few and each combination consists of too many graphs. 

