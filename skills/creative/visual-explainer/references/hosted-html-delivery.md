# Hosted HTML Delivery Pattern

Use this when a user needs a visual explainer/dashboard to open from a phone or messaging app as a clickable web page.

## Why
- Local HTML attachments often do not open correctly in Discord/Telegram clients.
- Full-page screenshots of long dashboards become blurry/unreadable.
- PDF can flatten the intended interactive/web layout and may feel like a downgrade when the user asked for HTML.

## Preferred delivery order
1. Public hosted HTML link that opens directly in the browser.
2. Native HTML attachment only as fallback.
3. Section-by-section readable images or PDF only when explicitly requested or when hosting is impossible.

## Temporary VPS hosting pattern
When no permanent hosting/domain is already configured:

```bash
mkdir -p /opt/hermes-public/<slug>
cp ~/.agent/diagrams/<file>.html /opt/hermes-public/<slug>/index.html
python3 -m http.server 8088 --directory /opt/hermes-public
```

Verify locally:

```bash
curl -I http://127.0.0.1:8088/<slug>/
```

If public IP + port is blocked by firewall/security group, use a temporary Cloudflare quick tunnel:

```bash
# if cloudflared is missing, install/update explicitly
curl -fsSL -o /usr/local/bin/cloudflared \
  https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x /usr/local/bin/cloudflared

cloudflared tunnel --url http://127.0.0.1:8088
```

Extract the `https://...trycloudflare.com` URL and verify it:

```bash
curl -I https://<tunnel-host>/<slug>/
```

Report the verified link and say clearly whether it is temporary. Do not claim permanence for quick tunnels.

## Permanent delivery options
- Configure a real domain/subdomain + reverse proxy/static server.
- Open the chosen port in both host firewall and cloud security group if direct-IP hosting is desired.
- Use a proper named Cloudflare Tunnel if Cloudflare is available.

## User-facing wording
- Short and direct: “Sudah gue host, tinggal klik: <url>”.
- Include only the key caveat: “sementara” vs “permanen”.
- Offer permanent setup as the next step; do not over-explain unless asked.