import random
import barcode
from barcode.writer import ImageWriter

def generate_barcode(name):
    """
    Generates a barcode image and saves it with the given name.

    Args:
        name (str): The base name for the barcode image file.

    Returns:
        tuple: The path to the saved barcode image file and the generated random number.
    """
    # Generate a random 12-digit number string
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
    
    # Choose the barcode type (EAN-13)
    barcode_type = barcode.get_barcode_class('ean13')
    
    # Create the barcode
    barcode_instance = barcode_type(random_number, writer=ImageWriter())
    
    # Save the barcode as an image file with the tag name
    barcode_filename = f'{name}_barcode'
    barcode_path = barcode_instance.save(barcode_filename)
    
    return barcode_path, random_number
