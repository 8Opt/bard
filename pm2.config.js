module.exports = {
    apps: [
      {
        name: "bard",
        script: "source .venv/bin/activate && fastapi run app --host 0.0.0.0 --port 7077",
        args: [],
        exec_mode: "fork",
        instances: 1,
        wait_ready: true,
        autorestart: true,
        max_restarts: 5,
        interpreter: "",
        cron_restart: "",
      },
    ],
  };
  