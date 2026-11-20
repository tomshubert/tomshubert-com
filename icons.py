"""Simple line icons, added in front of matching <h3> headings by build.py."""
import re

P = {
  "cloud": '<path d="M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z"/>',
  "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
  "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
  "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
  "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
  "wifi": '<path d="M12 20h.01M2 8.82a15 15 0 0 1 20 0M5 12.86a10 10 0 0 1 14 0M8.5 16.43a5 5 0 0 1 7 0"/>',
  "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20M2 12h20"/>',
  "bug": '<path d="m8 2 1.88 1.88M14.12 3.88 16 2M9 7.13v-1a3 3 0 1 1 6 0v1M12 20c-3.3 0-6-2.7-6-6v-3a4 4 0 0 1 4-4h4a4 4 0 0 1 4 4v3c0 3.3-2.7 6-6 6M12 20v-9M6.53 9C4.6 8.8 3 7.1 3 5M6 13H2M3 21c0-2.1 1.7-3.9 3.8-4M20.97 5c0 2.1-1.6 3.8-3.5 4M22 13h-4M17.2 17c2.1.1 3.8 1.9 3.8 4"/>',
  "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3M12 9v4M12 17h.01"/>',
  "printer": '<path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
  "apps": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
  "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
  "user": '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
  "user-minus": '<circle cx="9" cy="7" r="4"/><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2M22 11h-6"/>',
  "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6M15.5 7.5l3 3L22 7l-3-3"/>',
  "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>',
  "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14a9 3 0 0 0 18 0V5M3 12a9 3 0 0 0 18 0"/>',
  "eye": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
  "buoy": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="4"/><path d="m4.93 4.93 4.24 4.24M14.83 9.17l4.24-4.24M14.83 14.83l4.24 4.24M9.17 14.83l-4.24 4.24"/>',
  "folder": '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
  "swap": '<path d="m16 3 4 4-4 4M20 7H4M8 21l-4-4 4-4M4 17h16"/>',
  "share": '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><path d="m8.59 13.51 6.83 3.98M15.41 6.51l-6.82 3.98"/>',
  "hash": '<path d="M4 9h16M4 15h16M10 3 8 21M16 3l-2 18"/>',
  "sliders": '<path d="M21 4h-7M10 4H3M21 12h-9M8 12H3M21 20h-5M12 20H3M14 2v4M8 10v4M16 18v4"/>',
  "mobile": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>',
  "chat": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
  "check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
  "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
  "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
  "network": '<rect x="16" y="16" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="9" y="2" width="6" height="6" rx="1"/><path d="M5 16v-3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3M12 12V8"/>',
}

# Heading text (as written in the HTML) -> icon
H3 = {
  # Home: Explore cards
  "Microsoft 365": "cloud", "Security": "shield", "Services": "wrench",
  "Clients &amp; stories": "briefcase", "Phone service": "phone", "About Tom": "user",
  # Home: how I work
  "You deal with me": "user", "Remote first, anywhere": "globe",
  "No contract required": "clock", "Plain answers": "chat",
  # Services
  "Computers &amp; support": "monitor", "Networks &amp; wireless": "wifi",
  "Business phone service": "phone", "Security &amp; backups": "shield",
  "Business software": "apps", "Malware &amp; recovery": "bug",
  "Office technology": "printer", "Websites": "globe",
  # Microsoft 365
  "SharePoint &amp; OneDrive": "folder", "Email, Teams &amp; calendars": "mail",
  "A careful move": "swap", "Sensible security": "lock",
  "Sharing with outsiders": "share", "Optional backup &amp; 24/7 monitoring": "database",
  # Security
  "Multifactor sign-in": "key", "Email filtering": "mail", "Protected computers": "monitor",
  "Optional 24/7 monitoring": "eye", "Backups": "database", "Spotting scams": "alert",
  "People who leave": "user-minus", "When something goes wrong": "buoy",
  "Secure remote access": "lock",
  # Phone Service
  "Choosing the right service": "check", "Keeping your numbers": "hash",
  "Set up before you switch": "sliders", "Calls anywhere": "mobile",
  "Your network, ready for voice": "network", "Training and support after": "chat",
  # Remote help
  "Step by step": "monitor", "You stay in control": "lock", "Backup for Windows: Quick Assist": "buoy",
}

def svg(name):
    return ('<span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' + P[name] + '</svg></span>')

def add_icons(html):
    def rep(m):
        text = m.group(1)
        return f"<h3>{svg(H3[text])}{text}</h3>" if text in H3 else m.group(0)
    return re.sub(r"<h3>(.*?)</h3>", rep, html)
