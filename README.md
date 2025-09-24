# Product-Management

## Overview
This repository is a sandbox for demonstrating Product Management scenarios with [Harness](https://www.harness.io/) and other delivery tooling. It collects reusable manifests, Helm charts, Kustomize overlays, AWS ECS task definitions, and CI/CD pipeline specifications that can be mixed and matched when showcasing deployment strategies or validating new platform features. The content is intentionally lightweight so it can be cloned quickly and used in lab environments, live demos, or internal experiments.

## Repository structure
The repo is organized by deployment technology or scenario. The most commonly referenced paths are summarised below:

| Path | Purpose |
| --- | --- |
| `azure-pipelines.yml` | Azure Pipelines definition for building container images as part of CI demos. |
| `cd_lab/sample-webapp` | Kubernetes manifests used in Harness CD lab exercises (deployment, HPA, and values). |
| `cdng` | Default Helm chart values for Harness Next-Gen CD services. |
| `ecs/taskdefinition.json` | Reusable AWS Fargate task definition template parameterised with Harness expressions. |
| `helm-cdng/mychart` | Example Helm chart leveraged in Harness CD pipelines. |
| `jobs/pi.yaml` | Kubernetes job manifest used when demonstrating batch workloads. |
| `k8s/microservice-demo.yaml` | Google Online Boutique microservices demo manifest for multi-service rollouts. |
| `kustomize-cdng` | Base and overlay configurations for showing Kustomize-driven releases. |
| `pipelines/approval.yaml` | Harness pipeline sample highlighting manual approval stages. |
| `traffic-shifting-nginx` | Blue/green and canary style NGINX manifests for progressive delivery walkthroughs. |

Additional folders (for example `kustomize-cdng/overlays` or `traffic-shifting-nginx/templates`) hold supporting templates and environment-specific overrides.

## Typical workflows
* **Continuous Integration experiments** – Trigger the `azure-pipelines.yml` workflow (or import it into Harness CI) to build a container image using the repository Dockerfiles.
* **Continuous Delivery demonstrations** – Point Harness services at the manifests under `cdng`, `cd_lab`, `helm-cdng`, or `traffic-shifting-nginx` to exercise rolling, blue/green, and canary deployment strategies.
* **Cloud provider exploration** – Use the `ecs` task definition and the Kubernetes specs in `k8s/` and `jobs/` when testing deployments across AWS Fargate and Kubernetes clusters.

## Getting started
1. Clone the repository into your demo or lab environment.
2. Choose the manifest or pipeline definition that matches the scenario you want to showcase.
3. Update Harness (or your preferred CI/CD tool) to reference the selected files, supplying any required runtime inputs such as service names, namespaces, or artifact tags.
4. Run the pipeline or apply the manifests to the target environment.

Because the repository is used for experimentation, feel free to extend the manifests with additional services, environments, or delivery strategies as new features are evaluated.
