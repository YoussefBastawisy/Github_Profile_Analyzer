from datetime import datetime, timezone

LANGUAGE_COLORS = {
    'JavaScript': '#f1e05a',
    'TypeScript': '#3178c6',
    'Python':     '#3572A5',
    'Java':       '#b07219',
    'Go':         '#00ADD8',
    'Rust':       '#dea584',
    'C':          '#555555',
    'C++':        '#f34b7d',
    'C#':         '#239120',
    'Ruby':       '#701516',
    'PHP':        '#4F5D95',
    'Swift':      '#FA7343',
    'Kotlin':     '#A97BFF',
    'Dart':       '#00B4AB',
    'HTML':       '#e34c26',
    'CSS':        '#563d7c',
    'Shell':      '#89e051',
    'Vue':        '#41b883',
    'Svelte':     '#ff3e00',
    'R':          '#198CE7',
    'Scala':      '#c22d40',
    'Haskell':    '#5e5086',
    'Elixir':     '#6e4a7e',
    'Lua':        '#000080',
    'Perl':       '#0298c3',
    'default':    '#8b949e',
}


def calculate_score(user, repos):
    now = datetime.now(timezone.utc)
    own_repos = [r for r in repos if not r.get('fork')]

    # ── Activity (0–25) ──────────────────────────────────────
    repo_score   = min(user.get('public_repos', 0) / 4, 10)
    recent_count = 0
    for r in own_repos:
        updated = datetime.fromisoformat(r['updated_at'].replace('Z', '+00:00'))
        if (now - updated).days < 180:
            recent_count += 1
    recent_score = min(recent_count * 1.5, 10)
    gist_score   = min(user.get('public_gists', 0) / 4, 5)
    activity     = round(min(repo_score + recent_score + gist_score, 25))

    # ── Impact (0–25) ────────────────────────────────────────
    total_stars = sum(r.get('stargazers_count', 0) for r in own_repos)
    total_forks = sum(r.get('forks_count', 0) for r in own_repos)
    impact      = round(min(total_stars / 20 + total_forks / 10, 25))

    # ── Community (0–20) ─────────────────────────────────────
    followers  = user.get('followers', 0)
    following  = user.get('following', 1) or 1
    community  = round(min(followers / 8 + min((followers / following) * 1.5, 5), 20))

    # ── Code Quality (0–15) ──────────────────────────────────
    with_desc = sum(1 for r in own_repos if r.get('description', ''))
    desc_score  = (with_desc / len(own_repos)) * 7 if own_repos else 0
    languages   = {r.get('language') for r in repos if r.get('language')}
    lang_score  = min(len(languages) * 1.2, 5)
    with_topics = sum(1 for r in own_repos if r.get('topics'))
    topic_score = min((with_topics / len(own_repos)) * 3, 3) if own_repos else 0
    code_quality = round(min(desc_score + lang_score + topic_score, 15))

    # ── Consistency (0–15) ───────────────────────────────────
    created   = datetime.fromisoformat(user['created_at'].replace('Z', '+00:00'))
    age_years = (now - created).days / 365
    age_score = min(age_years * 1.2, 6)
    profile_score = 0
    if user.get('bio') and len(user.get('bio', '')) > 5: profile_score += 2.5
    if user.get('blog'):              profile_score += 2.0
    if user.get('location'):          profile_score += 1.5
    if user.get('company'):           profile_score += 1.5
    if user.get('twitter_username'):  profile_score += 1.5
    consistency = round(min(age_score + profile_score, 15))

    total = min(activity + impact + community + code_quality + consistency, 100)

    return {
        'total': total,
        'activity': {
            'score': activity, 'max': 25, 'label': 'Activity', 'icon': 'activity',
            'detail': f"{user.get('public_repos', 0)} repos · {recent_count} active in last 6 mo"
        },
        'impact': {
            'score': impact, 'max': 25, 'label': 'Impact', 'icon': 'zap',
            'detail': f"{total_stars:,} total stars · {total_forks:,} forks"
        },
        'community': {
            'score': community, 'max': 20, 'label': 'Community', 'icon': 'users',
            'detail': f"{followers:,} followers · {following:,} following"
        },
        'code_quality': {
            'score': code_quality, 'max': 15, 'label': 'Code Quality', 'icon': 'code',
            'detail': f"{len(languages)} languages · {round(with_desc/len(own_repos)*100) if own_repos else 0}% repos have description"
        },
        'consistency': {
            'score': consistency, 'max': 15, 'label': 'Consistency', 'icon': 'clock',
            'detail': f"{age_years:.1f} years on GitHub"
        },
    }


def get_score_label(score):
    if score >= 85:
        return {'label': 'Elite',     'emoji': '🏆', 'color': '#ffd700', 'glow': '0 0 20px rgba(255,215,0,0.4)'}
    if score >= 70:
        return {'label': 'Pro',       'emoji': '⚡', 'color': '#3fb950', 'glow': '0 0 20px rgba(63,185,80,0.4)'}
    if score >= 55:
        return {'label': 'Developer', 'emoji': '💻', 'color': '#58a6ff', 'glow': '0 0 20px rgba(88,166,255,0.4)'}
    if score >= 35:
        return {'label': 'Explorer',  'emoji': '🔭', 'color': '#d29922', 'glow': '0 0 20px rgba(210,153,34,0.4)'}
    return     {'label': 'Beginner',  'emoji': '🌱', 'color': '#8b949e', 'glow': '0 0 20px rgba(139,148,158,0.4)'}


def get_language_stats(repos):
    counts = {}
    for r in repos:
        lang = r.get('language')
        if lang:
            counts[lang] = counts.get(lang, 0) + 1
    total = sum(counts.values())
    if not total:
        return []
    return [
        {
            'language':   lang,
            'count':      count,
            'percentage': round(count / total * 100),
            'color':      LANGUAGE_COLORS.get(lang, LANGUAGE_COLORS['default']),
        }
        for lang, count in sorted(counts.items(), key=lambda x: x[1], reverse=True)[:7]
    ]
