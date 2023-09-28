from google.cloud import storage

def upload_file_to_gcs(file_path, bucket_name, gcs_path):
  """Uploads a file to Google Cloud Storage.

  Args:
    file_path: The path to the file to upload.
    bucket_name: The name of the bucket to upload the file to.
    gcs_path: The path to the file in Google Cloud Storage.
  """

  client = storage.Client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(gcs_path)
  blob.upload_from_filename(file_path)
  
def upload(jsonl_file):
    # Upload the JSON Lines file to Google Cloud Storage.
    bucket_name = "kuhne_nagel_hackathon_23"
    gcs_path = "exp01_llm_txt_gen_eval/trial01_learn_how_to_use_it/test_data/part-00000-of-00001.jsonl"

    upload_file_to_gcs(jsonl_file, bucket_name, gcs_path)
  
if __name__ == "__main__":
    jsonl_file = "./data/llm_eval_data.jsonl"
    upload(jsonl_file)