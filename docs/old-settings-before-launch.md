# tomshubert.com settings before the new site went live (saved 2026-11-14)

## How to switch back to the old site
The old DNS zone stays untouched at GoDaddy (YourWEB reseller account). To go back, set the domain's
nameservers at YourWEB back to:
    ns11.domaincontrol.com
    ns12.domaincontrol.com
Everything (old website, email) then works exactly as before. The old site's files stay on the GoDaddy
hosting at 107.180.46.146 until that hosting plan is cancelled.

## DNS records as they were (looked up 2026-11-14)
| Name | Type | TTL | Value |
|---|---|---|---|
| tomshubert.com | NS | 3600 | ns11.domaincontrol.com, ns12.domaincontrol.com |
| tomshubert.com | A | 10800 | 107.180.46.146 (old GoDaddy website hosting) |
| tomshubert.com | MX | 1800 | 10 aspmx.l.google.com |
| tomshubert.com | MX | 1800 | 20 alt1.aspmx.l.google.com |
| tomshubert.com | MX | 1800 | 30 alt2.aspmx.l.google.com |
| tomshubert.com | MX | 1800 | 40 aspmx2.googlemail.com |
| tomshubert.com | MX | 1800 | 50 aspmx3.googlemail.com |
| tomshubert.com | TXT | 1800 | google-site-verification=… (68 chars) |
| tomshubert.com | TXT | 1800 | MS=… (Microsoft 365 domain verification, 43 chars) |
| tomshubert.com | TXT | 1800 | v=spf1 include… (35 chars) |
| tomshubert.com | TXT | 1800 | verifydomain… (28 chars) |
| www | CNAME | 10800 | tomshubert.com |
| mail | A | 10800 | 107.180.46.146 |
| admin | A | 10800 | 107.180.46.146 |
| cpanel | CNAME | 10800 | tomshubert.com |
| remote | A | 3600 | 24.160.39.12 |
| calendar | CNAME | 1800 | ghs.google.com |
| docs | CNAME | 1800 | ghs.google.com |
| sites | CNAME | 1800 | ghs.google.com |
| _dmarc | TXT | 1800 | v=DMARC1; p=quarantine… (48 chars) |
| google._domainkey | TXT | 3600 | v=DKIM1; k=rsa; p=… (Google Workspace DKIM key, 410 chars) |
| _domainconnect | CNAME | 3600 | _domainconnect.ss.domaincontrol.com |

Full TXT values are copied exactly into the Cloudflare zone (and remain in the GoDaddy zone).
