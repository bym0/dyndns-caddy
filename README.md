# dyndns caddy (sidecar)

This little script will be used in pair with a Caddy Container and will periodically resolve the Environment variable "DYNDNS_DOMAIN" and write the result to the file "/app/dyndns.conf".

Now we mount this file from dyndns to our machine and again to caddy, to actually use that in our Caddyfile:
```yaml

services:
  caddy:
    container_name: caddy
    image: caddy:latest
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
    ports:
      - "80:80"
      - "443:443"
      - "443:443/udp"
    volumes:
      - /opt/caddy/Caddyfile:/etc/caddy/Caddyfile
      - /opt/caddy/site:/srv
      - caddy_data:/data
      - caddy_config:/config
      - ./dyndns.conf:/etc/caddy/dyndns.conf # Here! :)
    depends_on:
          dyndns:
            condition: service_healthy

  dyndns:
    container_name: dyndns
    image: ghcr.io/bym0/caddy-dyndns-sidecar:latest
    restart: unless-stopped
    volumes:
      - ./dyndns.conf:/app/dyndns.conf # And here! :)

volumes:
  caddy_data:
  caddy_config:

```