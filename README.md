# hyperplane-client
a client-code facing library exposing internal APIs for the hyperplane platform

## Utilities
## Secret_utils
* Get Secret:
   1. Get a secret corresponding with the given `{secret_name}` value from the Hyperplane secret manager (set via the UI).
   1. Local usage: fetching the secret value from an environment variable named: `HYPERPLANE_SECRET_{secret_name}` (set using the `export`/`set` command)

## aws_s3_utils
### For local run: (file example)
  ```
  # set environment variables:
  import os
  
  os.environ['HYPERPLANE_SECRET_s3_bucket_name']='my_aws_bucket_name'
  os.environ['HYPERPLANE_SECRET_s3_access_key_secret']='my_aws_access_key_secret'
  os.environ['HYPERPLANE_SECRET_s3_access_key_id']='my_aws_access_key_id'
  ```
  #### Download from s3:
  ```
  # example usage:
  source_path_in_s3 = 'my-bucket-dir-1/file-name-in-s3-1.data'
  target_path = './my-local-dir-1/file-name-in-my-computer-1.data'
  
  download_from_s3(source_path=source_path_in_s3, target_path=target_path)
      
  ```
  #### Upload to s3:
  ```
  # example usage:
  source_path_in_my_computer = './my-local-dir-1/file-name-in-my-computer-1.data'
  target_path = 'my-bucket-dir-1/file-name-in-s3-1.data'
  
  file_path_in_s3 = upload_to_s3(source_path=source_path_in_my_computer, target_path=target_path)      
  ```
### For running in server: (directory example with regex filter)
  `# set s3 related secrets in the UI`

  ![](readme_assets/s3_ui_creds.png)
  #### Download from s3:
  ```
  # example usage:
  source_path_in_s3 = 'my-bucket-dir-2/'
  target_path = './my-local-dir-2/'
  regex_filter = 'file_prefix_[0-9][0-9][0-9]' # file_prefix_100, file_prefix_123, file_prefix_754... 
  
  download_from_s3(source_path=source_path_in_s3, target_path=target_path, regex_filter=regex_filter)
      
  ```
  #### Upload to s3:
  ```
  # example usage:
  target_path = 'my-bucket-dir-2/'
  source_path_in_my_computer = './my-local-dir-2/'
  regex_filter = 'file_prefix_[0-9][0-9][0-9]' # file_prefix_100, file_prefix_123, file_prefix_754... 
  
  file_paths = upload_to_s3(source_path=source_path_in_my_computer, target_path=target_path, regex_filter=regex_filter)
      
  ```
