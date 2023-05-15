# SxT Commands

## CLI
### cd to directory with the file and check operation:
```bash
    java -jar sxtcli-0.0.2.jar help
```

### registering:
1. check user id exists:
    ```bash
        java -jar sxtcli-0.0.2.jar authenticate check-id --url="<https://<SxT-API-URL>" --userId="<userId>"
    ```
2. generate a new keypair:
    ```bash
        java -jar sxtcli-0.0.2.jar authenticate keypair
    ```
3. request user creation:
    ```bash
        java -jar sxtcli-0.0.2.jar authenticate register --code="<orgCode>" --privateKey="<privateKey>" --url="<https://<SxT-API-URL>" --userId="<userId>"
    ```
4. obtain accessToken and refreshTokens:
    ```bash
        java -jar sxtcli-0.0.2.jar authenticate login --privateKey="<privateKey>" --publicKey="<publicKey>" --url="https://<SXT-API-URL>" --userId="<userId>"
    ```
- accessTokens expire after 30 minutes, so renew with:
    ```bash
        java -jar sxtcli-0.0.2.jar authenticate refresh --refreshToken="<refreshToken>" --url="https://<SXT-API-URL>"
    ```

### curl commands via Python Requests:
