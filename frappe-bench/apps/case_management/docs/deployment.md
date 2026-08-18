# Deployment

## Two different environments — don't confuse them

- **`.devcontainer/`** (in `frappe_docker`, forked separately) — development only. Bind-mounts your code, runs everything unoptimized, has no real security hardening. This is what Codespaces/local VS Code uses while building the app.
- **`docker-compose.yml`** (in this repo) — production-style. Builds a real image with the app baked in, no bind mounts, no developer mode.

## 1. Build the custom image

This app depends on `frappe/frappe_docker`'s official layered build (`images/layered/Containerfile`), which reads `docker/apps.json` to know which apps to bake into the image.

```bash
# from a clone of frappe/frappe_docker
git clone https://github.com/frappe/frappe_docker
cd frappe_docker

docker build \
  --build-arg=FRAPPE_PATH=https://github.com/frappe/frappe \
  --build-arg=FRAPPE_BRANCH=version-16 \
  --secret=id=apps_json,src=/path/to/case_management/docker/apps.json \
  --tag=case-management:latest \
  --file=images/layered/Containerfile .
```

Update `docker/apps.json` first: point the second entry at your actual GitHub repo URL and branch (it currently has a placeholder).

## 2. Run it

```bash
cp .env.example .env   # set DB_ROOT_PASSWORD, ADMIN_PASSWORD, SITE_NAME
docker compose up -d
```

`configurator` runs once to wire up DB/Redis hostnames, `create-site` runs once to create the site and install the app, then `backend`, `frontend`, `websocket`, the two queue workers, and `scheduler` stay running. The app is reachable at `http://localhost:${HTTP_PORT}` (default 8080).

## 3. Honest caveats

This compose file is adapted from frappe_docker's well-documented production pattern, not copy-pasted from a pinned, tested source — the core shape (configurator → create-site → backend/frontend/websocket/workers/scheduler, all sharing a `sites` volume) is standard and stable across recent Frappe versions, but exact environment variable names occasionally shift between releases. If a container fails to start, the fastest fix is usually to check its logs against the current docs at https://github.com/frappe/frappe_docker/tree/main/docs rather than assuming this file is wrong in spirit.

For anything beyond a single-server demo deploy (TLS termination, backups, horizontal scaling, secrets management) — out of scope for this portfolio project by design (see "What NOT to Build Initially" in the project plan). Worth being able to talk through in the interview as a "what I'd add for real production use" answer, without having actually built it.
