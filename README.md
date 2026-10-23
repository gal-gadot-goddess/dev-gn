# dev-gn 🚀

> Automated Daily Video Publishing Pipeline for DevOps, Kubernetes, Docker, CI/CD, Terraform, Cloud Architecture, and SRE.

[![Daily DevOps Reel Automation](https://github.com/kreggscode/dev-gn/actions/workflows/automate.yml/badge.svg)](https://github.com/kreggscode/dev-gn/actions/workflows/automate.yml)

## 📌 Platforms & Channels
- **Instagram**: [@devopsgen](https://www.instagram.com/devopsgen/) (ID: `17841464799205820`)
- **Facebook Page**: [Devopsgen](https://www.facebook.com/942651072275054) (ID: `942651072275054`)

---

## ⚡ Pipeline Architecture
1. **Cloud Sync**: Synchronizes visual HTML animations from Google Drive folder (`1Com42vZ2qDEnf_Sl5bwKR3z1_4bg2dw1`).
2. **Weighted LRU Selection**: Prioritizes unpublished animations; once all are published, seamlessly runs in recirculation mode using inverse exponential weighting.
3. **AI Metadata Engine**: Pollinations AI crafts high-converting viral hook titles, educational breakdowns, discussion hooks, and strictly 5 lowercase hashtags.
4. **Visual & Audio Rendering**:
   - Headless Chromium Playwright captures visual animations at 1080x1920 (9:16 vertical format) @ 60 FPS.
   - Captures native in-browser Web Audio API synthesized sound effects.
   - **Zero Background Music**: Strictly pure native audio sound effects.
   - Injects high-clarity completed diagram into Frame 0 for guaranteed thumbnail preview.
5. **Multi-Platform Publishing**:
   - Resumable video upload to Instagram Reels (`share_to_feed: false` for Reels tab only).
   - Resumable video upload to Facebook Page Reels with custom thumbnail attachment.
   - Graceful fallback to Threads if configured.
6. **State Tracking**: Stores publication history, video hashes, timestamps, and platform responses in `history.json`.

---

## 🕒 Schedule
- Runs daily at **09:00 UTC** (14:30 IST) via GitHub Actions.
- Can be manually triggered via GitHub Actions (`workflow_dispatch`).

---

## 🛠️ Local Development

### Requirements
- Python 3.10+
- FFmpeg installed and in PATH
- Playwright Chromium (`playwright install chromium`)

### Quick Start
```bash
pip install -r requirements.txt
playwright install chromium
python orchestrator.py --publish
```
