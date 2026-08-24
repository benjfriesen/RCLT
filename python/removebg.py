import os
import concurrent.futures
import cv2
import numpy as np
from rembg import remove, new_session
from PIL import Image

# working directories
base_dir = '/Users/bfrzn/Pictures/cropped & cleaned'
input_folder = os.path.join(base_dir, 'last')
output_folder = os.path.join(base_dir, 'lastout')

os.makedirs(output_folder, exist_ok=True)

# use e-commerce model
model_session = new_session("isnet-general-use")


def process_image(filename):
    if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        return None

    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_white_bg.jpg")

    if os.path.exists(output_path):
        return f"Skipped (already exists): {filename}"

    try:
        # isolate the main subject
        input_image = Image.open(input_path)
        extracted_image = remove(input_image, session=model_session, post_process_mask=True)

        # convert PIL image to OpenCV format to access the Alpha channel mask
        cv_img = np.array(extracted_image)
        alpha_channel = cv_img[:, :, 3]

        # define horizontal kernel
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (150, 5))

        # run MORPH_OPEN to remove artifacts narrower than 150 pixels
        clean_alpha = cv2.morphologyEx(alpha_channel, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)

        # apply the cleaned mask back to the image
        cv_img[:, :, 3] = clean_alpha

        extracted_image_clean = Image.fromarray(cv_img)

        # create a solid white background
        white_bg = Image.new("RGBA", extracted_image_clean.size, "WHITE")
        white_bg.paste(extracted_image_clean, (0, 0), extracted_image_clean)

        # convert to standard RGB
        final_image = white_bg.convert("RGB")
        final_image.save(output_path, "JPEG", quality=95)

        return f"Successfully processed: {filename}"

    except Exception as e:
        return f"Error processing {filename}: {e}"


if __name__ == '__main__':
    filenames = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]
    print(f"Found {len(filenames)} files. Starting processing...")

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(process_image, filenames)

    for result in results:
        if result:
            print(result)

    print("Processing complete.")