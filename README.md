# hyperplane-dev
a client-code facing library exposing internal APIs for the hyperplane platform

## Utilities
### Secret_utils
1. Get Secret:
   1. Local usage: fetching the secret from environment variable
      1. Set the environment variable `HYPERPLANE_SECRET_{secret_name}` with your secret
   2. Remote: fetching the secret remotely
      1. Set the secret in the UI / api