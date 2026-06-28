# The Hunt — Name Rater (the built app)

A single web page that lets the family rate the candidate business names and send
their results back to you. Built from the spec in `../BUILD-REQUIREMENTS.md`.

**It's one file: `index.html`.** No server, no accounts, no database, nothing to install.

---

## Try it right now (on your Mac)

Double-click `index.html`. It opens in your browser and everything works (voting,
modes, leaderboard, even the share link). You don't need the internet or any setup
to test it. To see the phone layout, open your browser's responsive/device view, or
just make the window narrow.

## The two safety rules (built in)

1. **It never changes `names.json`.** The names are a *copy* embedded inside `index.html`.
   The app only reads them.
2. **No vote ever overwrites another.** Every person's votes are kept separately and
   tagged with their name. When you combine results, people are merged side by side. If
   the same person sends a newer link, only *their own* entry updates.

## How people use it

1. You send them one link (see hosting below). They open it on their phone.
2. They pick their name, then rate names: **Swipe** (yes/maybe/no), **Rate** (stars),
   **Duel** (pick one of two), and **Notes** (leave a comment on any name). A comment
   box sits on every name card, always visible, in every mode.
3. When they're done they tap **"Send my ratings"** → **Copy link** (or **Share via
   WhatsApp**) and send it to you. There's a **Download file** button as a backup.
4. You open their link, or paste it into the leaderboard's "Add their ratings" box, or
   load their file. Their votes drop into the combined **Leaderboard**.
5. From the leaderboard you can **Export combined results** and **Summary for Claude** —
   hand the summary to Claude to fold each person's reactions into `names.json` under
   each name's `leans`.

## Sharing the link (how the round-trip works)

The "Send my ratings" link carries the person's votes *inside the link itself*,
compressed with the browser's own built-in compression (no library, nothing installed).
That's why no server is needed. If someone's link ever gets too long to paste, the app
tells them to use the Download-file backup instead.

## Putting it online so others can open it

For other people to open it on their phones, it needs one public web address. Easiest
free option is **GitHub Pages**. You don't need to know Git — ask Claude to walk you
through it step by step, or:

1. Create a free GitHub account.
2. Make a new repository, upload `index.html` into it.
3. In the repo: Settings → Pages → set it to deploy from the main branch.
4. GitHub gives you a link like `https://yourname.github.io/your-repo/`. That's the link
   you share in WhatsApp.

Because it's a single file, simpler drag-and-drop hosts (e.g. Netlify Drop) also work.

## Refreshing the names later

The names are pasted into a `window.NAMES = [...]` block near the bottom of `index.html`.
When `../names.json` changes, that block needs refreshing. Easiest: ask Claude to
"refresh the names in the rater from names.json" and it'll regenerate that block. Name
`id`s (n001, n012…) are the anchor, so refreshing never loses anyone's votes.

## Getting the results to Claude (Cowork)

You don't have to do anything technical. Just paste the link (or attach the file)
someone sent you into a Cowork chat and ask Claude to read it. Claude can decode it.

Under the hood there's a decoder script here: **`decode.py`**. Claude (or you) can run:

```
python3 decode.py "<paste the link, code, or .json file path>"
```

It prints the votes as clean JSON, which Claude then folds into each name's `leans`
in `../names.json` (keyed by person, referenced by `id`, so nobody's view is lost).

### Payload format (so any future session can decode it)

The "Send my ratings" link looks like:

```
https://<wherever-it's-hosted>/#r=G.H4sIA....
                                 │ │ └── base64url of the data
                                 │ └──── "." separator
                                 └────── prefix: G = gzip, U = uncompressed
```

Only the part after `#r=` is data; the rest is just where the app is hosted (see
"the link points to my own files" — the base only has to be reachable by whoever
opens it). To decode the payload by hand:

1. Take the text after `#r=` (or `?r=` / `&r=`).
2. Split off the prefix before the first `.` — `G` means gzip, `U` means plain.
3. base64url-decode the rest (it uses `-`/`_` instead of `+`/`/`, padding stripped).
4. If the prefix was `G`, gunzip the bytes.
5. The result is UTF-8 JSON: `{ ratingsSchemaVersion, app, voter, exportedAt, events:[…] }`.
   The `events` array is the append-only log described in `../BUILD-REQUIREMENTS.md` §4.

The downloaded backup file, the "Export combined results", and the "Summary for
Claude" exports are **already plain JSON** — no decoding needed, just open them.

## Editing the list of voters

The names on the welcome screen are in `const PEOPLE = [...]` near the top of the script
in `index.html`. Add or change names there. Anyone can also choose "Someone else…" and
type their own name.
