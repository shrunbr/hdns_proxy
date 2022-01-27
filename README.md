# hdns_proxy
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

[![Build/Release Stable](https://github.com/shrunbr/hdns_proxy/actions/workflows/build.yml/badge.svg?branch=v0.2.0)](https://github.com/shrunbr/hdns_proxy/actions/workflows/build.yml)

hdns_proxy is a python-based Handshake DNS reverse proxy using Flask.

## Getting Started

To get started using hdns_proxy, you'll need to first clone this repo.

Once this repo has been cloned please copy the `config_example.yaml` file into `config.yaml` and update accordingly per the options below.

```
secretKey: Update this with a randomly generated string at least 32 characters in length. This is Flasks super secret key
rootDomain: This is the domain you own to host this proxy (ex. hdns.co)
bindAddress: This should typically stay 0.0.0.0 however, if you're running this on a server you can change it to the server interface IP you want to bind to
rootRedirect: This is the URL which the server should redirect your root domain to (ex. hdns.co redirects to this repo)
port: This should typically stay as port 80, this tells Flask which port to run the webserver on
nameservers: This is a list of nameservers which are able to resolve Handshake domains. If you change them from their default, ensure whichever DNS servers you use are able to resolve Handshake DNS names.
```

## Running hdns_proxy

There are two different ways to run hdns_proxy.

1. You can close this repo, install the requirements.txt and run the `app.py` script on any machine. This will launch the webserver and proxy directly.

2. You can build the docker image with the included `Dockerfile`.

To build the docker image, clone the repo, ensure you have Docker installed and run `docker build -t hdns_proxy:stable .` from within cloned directory.

3. You can use our pre-built docker image available on [ghcr.io](https://github.com/shrunbr/hdns_proxy/pkgs/container/hdns_proxy)

This docker image can be referenced in `docker-compose.yml` files by setting the image to `ghcr.io/shrunbr/hdns_proxy:stable` (see our provided `docker-compose.yml` file for reference).

## Using Caddy

To use Caddy with hdns_proxy, you can use the pre-built `docker-compose.yml` file included in this repo. If you need to be able to get SSL certificates by doing ACME DNS verification you can follow the guide located [here](https://caddy.community/t/how-to-use-dns-provider-modules-in-caddy-2/8148).

I use Cloudflare for DNS so below this I've placed what you can use for a Caddy docker image w/ Cloudflare DNS. Copy the content below into a `Dockerfile` and run `docker build -t caddy:cloudflare .` to build the image. Once the build is complete, replace the `image:` tag under `caddy` in the `docker-compose.yml` file with `caddy:cloudflare`. You can then use a Cloudflare API key to verify the domains via ACME DNS Verification.

```
FROM caddy:builder AS builder

RUN xcaddy build  --with github.com/caddy-dns/cloudflare

FROM caddy:latest

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
```

## Example Caddyfile w/ Cloudflare

```
{
    # Global options block. Entirely optional, https is on by default
    # Optional email key for lets encrypt
    email shrunbr@shrunbr.dev
    # Optional staging lets encrypt for testing. Comment out for production.
    #acme_ca https://acme-staging-v02.api.letsencrypt.org/directory
    acme_dns cloudflare <CLOUDFLARE_API_KEY>
}
hdns.co {
    reverse_proxy hdns_proxy:80
}
*.hdns.co {
    reverse_proxy hdns_proxy:80
}
```

## Example Caddyfile w/ Cloudflare & Nested Subdomains (HTTP-Only)

```
{
    # Global options block. Entirely optional, https is on by default
    # Optional email key for lets encrypt
    email shrunbr@shrunbr.dev
    # Optional staging lets encrypt for testing. Comment out for production.
    #acme_ca https://acme-staging-v02.api.letsencrypt.org/directory
    acme_dns cloudflare <CLOUDFLARE_API_KEY>
}
hdns.co {
    reverse_proxy hdns_proxy:80
}
*.hdns.co {
    reverse_proxy hdns_proxy:80
}
http://*.*.hdns.co {
    reverse_proxy hdns_proxy:80
}
http://*.*.*.hdns.co {
    reverse_proxy hdns_proxy:80
}
```

*hdns_proxy was inspired by angrymouses [hns-bridge](https://github.com/angrymouse/hns-bridge)*