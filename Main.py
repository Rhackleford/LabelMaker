import tkinter as tk
from tkinter import filedialog, messagebox
import reportlab

from reportlab.graphics.barcode import code39
from reportlab.graphics.barcode import code128
from reportlab.graphics.barcode import code93
from reportlab.graphics.barcode import usps, usps4s, ecc200datamatrix
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
import subprocess

# Function to retrieve the last entered width and height values
def get_last_dimensions():
    try:
        with open("dimensions.txt", "r") as file:
            width, height = file.read().split(",")
            return float(width), float(height)
    except FileNotFoundError:
        return None, None

# Function to save the current width and height values
def save_dimensions(width, height):
    with open("dimensions.txt", "w") as file:
        file.write(f"{width},{height}")

def create_barcode_pdf(barcode_value, page_width, page_height, pdf_file):
    """
    Create a PDF with a barcode and human-readable text centered horizontally and vertically on a specified page size
    """
    # Define the dimensions of the barcode and the human-readable text
    barcode_height = 1 * inch
    text_height = 0.2 * inch
    margin = 5 * mm

    # Calculate the maximum barcode width based on the available space
    max_barcode_width = page_width - 2 * margin
    barcode_width = min(max_barcode_width, len(barcode_value) * 0.2 * inch)

    # Calculate the coordinates to center the barcode and text horizontally on the page
    x = (page_width - barcode_width) / 2
    y = (page_height - barcode_height) / 2 + text_height

    # Create a canvas and set the page size
    c = canvas.Canvas(pdf_file, pagesize=(page_width, page_height))

    # Create the barcode and draw it on the canvas
    barcode = code39.Extended39(barcode_value)
    barcode_x_adjusted = x + (barcode_width - barcode.width) / 2
    barcode.drawOn(c, barcode_x_adjusted, y + text_height)

    # Draw the human-readable text under the barcode
    c.setFont("Helvetica", 15)
    text_x_adjusted = x + barcode_width / 2
    c.drawCentredString(text_x_adjusted, y, barcode_value)

    # Save the canvas as a PDF file
    c.save()

def print_pdf(pdf_file):
    # Print the PDF silently using Ghostscript
    if pdf_file:
        gs_command = [
            "gsWIN64",
            "-q",
            "-dNOPAUSE",
            "-dBATCH",
            "-dPrinted",
            "-sDEVICE=mswinpr2",
            "-sOutputFile=%printer%",
            "-dSAFER",  # Add the -dSAFER option
            pdf_file
        ]
        subprocess.Popen(gs_command, shell=True)

def validate_dimensions(width, height):
    if width < 3 * inch:
        messagebox.showwarning("Warning", "The label width is less than 3 inches. Long inventory IDs may be cut off.")

def generate_barcodes():
    barcode_value = barcode_entry.get()
    page_width = float(width_entry.get()) * inch
    page_height = float(height_entry.get()) * inch

    # Validate the dimensions
    validate_dimensions(page_width, page_height)

    # Create a temporary PDF file
    pdf_file = "barcode.pdf"
    create_barcode_pdf(barcode_value, page_width, page_height, pdf_file)

    # Print the PDF silently
    print_pdf(pdf_file)

    # Save the current width and height values
    save_dimensions(float(width_entry.get()), float(height_entry.get()))

# Create the main window
window = tk.Tk()
window.title("Barcode Generator")

# Retrieve the last entered width and height values
last_width, last_height = get_last_dimensions()

# Barcode value label and entry
barcode_label = tk.Label(window, text="Barcode Value:")
barcode_label.pack()
barcode_entry = tk.Entry(window)
barcode_entry.pack()

# Page width label and entry
width_label = tk.Label(window, text="Page Width (inches):")
width_label.pack()
width_entry = tk.Entry(window)
width_entry.pack()

# Set the last entered width value if available
if last_width:
    width_entry.insert(0, str(last_width))

# Page height label and entry
height_label = tk.Label(window, text="Page Height (inches):")
height_label.pack()
height_entry = tk.Entry(window)
height_entry.pack()

# Set the last entered height value if available
if last_height:
    height_entry.insert(0, str(last_height))

# Generate button
generate_button = tk.Button(window, text="Generate & Print", command=generate_barcodes)
generate_button.pack()

# Start the GUI event loop
window.mainloop()
