import tkinter as tk
import usb.core


def print_label():
    label_text = entry_text.get()
    font_size = int(entry_font_size.get())
    label_width = int(entry_width.get())
    label_height = int(entry_height.get())
    num_copies = int(entry_copies.get())

    # Initialize USB connection
    printer = usb.core.find(idVendor=YOUR_VENDOR_ID,
                            idProduct=YOUR_PRODUCT_ID)  # Replace with your printer's vendor and product IDs

    if printer is None:
        print("Printer not found.")
        return

    # Send print commands to the printer
    # Replace this part with the appropriate code for your printer's command set

    for _ in range(num_copies):
        # Send commands to the printer to set the label size, font size, and text
        # Example commands for ZPL II format:
        # Set label size
        printer.write(0x01, b'^XA^LL{0},{1}^XZ'.format(label_width, label_height))

        # Set font size
        printer.write(0x01, b'^XA^CI28^A@N,{0},0,0,1^XZ'.format(font_size))

        # Print label with the specified text
        printer.write(0x01, b'^XA^FO10,10^A@N,30,30^FD{0}^FS^XZ'.format(label_text))

    printer.close()


# Create the main window
window = tk.Tk()
window.title("Label Printer")
window.geometry("400x300")

# Create the input fields and labels
label_text = tk.Label(window, text="Label Text:")
label_text.pack()
entry_text = tk.Entry(window)
entry_text.pack()

label_font_size = tk.Label(window, text="Font Size:")
label_font_size.pack()
entry_font_size = tk.Entry(window)
entry_font_size.pack()

label_width = tk.Label(window, text="Label Width:")
label_width.pack()
entry_width = tk.Entry(window)
entry_width.pack()

label_height = tk.Label(window, text="Label Height:")
label_height.pack()
entry_height = tk.Entry(window)
entry_height.pack()

label_copies = tk.Label(window, text="Number of Copies:")
label_copies.pack()
entry_copies = tk.Entry(window)
entry_copies.pack()

# Create the print button
print_button = tk.Button(window, text="Print Label", command=print_label)
print_button.pack()

# Run the GUI event loop
window.mainloop()
