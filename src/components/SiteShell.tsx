import Link from "next/link";
export default function SiteShell({ children }: { children: React.ReactNode }) {
  return (
    <>
      <a className="skip-link" href="#main">
        Skip to content
      </a>
      <header className="site-header">
        <Link className="brand" href="/">
          ◒ <span>THE DATING POOL</span>
        </Link>
        <nav aria-label="Main">
          <Link href="/">Calculator</Link>
          <Link href="/explorer">Data explorer</Link>
          <Link href="/sources">Sources</Link>
          <Link href="/methodology">How it works</Link>
        </nav>
      </header>
      <main id="main">{children}</main>
      <footer>
        <span>Published inputs. Estimated overlap.</span>
        <a
          href="https://desktop-smsroim.tail0be63c.ts.net/"
          target="_blank"
          rel="noopener noreferrer"
        >
          Local Tailscale access ↗
        </a>
        <a
          href="https://www.passportpowell.com/card"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="Passport Powell Card"
        >
          <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
            <path
              fill="currentColor"
              d="M12 .8a11.2 11.2 0 0 0-3.54 21.83c.56.1.77-.24.77-.54v-2.1c-3.13.68-3.79-1.33-3.79-1.33-.51-1.3-1.25-1.65-1.25-1.65-1.02-.7.08-.69.08-.69 1.13.08 1.72 1.16 1.72 1.16 1 1.72 2.62 1.22 3.26.93.1-.73.4-1.22.71-1.5-2.5-.28-5.13-1.25-5.13-5.57 0-1.23.44-2.23 1.16-3.02-.12-.28-.5-1.43.11-2.98 0 0 .94-.3 3.08 1.15a10.7 10.7 0 0 1 5.6 0c2.14-1.45 3.08-1.15 3.08-1.15.61 1.55.23 2.7.11 2.98.72.79 1.16 1.79 1.16 3.02 0 4.33-2.64 5.28-5.15 5.56.4.35.76 1.03.76 2.08v3.1c0 .3.2.65.77.54A11.2 11.2 0 0 0 12 .8Z"
            />
          </svg>
        </a>
      </footer>
    </>
  );
}
