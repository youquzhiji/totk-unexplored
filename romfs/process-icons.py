import os
from PIL import Image
import svgwrite

def process_images(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Get a list of files in the input folder
    files = os.listdir(input_folder)

    for file in files:
        input_path = os.path.join(input_folder, file)
        output_path = os.path.join(output_folder, file)

        # Check if it's an SVG file
        if file.endswith(".svg"):
            process_svg(input_path, output_path)
        else:
            process_image(input_path, output_path)

def process_image(input_path, output_path):
    # Open the image
    image = Image.open(input_path)

    # Calculate the new size while maintaining the aspect ratio
    aspect_ratio = image.width / image.height
    target_width = 60
    target_height = int(target_width / aspect_ratio)

    # Resize the image
    resized_image = image.resize((target_width, target_height))

    # Save the resized image
    resized_image.save(output_path)
    print(f"Resized image saved as {output_path}")

def process_svg(input_path, output_path):
    # Load the SVG file
    drawing = svgwrite.Drawing(input_path)

    # Iterate through all elements in the SVG
    for element in drawing.elements:
        # Change black parts to rgb(234, 234, 29)
        if element.fill == "black":
            element.fill(rgb=(234, 234, 29))

    # Save the modified SVG as PNG
    drawing.saveas(output_path)
    print(f"Processed SVG saved as {output_path}")

# Example usage
input_folder = "unprocessed"
output_folder = "processed"
process_images(input_folder, output_folder)
