# RPi Home Server
Kubernetes cluster (K3s) hosted on a Raspberry Pi to manage my home media and networking configuration.

Ansible playbooks to automate the initial pi setup, cluster deployment and cluster destruction.

## Getting Started

Flash Raspberry Pi OS Lite (64-bit) and run `./setup.sh` to lockdown the pi and assign a static IP address.

Run `./create.sh` to install K3s and applications.

Run `./destroy.sh` to uninstall the cluster.

## Applications

- [Pi-hole](https://pi-hole.net) - advertising-aware DNS/web server.
- RSS Tracker - email notifications for rss feed updates.
- [Prometheus Stack](https://prometheus.io) - enable alerts and cluster visualisation on grafana.
- [NextCloud](https://nextcloud.com) - self-hosted cloud storage.

### Extras

- Pi-hole backups - automated weekly backup and reload on deployment of pi-hole's database using Google Drive.

### Todo

- [Home Assistant](https://www.home-assistant.io/) - centralise home IoT devices from multiple providers.
- [OctoPrint](https://octoprint.org) - remote dashboard for 3D printers.
- [Bitwarden](https://bitwarden.com) - open source password manager.

## Other Setup Steps

### Tokens

- Google Drive Service Account Token - used for pihole backup jobs
- Cloudflare DNS API Token - used for cert-manager challenge

### DNS Setup

- A Record - dashboard - `nginx-ingress-external-ip` - DNS only (no cloudflare proxy)
- A Record - pihole - `nginx-ingress-external-ip` - DNS only (no cloudflare proxy)
- A Record - prometheus - `nginx-ingress-external-ip` - DNS only (no cloudflare proxy)
- A Record - alertmanager - `nginx-ingress-external-ip` - DNS only (no cloudflare proxy)
- A Record - grafana - `nginx-ingress-external-ip` - DNS only (no cloudflare proxy)
- A Record - cloud - `nginx-ingress-external-ip` - DNS only (no cloudflare proxy)

### Ingress

- First metallb ip pool address - Nginx ingress
- Second metallb ip pool address - Pihole DNS ingress
