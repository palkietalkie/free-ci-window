// Starts run-scheduled-workflows.yml at minute 7 of every hour. GitHub's own `schedule:` fired it only 2 to 5 times a day since 2026-10-28, so reminders, daily content and reports skipped most days (palkietalkie/workspace#1462); a Cloudflare cron trigger fires every hour, and workflow_dispatch starts a run at once.
const DISPATCH_URL =
  "https://api.github.com/repos/palkietalkie/free-ci-window/actions/workflows/run-scheduled-workflows.yml/dispatches";

export default {
  async scheduled(_controller, env) {
    const response = await fetch(DISPATCH_URL, {
      method: "POST",
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${env.GH_DISPATCH_TOKEN}`,
        "User-Agent": "free-ci-window-hourly-clock",
        "X-GitHub-Api-Version": "2022-11-28",
      },
      body: JSON.stringify({ ref: "main" }),
    });
    // A failed start throws, so it shows in the Worker's logs as a failed scheduled run rather than passing silently.
    if (!response.ok) throw new Error(`dispatch answered ${response.status}: ${await response.text()}`);
  },
};
