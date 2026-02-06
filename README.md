# IEEE DataPort Streamlit Downloader

GitHub repository: [https://github.com/damilp36/downloader_IEEE_dataport](https://github.com/damilp36/downloader_IEEE_dataport)

This repository provides a Streamlit based web application for downloading datasets from IEEE DataPort using official AWS S3 credentials. IEEE DataPort hosts datasets in a private Amazon S3 bucket, and access is granted through personal AWS Access Keys associated with a DataPort account.

This tool simplifies downloading one or multiple dataset files by pasting their S3 URIs into a web interface instead of using the command line.

---

## Features

* Streamlit based graphical user interface
* Supports single or multiple IEEE DataPort S3 URIs
* Secure input for AWS Access Key ID and Secret Access Key
* Credential validation using AWS STS
* Automatic decoding of URL encoded S3 paths
* Download progress indicator
* Compatible with all IEEE DataPort datasets you are authorized to access

---

## Requirements

* Python 3.9 or newer
* An active IEEE DataPort account

### Python dependencies

* streamlit
* boto3
* botocore

---

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/damilp36/downloader_IEEE_dataport.git
cd IEEE
pip install streamlit boto3
```

---

## Running the Application

Start the Streamlit application with:

```bash
streamlit run app4dataport.py
```

The application will open in your browser automatically.

---

## How to Use

### Step 1 Get AWS credentials from IEEE DataPort

1. Log in to IEEE DataPort
2. Click Account in the top right corner
3. Copy your AWS Access Key ID
4. Click Show AWS Secret Access Key and copy the key

These credentials are issued by IEEE DataPort and control which datasets you can access.

---

### Step 2 Copy dataset S3 URIs

1. Open the dataset page on IEEE DataPort
2. Select the AWS S3 tab
3. Click on individual files to copy their S3 URI
4. Or use Copy All URIs if available

Example S3 URI:

```
s3://ieee-dataport/data/123626/Benign network traffic.zip
```

---

### Step 3 Download files

1. Paste your AWS Access Key ID into the application
2. Paste your AWS Secret Access Key
3. Keep the AWS region set to us east 1
4. Paste one or more S3 URIs one per line
5. Click Test keys to verify access
6. Click Download files

Downloaded files will be saved to the selected local folder.

---

## Common Errors and Troubleshooting

### 403 Forbidden

This means you do not have permission to access the dataset or file.
Confirm that you have accepted the dataset license or requested access on IEEE DataPort.

### NoSuchKey

The S3 URI path is incorrect or was copied incorrectly.
Ensure the URI matches exactly what is shown in the AWS S3 tab.

### Invalid or expired credentials

AWS keys may expire or be revoked.
Generate new keys from your IEEE DataPort account page and try again.

---

## Security Notes

* AWS credentials are not stored on disk
* Keys are used only for the current Streamlit session
* Never commit AWS keys to version control

---

## License

This project is intended for research and educational use.

All dataset licenses and usage terms are governed by IEEE DataPort and the dataset authors.

---

## Acknowledgment

This tool follows the official IEEE DataPort workflow for accessing private S3 hosted datasets.
