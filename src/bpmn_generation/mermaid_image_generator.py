import os
import subprocess
import tempfile
import shutil

class MermaidImageGenerator:
    def __init__(self, mmdc_path=None):
        """
        Initialize the MermaidImageGenerator.
        Please make sure mermaid-cli (mmdc) is installed and available in the system PATH.
        ```npm install -g @mermaid-js/mermaid-cli```
        
        :param mmdc_path: Path to the mermaid-cli executable. If None, it will try to find mmdc in PATH.
        """
        self.mmdc_path = mmdc_path or self.find_mmdc()

    def find_mmdc(self):
        """Try to find the mmdc executable in the system PATH."""
        return shutil.which("mmdc") or shutil.which("mmdc.cmd")  # .cmd for Windows

    def generate_image(self, mermaid_code, output_path, image_format="png"):
        """
        Generate an image from Mermaid code.
        
        :param mermaid_code: The Mermaid notation as a string.
        :param output_path: The path where the output image should be saved.
        :param image_format: The desired image format (png, svg, pdf). Default is png.
        :return: True if successful, False otherwise.
        """
        if not self.mmdc_path:
            print("Error: mermaid-cli (mmdc) not found. Please install it or provide the correct path.")
            return False

        # Create a temporary file to store the Mermaid code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False) as temp_file:
            temp_file.write(mermaid_code)
            temp_file_path = temp_file.name

        try:
            # Run mermaid-cli to generate the image
            command = [
                self.mmdc_path,
                "-i", temp_file_path,
                "-o", output_path,
                "-f", image_format
            ]
            
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            
            # print(f"Image generated successfully: {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error code: {e.returncode}")    
            print(f"Error generating image: {e}")
            print(f"Command output: {e.output}")
            return False
        except FileNotFoundError:
            print(f"Error: Could not run the command. Make sure mermaid-cli is installed and the path is correct.")
            print(f"Current mmdc path: {self.mmdc_path}")
            return False
        finally:
            # Clean up the temporary file
            os.unlink(temp_file_path)