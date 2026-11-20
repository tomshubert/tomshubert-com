// /get-rustdesk?os=win|mac  ->  redirects to the newest official RustDesk download on GitHub.
// Cached for an hour so we don't hit GitHub's API on every click.
const PICK = {
  win: (n) => /^rustdesk-[\d.]+-x86_64\.exe$/i.test(n),
  mac: (n) => /^rustdesk-[\d.]+-x86_64\.dmg$/i.test(n),
  macarm: (n) => /^rustdesk-[\d.]+-aarch64\.dmg$/i.test(n),
};
const FALLBACK = 'https://github.com/rustdesk/rustdesk/releases/latest';

export async function onRequestGet({ request, waitUntil }) {
  const os = new URL(request.url).searchParams.get('os') || 'win';
  const pick = PICK[os] || PICK.win;
  const cache = caches.default;
  const key = new Request('https://cache.tomshubert.com/rustdesk-latest');
  let res = await cache.match(key);
  if (!res) {
    try {
      const r = await fetch('https://api.github.com/repos/rustdesk/rustdesk/releases/latest', {
        headers: { 'user-agent': 'tomshubert.com', accept: 'application/vnd.github+json' },
      });
      if (!r.ok) throw new Error('github ' + r.status);
      const body = JSON.stringify((await r.json()).assets.map((a) => [a.name, a.browser_download_url]));
      res = new Response(body, { headers: { 'cache-control': 'max-age=3600' } });
      waitUntil(cache.put(key, res.clone()));
    } catch (e) {
      return Response.redirect(FALLBACK, 302);
    }
  }
  const assets = await res.json();
  const hit = assets.find(([n]) => pick(n));
  return Response.redirect(hit ? hit[1] : FALLBACK, 302);
}
