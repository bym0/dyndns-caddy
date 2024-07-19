# dyndns caddy (sidecar)

This little script will be used in pair with a Caddy Container and will periodically resolve the Environment variable "DYNDNS_DOMAIN" and write the result to the file "/app/dyndns.conf".

Now we mount this file from dyndns to our machine and again to caddy, to actually use that in our Caddyfile:

But first:
```bash
touch dyndns.config
```

and then...

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
    image: ghcr.io/bym0/dyndns-caddy:latest
    restart: unless-stopped
    environment:
      DYNDNS_DOMAIN: <YOUR DOMAIN>
    volumes:
      - ./dyndns.conf:/app/dyndns.conf # And here! :)
    healthcheck:
      test: ["CMD-SHELL", "[ -s /app/dyndns.conf ]"]
      interval: 10s
      timeout: 15s
      retries: 3

volumes:
  caddy_data:
  caddy_config:

```

aaaand then you should be able to

```

uptime-kuma.example.com {
  import /etc/caddy/dyndns_ips.conf
  reverse_proxy / http://127.0.0.1:3000
}

```