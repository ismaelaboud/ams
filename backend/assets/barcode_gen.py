import random
import barcode
from barcode.writer import ImageWriter

def generate_barcode(name):
    # Generate a random 12-digit number string
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    
    # Choose the barcode type
    barcode_type = barcode.get_barcode_class('ean13')
    
    # Create the barcode
    barcode_instance = barcode_type(random_number, writer=ImageWriter())
    
    # Save the barcode as an image file with the tag name
    barcode_filename = f'{name}_barcode'
    barcode_path = barcode_instance.save(barcode_filename)
    
    return barcode_path, random_number
