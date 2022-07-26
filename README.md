# hyperplane-dev
a client-code facing library exposing internal APIs for the hyperplane platform

## Local Run
### Utilities
#### Secret_utils
1. Get Secret:
   1. Fetching the secret by using the hyperplane secret manager
      1. Set the environment variable `HYPERPLANE_USER_TOKEN` with your session token
   2. Fetching the secret from environment variable
      1. set the environment variable `HYPERPLANE_SECRET_{secret_name}` with your secret