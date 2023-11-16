import os
import tkinter as tk
from tkinter import filedialog
import boto3
from botocore.exceptions import NoCredentialsError

def set_aws_credentials():
    os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_entry.get()
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_key_entry.get()

def select_file():
    file_path.set(filedialog.askopenfilename())

def upload_file():
    set_aws_credentials()
    s3 = boto3.client('s3')
    bucket_name = s3_bucket_entry.get()
    file_to_upload = file_path.get()

    try:
        s3.upload_file(file_to_upload, bucket_name, os.path.basename(file_to_upload))
        output_text.insert(tk.END, "Upload Successful\n")
    except NoCredentialsError:
        output_text.insert(tk.END, "Error: AWS credentials not valid\n")
    except Exception as e:
        output_text.insert(tk.END, f"Error: {str(e)}\n")

# Setup the GUI
root = tk.Tk()
root.title("S3 File Uploader")

tk.Label(root, text="AWS Access Key ID:").pack()
aws_access_key_entry = tk.Entry(root)
aws_access_key_entry.pack()

tk.Label(root, text="AWS Secret Access Key:").pack()
aws_secret_key_entry = tk.Entry(root)
aws_secret_key_entry.pack()

tk.Label(root, text="S3 Bucket Name (without 's3://' and '/'):").pack()
s3_bucket_entry = tk.Entry(root)
s3_bucket_entry.pack()

tk.Button(root, text="Select File", command=select_file).pack()
file_path = tk.StringVar()
tk.Entry(root, textvariable=file_path).pack()

tk.Button(root, text="Upload to S3", command=upload_file).pack()

output_text = tk.Text(root, height=10)
output_text.pack()

root.mainloop()