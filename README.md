# Daily Wiki Insights 🧠

An autonomous, AI-powered website that generates daily insights from Wikipedia's Featured Article. It connects historical facts to modern life, running entirely on your local machine or GitHub Actions.

## 🚀 Features

-   **Autonomous Content Generation**: Fetches Wikipedia's "Today's Featured Article" daily.
-   **AI-Powered Insights**: Uses OpenRouter (Claude/GPT) to rewrite content into engaging, relevant insights.
-   **Modern Editorial Design**: Generates a clean, responsive static site.
-   **Self-Healing**: Includes an agent script to monitor and fix generation issues.
-   **Automated Deployment**:
    -   **Windows**: Runs via Task Scheduler and pushes to GitHub Pages.
    -   **GitHub Actions**: (Optional) Can run entirely in the cloud.

## 🛠️ Setup

### Prerequisites

-   **Python 3.12+**
-   **uv** (Fast Python package manager): `pip install uv` or see [astral.sh/uv](https://astral.sh/uv)
-   **Git** configured with your GitHub account.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/wikipedia-insights.git
    cd wikipedia-insights
    ```

2.  **Initialize the environment**:
    ```bash
    uv sync
    ```

3.  **Configure Secrets**:
    -   Copy `.env.example` to `.env`:
        ```bash
        cp .env.example .env
        ```
    -   Edit `.env` and add your **OpenRouter API Key**:
        ```
        OPENROUTER_API_KEY=sk-or-v1-your-key-here
        ```
    -   *Note: `.env` is git-ignored to keep your secrets safe.*

## 🏃‍♂️ Usage

### ⚡ One-Time GitHub Setup (Required for Website)

To make your website live, you need to enable GitHub Pages **once**:

1.  Push your code to GitHub: `git push origin main`
2.  Wait for the "Daily Wikipedia Insights Update" action to finish (it might fail the first time if Pages isn't set up, that's okay).
3.  Go to your repository **Settings** > **Pages**.
4.  Under **Build and deployment** > **Source**, select **Deploy from a branch**.
5.  Under **Branch**, select **gh-pages** and **/ (root)**.
6.  Click **Save**.

🎉 Your site is now live at `https://<your-username>.github.io/wikipedia-insights/`!

### Manual Run

Generate the site immediately:
```bash
uv run src/main.py
```
Check `site/index.html` to see the result.

### 📅 Automate on Windows

This sets up a daily task (9:00 AM) that generates content locally and pushes it to GitHub, which then updates the live site.

1.  **Open PowerShell as Administrator**.
2.  **Run the setup script**:
    ```powershell
    ./scripts/setup_schedule.ps1
    ```
3.  **Verify**: Open "Task Scheduler" and look for `WikipediaInsightsDailyUpdate`.

### ☁️ Automate on GitHub Actions

1.  Go to your repository **Settings > Secrets and variables > Actions**.
2.  Add a new Repository Secret:
    -   Name: `OPENROUTER_API_KEY`
    -   Value: Your OpenRouter API key.
3.  The workflow is already configured in `.github/workflows/daily-update.yml`.

## 🛡️ Security

-   **No Secrets in Code**: All API keys are loaded from environment variables or the `.env` file.
-   **Safe Commits**: The `.gitignore` file ensures sensitive files (logs, envs) are never committed.

## 🤝 Contributing

Feel free to open issues or submit PRs to improve the prompts or styling!

---
*Powered by [OpenRouter](https://openrouter.ai) and [Wikipedia](https://wikipedia.org).*
