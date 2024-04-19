# HTTPS

## TLS Handshake

First, we have the **Client Hello**.

It contains the Random:

```
468f695f355788d44da83964e68a10437ffd3cba099adb83cd1fc2ee49f31a2b
```

Then we have the **Server Hello**.

It contains another Random:

```
8da75c7e50de388c2ef938432680c5f0a6d6c96e98bb3bad7b05a6c7bc0efc93
```

It contains the chose cipher suite `0x1302`:

```
Cipher Suite: TLS_AES_256_GCM_SHA384 (0x1302)
```

Then we have the **Encrypted Extensions**, **Certificate**, **Certificate Verify** and **Server Handshake Finished** in one packet (note that the packet is encrypted).

Finally we have the **Client Change Cipher Spec** and **Client Handshake Finished** in one packet (note that the packet is encrypted).
