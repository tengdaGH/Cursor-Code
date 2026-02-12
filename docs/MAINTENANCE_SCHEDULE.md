# Periodic documentation & logs maintenance

A maintenance script runs **every 12 hours** to validate documentation, review-log references, and the project skill. It does **not** change the content of `item-review-log.md` or skills; it only checks structure and writes a last-run stamp.

---

## What runs

- **Script:** `scripts/docs_maintenance.py`
- **Checks:** Data files have `meta.reviewLogRef` and valid JSON; practice HTML pages have the REVIEW LOG comment and `item-review-log.md` reference; required docs and skill exist.
- **Output:** Writes `docs/.maintenance-last-run.txt` with status (`OK` / `WARN` / `FAIL`) and any errors/warnings. Exit code 0 if OK, 1 if any error.

---

## Run once (manual)

From the project root:

```bash
python3 scripts/docs_maintenance.py
echo "Exit code: $?"
cat docs/.maintenance-last-run.txt
```

---

## Schedule every 12 hours

### Option A: macOS (launchd) — recommended on Mac

1. Copy the plist template:

   ```bash
   cp scripts/com.nyk.docs-maintenance.plist.template ~/Library/LaunchAgents/com.nyk.docs-maintenance.plist
   ```

2. Edit `~/Library/LaunchAgents/com.nyk.docs-maintenance.plist` and replace **both** occurrences of `REPLACE_WITH_PROJECT_ROOT` with your project root (e.g. `/Users/you/Cursor Code`). That sets `WorkingDirectory` and the script path in `ProgramArguments`.

3. Load and start:

   ```bash
   launchctl load ~/Library/LaunchAgents/com.nyk.docs-maintenance.plist
   ```

4. Check it’s loaded: `launchctl list | grep nyk.docs-maintenance`

5. To stop: `launchctl unload ~/Library/LaunchAgents/com.nyk.docs-maintenance.plist`

### Option B: Linux / macOS (cron)

1. Open crontab: `crontab -e`

2. Add a line to run every 12 hours (e.g. at 00:00 and 12:00):

   ```cron
   0 */12 * * * cd /path/to/your/project && python3 scripts/docs_maintenance.py >> /tmp/docs-maintenance.log 2>&1
   ```

   Replace `/path/to/your/project` with the real project root.

---

## Last-run stamp

After each run, `docs/.maintenance-last-run.txt` looks like:

```
status=OK
errors=0
warnings=0
```

On failure:

```
status=FAIL
errors=2

error: read-in-daily-life-passages.json: meta.reviewLogRef missing or wrong
error: toefl-reading-daily-life-practice.html: missing REVIEW LOG comment or item-review-log.md reference
```

Add `docs/.maintenance-last-run.txt` to `.gitignore` if you don’t want it committed (it’s machine-specific).
