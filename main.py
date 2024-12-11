import os
import functions_framework
from google.cloud import storage
from pdf2image import convert_from_path


storage_client = storage.Client()


@functions_framework.cloud_event
def main(cloud_event):
    data = cloud_event.data

    bucket_name = data["bucket"]
    file_name = data["name"]  # PDF filename

    # Only process PDFs in the "input_files" folder
    if not file_name.endswith(".pdf") or not file_name.startswith("input_files/"):
        print(f"Skipping non-PDF file: {file_name}")
        return

    # The PDF file is named as <run_id>.pdf in the input files directory
    run_id = os.path.splitext(os.path.basename(file_name))[0]

    # Temporary path for downloading the file
    temp_download_path = f"/tmp/{run_id}.pdf"

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Download the PDF file to the temporary location
    blob.download_to_filename(temp_download_path)
    print(f"Downloaded {file_name} to {temp_download_path}")

    # Convert PDF to images using Poppler
    images = convert_from_path(temp_download_path)

    # Save each page as a JPEG image to GCS
    for i, image in enumerate(images):
        page_number = i + 1
        output_filename = f"pdf_to_images/{run_id}/page{page_number:03d}.jpeg"
        temp_image_path = f"/tmp/page{page_number:03d}-{run_id}.jpeg"

        # Save the image temporarily
        image.save(temp_image_path, format="JPEG")

        # Upload the image to the GCS bucket
        output_blob = bucket.blob(output_filename)
        output_blob.upload_from_filename(temp_image_path)

        print(f"Uploaded {output_filename} to bucket {bucket_name}")

    # Clean up the temporary files
    os.remove(temp_download_path)
    for i in range(len(images)):
        temp_image_path = f"/tmp/page{i+1:03d}-{run_id}.jpeg"
        os.remove(temp_image_path)

    print(f"Processed PDF {file_name} and saved images to {bucket_name}/pdf_to_images/{run_id}")
