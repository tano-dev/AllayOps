# Fabric Server Mods Source (`mods_src/`)

Place custom **Fabric (MC 26.3 / Loader 0.20.1 / JDK 25)** server-side mod sources here (e.g., `allayops-telemetry` or `allayops-parry-guard`).

## Planned Responsibilities
- Expose sub-50ms tick telemetry (`MSPT`, `TPS`, `PrimedTnt` & entity counts per chunk) over a local socket/HTTP/JMX endpoint.
- Provide an in-JVM **Active Parry Hook** to freeze or throttle runaway entity/explosion ticks before hitting `max-tick-time=60000` Server Watchdog.

> **Note:** Compiled `*.jar` outputs are excluded from Git by `.gitignore`; build artifacts should be published via GitHub Releases.
