import argparse

from PIL import Image
import requests
from PIL import Image
# parser = argparse.ArgumentParser()
# # Size of each smaller photo
# photo_width = 564
# photo_height = 564
# parser.add_argument("layer", help="Layer to merge")
# args = parser.parse_args()
# layer = args.layer
# # Number of photos in x and y directions
# num_photos_x = 8
# num_photos_y = 8
# def save_image_from_url():
#     for x in range(num_photos_x):
#         for y in range(num_photos_y):
#          # Send a GET request to the URL
#             response = requests.get(f"https://www.zeldadungeon.net/maps/totk/tiles/{layer}/3/{x}_{y}.jpg")
#
#             # Check if the request was successful
#             if response.status_code == requests.codes.ok:
#                 # Open a file in binary mode and write the image content
#                 with open(f"romfs/{layer}/{x}_{y}.jpg", "wb") as file:
#                     file.write(response.content)
#
#             else:
#                 print(f"Failed to download the image. Error: {response.status_code}")
#
#
# def trim_image(image_path, output_path):
#     # Open the image
#     image = Image.open(image_path)
#
#     # Get the dimensions of the image
#     width, height = image.size
#
#     # Define the cropping boundaries
#     left = 0
#     top = 400
#     right = width - 0
#     bottom = height - 400
#
#     # Crop the image
#     trimmed_image = image.crop((left, top, right, bottom))
#
#     # Save the trimmed image
#     trimmed_image.save(output_path)
#     print(f"Trimmed image saved as {output_path}")
#
# # Example usage
# def shrink_image(image_path, output_path, new_width, new_height):
#     # Open the image
#     image = Image.open(image_path)
#
#     # Resize the image
#     resized_image = image.resize((new_width, new_height))
#
#     # Save the resized image
#     resized_image.save(output_path)
#     print(f"Resized image saved as {output_path}")
# def move_image(image_path, output_path):
#     # Open the image
#     image = Image.open(image_path)
#
#     # Get the dimensions of the image
#     width, height = image.size
#
#     # Define the cropping boundaries
#     left = 21
#     top = 0
#     right = width - 0
#     bottom = height - 0
#
#     # Crop the image
#     trimmed_image = image.crop((left, top, right, bottom))
#
#     # Save the trimmed image
#     trimmed_image.save(output_path)
#     print(f"Trimmed image saved as {output_path}")
# # Example usage



def crop_image(image_path, output_path, new_width, new_height):
    # Open the image
    image = Image.open(image_path)

    # Get the original dimensions
    original_width, original_height = image.size

    # Calculate the crop boundaries
    left = 5
    top = 11
    right = original_width - 6
    bottom = original_height - 12

    # Calculate the new center coordinates
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2

    # Calculate the new top-left coordinates for cropping
    new_left = center_x - (new_width // 2)
    new_top = center_y - (new_height // 2)

    # Calculate the new bottom-right coordinates for cropping
    new_right = new_left + new_width
    new_bottom = new_top + new_height

    # Crop the image
    cropped_image = image.crop((new_left, new_top, new_right, new_bottom))

    # Save the cropped image
    cropped_image.save(output_path)
    print(f"Cropped image saved as {output_path}")

# Example usage
# image_path = "input_image.jpg"
# output_path = "cropped_image.jpg"
# new_width = 100
# new_height = 120
# crop_image(image_path, output_path, new_width, new_height)

if __name__ == '__main__':

# Size of the large photo
#     large_photo_width = photo_width * num_photos_x
#     large_photo_height = photo_height * num_photos_y
#
#     # Create a new blank image for the large photo
#     large_photo = Image.new("RGB", (large_photo_width, large_photo_height))
#     #save_image_from_url()
#     # Iterate through the photos and paste them onto the large photo
#     for x in range(num_photos_x):
#         for y in range(num_photos_y):
#             # Generate the filename based on the x and y coordinates
#             filename = f"romfs/{layer}/{x}_{y}.jpg"  # Modify the file extension if necessary
#
#             # Open the smaller photo
#             photo = Image.open(filename)
#
#             # Calculate the coordinates to paste the smaller photo onto the large photo
#             paste_x = x * photo_width
#             paste_y = y * photo_height
#
#             # Paste the smaller photo onto the large photo
#             large_photo.paste(photo, (paste_x, paste_y))
#
#     # Save the large photo
#     large_photo.save(f"romfs/{layer}.png")
#     trim_image(f"romfs/{layer}.png", f"romfs/{layer}.png")
#     shrink_image(f"romfs/{layer}.png", f"romfs/{layer}.png",3011,2477)
#     move_image(f"romfs/{layer}.png", f"romfs/{layer}.png")

    image_path = "-1-min.png"
    output_path = "-1-min.png"
    new_width = 3000
    new_height = 2500
    crop_image(image_path, output_path, new_width, new_height)
    print("Large photo created successfully!")
