import re
from pathlib import Path

import streamlit as st
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from urllib.parse import unquote


def parse_s3_uri(uri: str):
    m = re.match(r"^s3://([^/]+)/(.+)$", uri.strip())
    if not m:
        raise ValueError("Invalid S3 URI. Expected: s3://bucket/path/to/file")
    return m.group(1), m.group(2)


def safe_mkdir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


st.set_page_config(page_title="IEEE DataPort S3 Downloader", layout="centered")
st.title("IEEE DataPort Downloader")

st.write("Paste one or many S3 URIs from the IEEE DataPort AWS S3 tab, one per line.")

aws_access_key_id = st.text_input("AWS Access Key ID", type="password")
aws_secret_access_key = st.text_input("AWS Secret Access Key", type="password")
region = st.text_input("AWS Region", value="us-east-1")

download_dir = Path(st.text_input("Download folder", value=str(Path.cwd() / "ieee_dataport_downloads")))
safe_mkdir(download_dir)

uris_text = st.text_area(
    "S3 URIs",
    value="",
    height=140
)

col1, col2 = st.columns(2)
with col1:
    test_identity = st.button("Test keys")
with col2:
    do_download = st.button("Download files", type="primary")

if test_identity:
    try:
        session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region,
        )
        sts = session.client("sts", config=Config(signature_version="v4"))
        ident = sts.get_caller_identity()
        st.success(f"Keys OK. Account: {ident.get('Account')}  Arn: {ident.get('Arn')}")
    except Exception as e:
        st.error(f"Key test failed: {e}")

if do_download:
    try:
        session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region,
        )
        s3 = session.client("s3", config=Config(signature_version="s3v4"))

        uris = [u.strip() for u in uris_text.splitlines() if u.strip()]
        if not uris:
            st.warning("Paste at least one S3 URI.")
            st.stop()

        progress = st.progress(0.0)
        status = st.empty()

        for i, uri in enumerate(uris, start=1):
            bucket, key = parse_s3_uri(uri)
            key = unquote(key)

            out_path = download_dir / Path(key).name
            status.write(f"{i}/{len(uris)} Downloading: {bucket}/{key}")

            try:
                s3.download_file(bucket, key, str(out_path))
                st.write(f"Saved: {out_path}")
            except ClientError as ce:
                st.error(f"Failed: {uri}  Error: {ce}")
                continue

            progress.progress(i / len(uris))

        status.success("Done.")
    except Exception as e:
        st.error(f"Download failed: {e}")
