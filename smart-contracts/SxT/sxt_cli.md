# SxT Commands and Data

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
- after creating a schema, generate a biscuit keypair and table biscuit:
    ```bash
        java -jar sxtcli-0.0.2.jar biscuit keypair
        java -jar sxtcli-0.0.2.jar biscuit generate table --privateKey=$b_priv_key --resources="<SCHEMA>.<TABLE_1>,<SCHEMA>.<TABLE_2>" --operations="CREATE,ALTER,DROP,INSERT,UPDATE,MERGE,DELETE,SELECT"
    ```

### curl commands via Python Requests:


## DATA
Schema: 