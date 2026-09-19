"""Explainable migration recommendation for a synthetic application inventory."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Application:
    name: str
    source: str
    os: str
    stateful: bool
    has_container_build: bool
    dependencies: int
    data_gb: int
    regulated: bool


def assess(app: Application) -> dict[str, object]:
    if app.source != "Azure VM":
        raise ValueError("This exercise accepts an Azure VM as its source")
    if not app.name.strip() or app.dependencies < 0 or app.data_gb < 0:
        raise ValueError("Name is required; counts cannot be negative")

    reasons: list[str] = []
    if app.stateful:
        route = "VM first, then modernize"
        reasons.append("Persistent local state needs a separate data and backup plan before containerization.")
    elif app.has_container_build:
        route = "Containerize and deploy"
        reasons.append("A repeatable container build exists and the service is stateless.")
    else:
        route = "VM first, then modernize"
        reasons.append("No repeatable container build exists yet; preserve behavior before refactoring.")

    wave = "Later wave" if app.dependencies > 2 or app.data_gb > 100 or app.regulated else "Pilot wave"
    if wave == "Later wave":
        reasons.append("Dependencies, data volume, or regulated data require extra discovery and controls.")

    checklist = [
        "Inventory inbound/outbound dependencies and owner-approved downtime window.",
        "Map Azure identities to least-privilege GCP service identities; do not transfer credentials.",
        "Design network connectivity, DNS, firewall policy, and non-overlapping address ranges.",
        "Take a source backup and define a restore point and rollback owner.",
        "Transfer synthetic test data and compare row counts and checksums before cutover.",
        "Test application behavior, latency, logs, and alerts before changing traffic.",
        "Cut over gradually; restore source routing if acceptance checks fail.",
    ]
    if route == "Containerize and deploy":
        checklist.insert(4, "Build and scan an image locally; test service boundaries and configuration outside the image.")
    else:
        checklist.insert(4, "Validate guest OS compatibility, machine sizing, image, and boot behavior in a trial migration.")
    return {"name": app.name, "route": route, "wave": wave,
            "reasons": reasons, "checklist": checklist}
