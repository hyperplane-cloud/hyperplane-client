# hyperplane-dev
a client-code facing library exposing internal APIs for the hyperplane platform

## Utilities
### Secret_utils
* Get Secret:
   1. Get a secret corresponding with the given `{secret_name}` value from the Hyperplane vault (set via the UI).
   1. Local usage: fetching the secret value from an environment variable named: `HYPERPLANE_SECRET_{secret_name}` (set using the `export`/`set` command)