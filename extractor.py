import fitz
from datetime import datetime
import os
from PIL import Image
import io

class Utils:
    def get_date_time(self):
        return datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    
    # Checks for end command (standard for command line apps)
    def check_for_end_command(self, prompt):
        if prompt.lower().replace(" ", "") == "end":
            print("Ended Session.")
            return False
        return True

class Processor:
    # 
    def check_folder_path(self,folder_path):
        if not os.path.exists(folder_path):
            print(f"Folder @ {folder_path} does not exist. Attempting to create it...")
            os.makedirs(folder_path)

    def image_extraction(self, folder_name, filename, file_obj):
        try:
            self.check_folder_path(folder_name)

            for page_index, page in enumerate(file_obj):
                image_list = page.get_images(full=True)
                if image_list:
                    print(f"Found {len(image_list)} images on page {page_index + 1}.")
                else:
                    print(f"No images found on page {page_index + 1}.")
                
                for image_index, img in enumerate(image_list, start=1):
                    xref = img[0]
                    base_image = file_obj.extract_image(xref)
                    image_bytes = base_image["image"]
                    image = Image.open(io.BytesIO(image_bytes))

                    image_path = os.path.join(folder_name, f"Image{image_index}-pg{page_index+1}-pdfFile{os.path.basename(filename)}.png")
                    image.save(image_path)
                    print(f"Saved: {image_path}")

        except Exception as e:
            print(f"Error occurred during image extraction: {e}")

class App(Utils, Processor):
    def run(self):
        print(f"Session begun at {self.get_date_time()}.")

        while True:
            prompt = input("Please input the path to the PDF file: ").strip()

            if not self.check_for_end_command(prompt):
                break
            
            prompt = prompt.strip('"')  # Remove surrounding quotes if pasted with them

            if not os.path.exists(prompt):
                print("Error: File not found. Please enter a valid file path.")
                continue

            try:
                file_obj = fitz.open(prompt)
            except (FileNotFoundError, PermissionError) as e:
                print(f"Error: {e}")
                continue
            except Exception as e:
                print(f"Unexpected Error Occurred: {e}. Retrying.")
                continue

            folder_save_location = input("Please input the folder to store the images in: ").strip().strip('"')
            self.image_extraction(folder_save_location, prompt, file_obj)

if __name__ == "__main__":
    app = App()
    app.run()