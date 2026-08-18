### Case Management

A small, self-contained case-management system built on the Frappe framework: structured case records, assignment, an enforced status workflow, role-based permissions (with row-level restriction), SLA tracking, and a REST + custom API.

This is an independent portfolio project. It is not affiliated with, endorsed by, or built for any specific organization — the domain is intentionally generic, and all data is synthetic.

### Design docs

- [`docs/architecture.md`](docs/architecture.md) — system diagram, why Frappe, where logic lives and why
- [`docs/api.md`](docs/api.md) — REST + the custom `assign_case` endpoint
- [`docs/security.md`](docs/security.md) — permission model, server-side enforcement, secrets handling
- [`docs/deployment.md`](docs/deployment.md) — building and running the production image

### Data model, workflow, and permission matrix

See `02-data-model-and-design.md` for the full DocType field specs, the Case workflow state machine, and the role/permission matrix this app implements.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app case_management
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/case_management
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit
