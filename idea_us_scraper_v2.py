#!/usr/bin/env python3
"""
IDEA (dialectsarchive.com) US states scraper (v2)
- Handles 403 by:
  * using a realistic browser User-Agent + headers
  * optional Cookie header via --cookie "name=value; name2=value2"
  * optional fallback to cloudscraper if installed (pip install cloudscraper)
- Downloads audio files and saves rich metadata.

Outputs (under --outdir, default "."):
  data/idea_us_metadata.csv
  data/idea_us_metadata.jsonl
  audio/{STATE}/{SAMPLE}.mp3

Examples:
  python idea_us_scraper_v2.py
  python idea_us_scraper_v2.py --states "Vermont,California"
  python idea_us_scraper_v2.py --cookie "$(python -c 'print(open(\"cookies.txt\").read().strip())')"

Tip: If you still get 403, open a sample page in your browser, copy request headers (esp. Cookie),
     and pass them with --cookie.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

# --- HTTP client setup -------------------------------------------------------
def create_http_client(cookie_header: Optional[str] = None):
    """
    Returns (session, using_cloudscraper: bool)
    Tries cloudscraper if available, else requests.Session
    """
    headers = {
        # Realistic desktop Chrome UA (macOS) – adjust as needed
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/127.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
    }
    if cookie_header:
        headers["Cookie"] = cookie_header.strip()

    try:
        import cloudscraper  # type: ignore
        sess = cloudscraper.create_scraper(
            browser={
                "browser": "chrome",
                "platform": "windows",
                "mobile": False
            }
        )
        sess.headers.update(headers)
        return sess, True
    except Exception:
        import requests  # type: ignore
        sess = requests.Session()
        sess.headers.update(headers)
        return sess, False

# --- Scraper -----------------------------------------------------------------
import requests
from bs4 import BeautifulSoup

BASE = "https://www.dialectsarchive.com/"
USA_PAGE = urljoin(BASE, "united-states-of-america")

AUDIO_EXT_RE = re.compile(r"\.(mp3|wav|m4a|aac|ogg)$", re.I)
SECTION_TITLES = [
    "BIOGRAPHICAL INFORMATION",
    "PHONETIC TRANSCRIPTION OF SCRIPTED SPEECH",
    "ORTHOGRAPHIC TRANSCRIPTION OF UNSCRIPTED SPEECH",
    "PHONETIC TRANSCRIPTION OF UNSCRIPTED SPEECH",
    "SCHOLARLY COMMENTARY",
]
FIELD_ALIASES = {
    "AGE": "age",
    "DATE OF BIRTH (DD/MM/YYYY)": "dob",
    "PLACE OF BIRTH": "place_of_birth",
    "GENDER": "gender",
    "ETHNICITY": "ethnicity",
    "OCCUPATION": "occupation",
    "EDUCATION": "education",
    "AREAS OF RESIDENCE OUTSIDE REPRESENTATIVE REGION FOR LONGER THAN SIX MONTHS": "residence_outside_region",
    "AREA(S) OF RESIDENCE OUTSIDE REPRESENTATIVE REGION FOR LONGER THAN SIX MONTHS": "residence_outside_region",
    "OTHER INFLUENCES ON SPEECH": "other_speech_influences",
    "RECORDED BY": "recorded_by",
    "DATE OF RECORDING (DD/MM/YYYY)": "recording_date",
    "PHONETIC TRANSCRIPTION OF SCRIPTED SPEECH": "phonetic_transcription_scripted",
    "TRANSCRIBED BY": "transcribed_by",
    "DATE OF TRANSCRIPTION (DD/MM/YYYY)": "transcription_date",
    "ORTHOGRAPHIC TRANSCRIPTION OF UNSCRIPTED SPEECH": "orthographic_transcription_unscripted",
    "PHONETIC TRANSCRIPTION OF UNSCRIPTED SPEECH": "phonetic_transcription_unscripted",
    "SCHOLARLY COMMENTARY": "scholarly_commentary",
    "COMMENTARY BY": "commentary_by",
    "DATE OF COMMENTARY (DD/MM/YYYY)": "commentary_date",
}

REQUEST_TIMEOUT = 30
THROTTLE_S = 0.8

@dataclass
class SampleRecord:
    state: str
    state_url: str
    sample_title: str
    sample_url: str
    audio_url: Optional[str]
    audio_filename: Optional[str]
    description_line: Optional[str]
    fields: Dict[str, Optional[str]]

class Scraper:
    def __init__(self, session: requests.Session, throttle: float = THROTTLE_S):
        self.sess = session
        self.throttle = throttle

    def _get(self, url: str) -> Optional[requests.Response]:
        time.sleep(self.throttle)
        try:
            r = self.sess.get(url, timeout=REQUEST_TIMEOUT, allow_redirects=True)
            if r.status_code == 403:
                sys.stderr.write(f"[WARN] 403 Forbidden at {url} — try passing --cookie from your browser or installing cloudscraper\n")
                return None
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            sys.stderr.write(f"[WARN] GET failed {url}: {e}\n")
            return None

    def soup(self, url: str) -> Optional[BeautifulSoup]:
        resp = self._get(url)
        if not resp:
            return None
        return BeautifulSoup(resp.text, "html.parser")

    def get_state_links(self) -> List[Tuple[str, str]]:
        soup = self.soup(USA_PAGE)
        if not soup:
            return []

        out = []
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            if not text:
                continue
            href = a["href"]
            url = urljoin(BASE, href)
            # Heuristic: single path segment (state slug) and not the USA hub
            path = urlparse(url).path.strip("/")
            if path and "/" not in path and path.lower() not in {"united-states-of-america"}:
                if re.fullmatch(r"[A-Za-z .'-]+", text) and text[0].isupper():
                    out.append((text, url))

        # Deduplicate preserving order
        seen = set()
        unique = []
        for name, url in out:
            key = (name.lower(), url)
            if key not in seen:
                seen.add(key)
                unique.append((name, url))
        return unique

    def parse_state_samples(self, state_name: str, state_url: str) -> List[Tuple[str, str, str]]:
        soup = self.soup(state_url)
        if not soup:
            return []
        samples = []
        prefix = state_name.lower().replace(" ", "-")
        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            url = urljoin(BASE, a["href"])
            slug = urlparse(url).path.strip("/")
            if slug.startswith(prefix):
                desc = None
                parent_text = a.parent.get_text(" ", strip=True) if a.parent else title
                if parent_text and len(parent_text) > len(title):
                    desc = parent_text.replace(title, "").strip(" –:;,-")
                samples.append((title, url, desc))
        # Dedup
        seen = set()
        dedup = []
        for t, u, d in samples:
            if u not in seen:
                seen.add(u)
                dedup.append((t, u, d))
        return dedup

    def extract_audio_url(self, soup: BeautifulSoup) -> Optional[str]:
        # direct anchors to audio
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href and AUDIO_EXT_RE.search(href):
                return urljoin(BASE, href)
        # <audio> or <source>
        for audio in soup.find_all("audio"):
            src = audio.get("src")
            if src and AUDIO_EXT_RE.search(src):
                return urljoin(BASE, src)
            for source in audio.find_all("source"):
                s2 = source.get("src")
                if s2 and AUDIO_EXT_RE.search(s2):
                    return urljoin(BASE, s2)
        return None

    @staticmethod
    def _normalize(s: Optional[str]) -> str:
        return re.sub(r"\s+", " ", (s or "")).strip()

    def parse_fields(self, soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        blocks = []
        for el in soup.find_all(["h2", "h3", "p", "div", "li"]):
            txt = self._normalize(el.get_text(" ", strip=True))
            if txt:
                blocks.append(txt)

        data: Dict[str, Optional[str]] = {}
        current = None
        section_buf: List[str] = []

        def flush():
            nonlocal current, section_buf
            if current and section_buf:
                key = FIELD_ALIASES.get(current, current.lower().replace(" ", "_"))
                data[key] = "\n".join(section_buf).strip()
            current, section_buf = None, []

        for line in blocks:
            if line in SECTION_TITLES:
                flush()
                current = line
                continue

            if current:
                if line in SECTION_TITLES:
                    flush()
                    current = line
                else:
                    section_buf.append(line)
                continue

            m = re.match(r"^([A-Z0-9 ()/\-–—]+):\s*(.*)$", line)
            if m:
                raw, val = m.group(1).strip(), m.group(2).strip()
                key = FIELD_ALIASES.get(raw, raw.lower().replace(" ", "_"))
                if key in data and data[key]:
                    data[key] = f"{data[key]}\n{val}"
                else:
                    data[key] = val
        flush()
        return data

    @staticmethod
    def slugify(s: str) -> str:
        s = s.lower().strip()
        s = re.sub(r"[^a-z0-9]+", "-", s)
        s = re.sub(r"-+", "-", s).strip("-")
        return s or "sample"

    def download(self, url: str, outpath: Path) -> bool:
        try:
            with self.sess.get(url, timeout=REQUEST_TIMEOUT, stream=True) as r:
                if r.status_code == 403:
                    sys.stderr.write(f"[WARN] 403 on audio: {url}\n")
                    return False
                r.raise_for_status()
                outpath.parent.mkdir(parents=True, exist_ok=True)
                with open(outpath, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
            return True
        except requests.RequestException as e:
            sys.stderr.write(f"[WARN] audio download failed {url}: {e}\n")
            return False

    def scrape_state(self, state_name: str, state_url: str, audio_root: Path) -> List[SampleRecord]:
        print(f"[INFO] State: {state_name} ({state_url})")
        samples = self.parse_state_samples(state_name, state_url)
        print(f"[INFO]  Found {len(samples)} samples")
        out: List[SampleRecord] = []
        for title, url, desc in samples:
            print(f"[INFO]   Sample: {title}")
            soup = self.soup(url)
            if not soup:
                continue
            audio_url = self.extract_audio_url(soup)
            fields = self.parse_fields(soup)

            state_slug = self.slugify(state_name)
            sample_slug = self.slugify(title) or self.slugify(urlparse(url).path.split("/")[-1])
            audio_filename = None
            if audio_url:
                ext = os.path.splitext(urlparse(audio_url).path)[1] or ".mp3"
                outpath = audio_root / state_slug / f"{sample_slug}{ext}"
                if self.download(audio_url, outpath):
                    audio_filename = str(outpath)
            else:
                sys.stderr.write(f"[WARN]    No audio found for {title}\n")

            out.append(SampleRecord(
                state=state_name,
                state_url=state_url,
                sample_title=title,
                sample_url=url,
                audio_url=audio_url,
                audio_filename=audio_filename,
                description_line=desc,
                fields=fields,
            ))
        return out

# --- Main --------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Scrape IDEA US states (audio + metadata).")
    parser.add_argument("--states", type=str, default="", help="Comma-separated state names to scrape (default all).")
    parser.add_argument("--outdir", type=str, default=".", help="Output directory (default .)")
    parser.add_argument("--cookie", type=str, default="", help="Cookie header string to include (from your browser).")
    parser.add_argument("--max-states", type=int, default=0, help="Limit number of states (debug).")
    args = parser.parse_args()

    sess, used_cloud = create_http_client(args.cookie or None)
    if used_cloud:
        print("[INFO] Using cloudscraper client")
    else:
        print("[INFO] Using requests Session (install cloudscraper for CF-challenge sites)")

    scraper = Scraper(sess)

    outdir = Path(args.outdir).resolve()
    data_dir = outdir / "data"
    audio_root = outdir / "audio"
    data_dir.mkdir(parents=True, exist_ok=True)

    # discover states
    states = scraper.get_state_links()
    if args.states.strip():
        wanted = {s.strip() for s in args.states.split(",") if s.strip()}
        states = [(n, u) for (n, u) in states if n in wanted]
        if not states:
            sys.stderr.write("[WARN] No matching states for the provided filter\n")

    if args.max_states > 0:
        states = states[: args.max_states]

    all_records: List[SampleRecord] = []
    try:
        for name, url in states:
            all_records.extend(scraper.scrape_state(name, url, audio_root))
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted; writing partial results…")

    # write outputs
    csv_path = data_dir / "idea_us_metadata.csv"
    jsonl_path = data_dir / "idea_us_metadata.jsonl"

    # CSV header
    base_cols = ["state", "state_url", "sample_title", "sample_url", "audio_url", "audio_filename", "description_line"]
    dynamic_keys = set()
    for rec in all_records:
        dynamic_keys.update(rec.fields.keys())
    fieldnames = base_cols + sorted(dynamic_keys)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in all_records:
            row = {
                "state": rec.state,
                "state_url": rec.state_url,
                "sample_title": rec.sample_title,
                "sample_url": rec.sample_url,
                "audio_url": rec.audio_url,
                "audio_filename": rec.audio_filename,
                "description_line": rec.description_line,
            }
            for k in dynamic_keys:
                row[k] = rec.fields.get(k, "")
            writer.writerow(row)

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for rec in all_records:
            obj = {
                "state": rec.state,
                "state_url": rec.state_url,
                "sample_title": rec.sample_title,
                "sample_url": rec.sample_url,
                "audio_url": rec.audio_url,
                "audio_filename": rec.audio_filename,
                "description_line": rec.description_line,
                "fields": rec.fields,
            }
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    print(f"[DONE] Wrote {csv_path}")
    print(f"[DONE] Wrote {jsonl_path}")
    print(f"[DONE] Audio under {audio_root}")

if __name__ == "__main__":
    main()
