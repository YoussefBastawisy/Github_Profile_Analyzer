# GitHub Profile Analyzer

A web app that analyzes any GitHub profile and generates a full developer report — tech stack breakdown, top repositories, developer score, and actionable recommendations.

> Built entirely by [Cycls Super Agent](https://super.cycls.ai) from a single prompt, as part of a real-world AI use case series by [@YoussefBastawisy](https://github.com/YoussefBastawisy).

---

## What it does

Paste any GitHub username and get back:

- **Tech Stack** — languages used across all repos with percentage breakdown
- **Top Repositories** — top 5 repos by stars with descriptions and metadata
- **Developer Score** — score out of 100 based on profile completeness, activity, tech diversity, and community impact
- **Score Breakdown** — detailed view of each scoring category
- **Recommendations** — actionable tips to improve your GitHub profile

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| Frontend | HTML, CSS, JavaScript |
| Data | GitHub REST API (public) |
| Styling | Custom dark theme, no frameworks |

---

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YoussefBastawisy/Github_Analyzer.git
cd Github_Analyzer
```

### 2. Install dependencies

```bash
pip install flask requests
```

### 3. Run the app

```bash
python app.py
```

### 4. Open in browser

```
http://localhost:5050
```

---

## Usage

1. Open the app in your browser
2. Enter any GitHub username in the search box
3. Hit **Analyze**
4. Get your full developer profile report in seconds

---

## Current Limitations

This is an MVP. Known limitations:

- Only analyzes **public repositories** — private repos are not accessible via the public GitHub API
- Language stats are based on the **20 most recently updated repos**
- Score algorithm is rule-based, not AI-powered (yet)
- No caching — each request hits the GitHub API directly

---

## How it was built

This project was built from scratch by **Cycls Super Agent** using a single natural language prompt — no manual coding, no boilerplate setup.

When the agent ran into a compatibility issue with the initial approach, it identified the problem, proposed an alternative solution, and continued building without any intervention.

The output was downloaded as a folder, opened in any IDE, and ran immediately.

This is part of an ongoing series of real-world use cases showing what Cycls can build in minutes.

Try it yourself: [super.cycls.ai](https://super.cycls.ai)

---

## Roadmap

- [ ] Support for private repos via GitHub OAuth
- [ ] Contribution heatmap visualization
- [ ] AI-generated profile summary
- [ ] Compare two GitHub profiles side by side
- [ ] Export report as PDF

---

## License

MIT
