from PIL import Image, ImageOps
import numpy as np
import cv2

def apply_transparency(image):
    # Load the image in RGBA format to handle transparency
    print(f"Image Type is : {type(image)}")
    
    # Ensure the image has an alpha channel
    if image.mode != 'RGBA':
        image = image.convert('RGBA')

    original = image.copy()  # Keep the original for final processing
    

    # Convert the image to a grayscale NumPy array
    gray_image = ImageOps.grayscale(image)
    gray_array = np.array(gray_image)

    # Normalize the background by setting near-white to white
    normalized_background = np.where(gray_array > 200, 255, gray_array)
    normalized_background_image = Image.fromarray(normalized_background.astype(np.uint8))
    

    # Convert the normalized background image to a numpy array before thresholding
    normalized_background_array = np.array(normalized_background_image)

    # Threshold the image to isolate the white areas
    _, binary_image = cv2.threshold(normalized_background_array, 240, 255, cv2.THRESH_BINARY)
    binary_image = cv2.bitwise_not(binary_image)  # Invert to make white areas black for flood fill
    binary_image = Image.fromarray(binary_image)
    
    # Convert RGB and Alpha to separate arrays for OpenCV processing
    rgb_image = np.array(normalized_background_image.convert('RGB'))
    alpha_channel = np.array(image)[:, :, 3]  # Extract the alpha channel directly from the original RGBA image

    h, w = rgb_image.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)

    # Define the seed point for flood fill, assuming it's set to a point known to be within the background
    seed_point = (0, 0)  # Adjust this as needed

    # Sample the color at the seed point from the RGB image
    seed_color = rgb_image[seed_point[1], seed_point[0]].tolist()

    # Set tolerance levels such that the fill will stop at or before hitting black
    # Black in BGR is (0, 0, 0), and we set a very low tolerance to stop at any near-black color
    # Lower numbers are more restrictive to fill, higher is more permissive
    lo_diff = (3, 3, 3)  # Lower bounds for color differences (can be adjusted)
    up_diff = (3, 3, 3)  # Upper bounds for color differences (can be adjusted)

    # Perform the flood fill operation
    cv2.floodFill(rgb_image, mask, seed_point, seed_color, lo_diff, up_diff, 8)
     # Convert back to RGB and then to Image for saving
    filled_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)
    filled_image = Image.fromarray(filled_image)

    # Save the filled image to disk
    
    # Optionally, save the mask to review which areas were filled
    mask_image = Image.fromarray(mask[1:-1, 1:-1] * 255)  # Scale mask to 0-255 for visibility
    


    # Dilate the mask to extend the transparency slightly
    kernel = np.ones((12,12), np.uint8)  # You can adjust the kernel size for more/less dilation
    dilated_mask = cv2.dilate(mask, kernel, iterations = 1)

    # Apply Gaussian blur to the dilated mask to smooth the edges
    blurred_mask = cv2.GaussianBlur(dilated_mask, (5, 5), 0)

    # Update alpha channel based on the blurred mask
    alpha_channel[blurred_mask[1:h+1, 1:w+1] == 1] = 0

    # Combine RGB and modified Alpha into the final image
    final_image = np.dstack((rgb_image, alpha_channel))

    # Apply original colors back only to non-transparent areas
    original_rgb = np.array(original.convert('RGB'))
    final_rgb = final_image[:, :, :3]  # Extract RGB channels
    final_rgb[blurred_mask[1:h+1, 1:w+1] != 1] = original_rgb[blurred_mask[1:h+1, 1:w+1] != 1]

    # Recombine with alpha channel
    final_image_with_original_colors = np.dstack((final_rgb, alpha_channel))
    final_image_with_original_colors = Image.fromarray(final_image_with_original_colors)

    return final_image_with_original_colors
  

