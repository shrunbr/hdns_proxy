# hdns_proxy

hdns_proxy is a python-based Handshake DNS reverse proxy using Flask.

## Getting Started

:construction: **Coming Soon** :construction:

## Using Caddy

To use Caddy with hdns_proxy, you can use the pre-built `docker-compose.yml` file included in this repo. If you need to be able to get SSL certificates by doing ACME DNS verification you can follow the guide located [here](https://caddy.community/t/how-to-use-dns-provider-modules-in-caddy-2/8148).

I use Cloudflare for DNS so below this I've placed what you can use for a Caddy docker image w/ Cloudflare DNS. Copy the content below into a `Dockerfile` and run `docker build -t caddy:cloudflare .` to build the image. Once the build is complete, replace the `image:` tag under `caddy` in the `docker-compose.yml` file with `caddy:cloudflare`. You can then use a Cloudflare API key to verify the domains via ACME DNS Verification.

```
FROM caddy:builder AS builder

RUN xcaddy build  --with github.com/caddy-dns/cloudflare

FROM caddy:latest

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
```