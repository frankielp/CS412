from PIL import Image
import os
from skimage.metrics import structural_similarity
from tqdm import tqdm
import cv2
import numpy as np
def img2gif():
    # Input folder containing image files
    input_folder = "output/mipnerf360_room/train/ours_30000/renders"

    # Output GIF file name
    output_gif = "output/mipnerf360_room/train/ours_30000/renders/output.gif"

    # Get a list of image files in the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith((".jpg", ".png", ".jpeg"))]

    # Sort the image files (optional)
    image_files.sort()

    # Create a list to store image frames
    frames = []

    # Load each image and append it to the frames list
    for image_file in tqdm(image_files):
        image_path = os.path.join(input_folder, image_file)
        image = Image.open(image_path)
        frames.append(image)

    # Save the frames as a GIF
    frames[0].save(output_gif, save_all=True, append_images=frames[1:], duration=500, loop=0)

    print(f"GIF saved as {output_gif}")



def concat_images(gt_path, predict_path, output_folder):
    filename=os.path.basename(gt_path)
    if os.path.exists(predict_path):
        # Read images
        gt = cv2.imread(gt_path)
        pred = cv2.imread(predict_path)

        # compute difference
        # Convert images to grayscale
        before_gray = cv2.cvtColor(gt, cv2.COLOR_BGR2GRAY)
        after_gray = cv2.cvtColor(pred, cv2.COLOR_BGR2GRAY)

        # Compute SSIM between the two images
        (score, diff) = structural_similarity(before_gray, after_gray, full=True)
        print("Image Similarity (SSIM): {:.4f}%".format(score * 100))

        diff = 255 - cv2.absdiff(gt, pred)

        # Concatenate images horizontally
        concat_image = np.concatenate((gt, pred, diff), axis=1)

        # Write the concatenated image to the output folder
        output_path = os.path.join(output_folder, f"{filename}")
        cv2.imwrite(output_path, concat_image)

def compute_difference(source_folder):
    gt_folder = os.path.join(source_folder, 'gt')
    predict_folder = os.path.join(source_folder, 'renders')
    output_folder = os.path.join(source_folder, 'difference')
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Iterate through the images in the 'gt' folder
    for filename in tqdm(sorted(os.listdir(gt_folder))):
        gt_path = os.path.join(gt_folder, filename)
        predict_path = os.path.join(predict_folder, filename)
        concat_images(gt_path, predict_path, output_folder)

if __name__ == "__main__":
    source_folder = "output/lego/test/ours_30000"
    compute_difference(source_folder)

