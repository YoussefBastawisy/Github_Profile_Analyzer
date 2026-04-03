from flask import Flask, render_template, redirect, url_for, request
from lib.github_api import fetch_user, fetch_repos, GitHubAPIError
from lib.scorer import calculate_score, get_score_label, get_language_stats

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    username = request.form.get('username', '').strip().lstrip('@')
    if not username:
        return redirect(url_for('index'))
    return redirect(url_for('profile', username=username))


@app.route('/<username>')
def profile(username):
    try:
        user  = fetch_user(username)
        repos = fetch_repos(username)

        score_data = calculate_score(user, repos)
        label      = get_score_label(score_data['total'])
        languages  = get_language_stats(repos)
        top_repos  = sorted(
            [r for r in repos if not r.get('fork')],
            key=lambda r: r.get('stargazers_count', 0),
            reverse=True
        )[:6]

        return render_template(
            'profile.html',
            user=user,
            score=score_data,
            label=label,
            languages=languages,
            top_repos=top_repos,
        )

    except GitHubAPIError as e:
        return render_template('index.html', error=str(e))
    except Exception as e:
        return render_template('index.html', error=f'Unexpected error: {e}')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
