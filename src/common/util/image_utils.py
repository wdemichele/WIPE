import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

class ImageUtils:
    @staticmethod
    def plot_image_from_path(file_path, title=None, figsize=(10, 10)):
        """
        Plot an image from a given file path.
        
        Args:
        file_path (str): Path to the image file.
        title (str, optional): Title for the plot. Defaults to None.
        figsize (tuple, optional): Figure size (width, height) in inches. Defaults to (10, 10).
        
        Returns:
        None
        """
        try:
            img = Image.open(file_path)
            
            img_array = np.array(img)
            
            plt.figure(figsize=figsize)
            
            if len(img_array.shape) == 2 or (len(img_array.shape) == 3 and img_array.shape[2] == 1):
                plt.imshow(img_array, cmap='gray')
            else:
                plt.imshow(img_array)
            
            plt.axis('off')
            
            if title:
                plt.title(title)
            
            plt.show()
            
        except Exception as e:
            print(f"Error plotting image: {str(e)}")