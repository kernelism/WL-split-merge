import unittest
import pickle
import numpy as np

class TestCompleteKernelMatrix(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Load the complete kernel matrix once for all tests
        with open('final_kernel_matrix/final_matrix.pkl', 'rb') as f:
            cls.complete_kernel_matrix = pickle.load(f)
    
    def test_shape(self):
        self.assertEqual(self.complete_kernel_matrix.shape, (204, 204), "Matrix shape is not (4032, 4032)")
    
    def test_diagonal(self):
        self.assertTrue(np.all(self.complete_kernel_matrix.diagonal() == 1.0), "Diagonal elements are not all 1")
        
    def test_symmetric(self):
        self.assertTrue(np.allclose(self.complete_kernel_matrix, self.complete_kernel_matrix.T, atol=1e-8), "Matrix is not symmetric")

    def test_similar_to_direct_generated(self):
        matrix_npy = np.load('./final_kernel_matrix/similarity_matrix.npy')
        with open('./final_kernel_matrix/final_matrix.pkl', 'rb') as f:
            matrix_pkl = pickle.load(f)
        
        self.assertTrue(np.array_equal(matrix_npy, matrix_pkl), "Matrices are not equal!")


if __name__ == '__main__':
    unittest.main()
