# How to rotate the signing key

Rotate the signing key every 90 days, or immediately when you suspect that it leaked.
The `auth` service is written in Go and reads the key from the `SIGNING_KEY` secret at
startup, so a rotation needs a restart.

## Before you start

You need `kubectl` access to the `prod` cluster and the `secrets-admin` role.

## Steps

1. Generate the new key:

   ```bash
   openssl genpkey -algorithm ed25519 -out signing.pem
   ```

2. Add the new key to the secret as `SIGNING_KEY_NEXT`. The `auth` service accepts
   tokens signed with either key while both are present.

   ```bash
   kubectl -n auth create secret generic signing --from-file=SIGNING_KEY_NEXT=signing.pem --dry-run=client -o yaml | kubectl apply -f -
   ```

3. Restart the `auth` service:

   ```bash
   kubectl -n auth rollout restart deployment/auth
   ```

   Wait until `kubectl -n auth rollout status deployment/auth` prints
   `successfully rolled out`.

4. Promote the new key: copy the value of `SIGNING_KEY_NEXT` to `SIGNING_KEY` and delete
   `SIGNING_KEY_NEXT`. Then restart the service again, as in step 3.

Tokens that the old key signed stop working after step 4. The `auth` service issues
tokens that live 15 minutes, so wait 15 minutes between step 3 and step 4.
