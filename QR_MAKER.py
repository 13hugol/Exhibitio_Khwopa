import os
import pandas as pd
import qrcode


def generate_qr_code(data, output_folder="qr_codes"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    for name in data:
        qr.clear()
        qr.add_data(name)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(f"{output_folder}/{name}.png")


if __name__ == "__main__":
    # Input file names
    input_file = "students.txt"

    # Read names from the file into a pandas DataFrame
    try:
        df = pd.read_csv(input_file, header=None, names=["Name"])
    except pd.errors.EmptyDataError:
        print("Error: The input file is empty.")
        exit()

    # Ensure the output folder exists
    output_folder = "qr_codes"
    os.makedirs(output_folder, exist_ok=True)

    # Extract names as a list
    names = df["Name"].tolist()

    # Generate QR codes for each name
    generate_qr_code(names, output_folder)

    print("QR codes generated successfully.")
