# hyperplane-client
a client-code facing library exposing internal APIs for the hyperplane platform

## Utilities
## Secret_utils
* Get Secret:
   1. Get a secret corresponding with the given `{secret_name}` value from the Hyperplane secret manager (set via the UI).
   1. Local usage: fetching the secret value from an environment variable named: `HYPERPLANE_SECRET_{secret_name}` (set using the `export`/`set` command)

## aws_s3_utils
### For local run:
First, set your 3 secrets: bucket name, access key and secret key as environment variables. 
Can be done anyway, for example with python:
  ```python
import os

os.environ['HYPERPLANE_SECRET_s3_bucket_name']='my_aws_bucket_name'
os.environ['HYPERPLANE_SECRET_s3_access_key_secret']='my_aws_access_key_secret'
os.environ['HYPERPLANE_SECRET_s3_access_key_id']='my_aws_access_key_id'
  ```
  #### Download a single file from s3 to your local machine:
  ```python
from hyperplane.aws_s3_utils import download_from_s3

source_path_in_s3 = 'my-bucket-dir-1/file-name-in-s3-1.data'
target_path = './my-local-dir-1/file-name-in-my-computer-1.data'

download_from_s3(source_path=source_path_in_s3, target_path=target_path)
      
  ```
  #### Upload a single file to s3 from your local machine:
  ```python
from hyperplane.aws_s3_utils import upload_to_s3

source_path_in_my_computer = './my-local-dir-1/file-name-in-my-computer-1.data'
target_path = 'my-bucket-dir-1/file-name-in-s3-1.data'

file_path_in_s3 = upload_to_s3(source_path=source_path_in_my_computer, target_path=target_path)      
  ```
### For running in server: 
  First set s3 related secrets in the UI

  ![](readme_assets/s3_ui_creds.png)
  #### Download a filtered set of files from s3 to a *job server* directory:
  ```python
from hyperplane.aws_s3_utils import download_from_s3

source_path_in_s3 = 'my-bucket-dir-2/'  # when downloading a dir, path should end with '/'
target_path = './my-local-dir-2/'       # when downloading a dir, path should end with '/'
regex_filter = 'file_prefix_[0-9][0-9][0-9]' # file_prefix_100, file_prefix_123, file_prefix_754... 

download_from_s3(source_path=source_path_in_s3, target_path=target_path, regex_filter=regex_filter)
      
  ```
  #### Download a complete directory from s3 to a *job server* directory:
  ```python
from hyperplane.aws_s3_utils import download_from_s3

source_path_in_s3 = 'my-bucket-dir-2/'  # when downloading a dir, path should end with '/'
target_path = './my-server-dir-2/'       # when downloading a dir, path should end with '/'

download_from_s3(source_path=source_path_in_s3, target_path=target_path)
      
  ```
  #### Upload a filtered set of files from a *job server* directory to s3:
  ```python
from hyperplane.aws_s3_utils import upload_to_s3

target_path = 'my-bucket-dir-2/'                  # when uploading a dir, path should end with '/'
source_path_in_my_server = './my-server-dir-2/'  # when uploading a dir, path should end with '/'
regex_filter = 'file_prefix_[0-9][0-9][0-9]' # file_prefix_100, file_prefix_123, file_prefix_754... 

file_paths = upload_to_s3(source_path=source_path_in_my_server, target_path=target_path, regex_filter=regex_filter)
      
  ```
  #### Upload complete directory from a *job server* directory to s3:
  ```python
from hyperplane.aws_s3_utils import upload_to_s3

target_path = 'my-bucket-dir-2/'                  # when uploading a dir, path should end with '/'
source_path_in_my_server = './my-server-dir-2/'  # when uploading a dir, path should end with '/'

file_paths = upload_to_s3(source_path=source_path_in_my_server, target_path=target_path)
      
  ```
