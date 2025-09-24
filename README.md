# Kubernetes, Helm, Kustomize, and Harness CDNG Examples

This repository contains a curated set of infrastructure-as-code examples showing different ways to deploy and operate applications:

- Harness CD NextGen (CDNG) Kubernetes templates with Go-style templating
- A standard Helm v3 chart
- Kustomize base and overlay example
- NGINX Ingress Controller traffic shifting (blue/green, weighted routing)
- AWS ECS Fargate task definition template
- Standalone Kubernetes manifests, including Google Online Boutique microservices demo
- A sample Kubernetes Job

Use these examples to learn, prototype, or integrate with CI/CD pipelines (e.g., Harness).

## Repository Structure

```text
.
├─ cdng/                         # Harness CDNG-compatible K8s templates and values
│  ├─ templates/
│  │  ├─ deployment.yaml         # Templated Deployment + optional imagePullSecret
│  │  ├─ namespace.yaml          # Optional Namespace creation
│  │  └─ service.yaml            # Service (type configurable)
│  └─ values.yaml                # Values used by templates (Harness can override)
├─ ecs/
│  └─ taskdefinition.json        # AWS ECS Fargate task definition (Harness placeholders)
├─ helm-cdng/
│  └─ mychart/                   # Standard Helm chart (nginx default)
│     ├─ Chart.yaml
│     ├─ values.yaml
│     └─ templates/              # Deployment, Service, Ingress, HPA, etc.
├─ jobs/
│  └─ pi.yaml                    # Simple Job computing digits of π (with TTL)
├─ k8s/
│  └─ microservice-demo.yaml     # Google Online Boutique (multi-service demo)
├─ kustomize-cdng/
│  ├─ base/
│  │  ├─ kustomization.yaml      # References base resources
│  │  └─ my-app.yaml             # Deployment (rohan-helloworld)
│  ├─ overlays/
│  │  └─ dev/
│  │     └─ kustomization.yaml   # Example overlay referencing base
│  └─ patch.yaml                 # Example patch with Harness variable placeholders
├─ traffic-shifting-nginx/       # NGINX Ingress Controller CRDs + UI to visualize splits
│  ├─ backend/                   # App Deployment + Services + VirtualServer
│  ├─ frontend/                  # UI that shows/links traffic targets
│  ├─ values.yaml                # Default values (Harness placeholders supported)
│  ├─ 25-values.yaml             # 75/25 split
│  ├─ 50-values.yaml             # 50/50 split
│  └─ 80-values.yaml             # 80/20 split
└─ README.md
```

## Prerequisites

- Kubernetes 1.19+ cluster and `kubectl` configured
- For Helm examples: Helm 3
- For Kustomize: `kubectl` with `-k` support (v1.14+) or standalone kustomize
- For traffic shifting: NGINX Ingress Controller with CRDs `VirtualServer` and `VirtualServerRoute` installed
- For ECS example: AWS account with ECS Fargate and CloudWatch Logs; a pipeline/tooling to render placeholders
- Optional: Harness CD NextGen to render `<+ ... >` expressions and `.Values` in CDNG templates

## Modules and How to Use Them

### 1) Harness CDNG Kubernetes templates (`cdng/`)

Templated Kubernetes manifests rendered by Harness CDNG using `values.yaml` and runtime variables.

- Key values (see `cdng/values.yaml`):
  - `name`: base name used for resources
  - `replicas`: desired replicas
  - `image`: container image
  - `createNamespace`, `namespace`: optional namespace management
  - `serviceType`, `servicePort`, `serviceTargetPort`: service parameters
- Placeholders like `<+service.name>` are resolved by Harness at runtime.

Render/deploy via your Harness pipeline or render with your own templating if you have a compatible renderer. These are not raw `kubectl apply` files until rendered.

### 2) Standard Helm chart (`helm-cdng/mychart`)

This is a conventional Helm v3 chart that deploys an NGINX-based workload.

Install into a namespace:

```bash
helm install myapp /workspace/helm-cdng/mychart -n demo --create-namespace
```

Override values (example: image tag, replicas, ingress):

```bash
helm install myapp /workspace/helm-cdng/mychart \
  -n demo --create-namespace \
  --set image.repository=nginx \
  --set image.tag=1.27 \
  --set replicaCount=2 \
  --set ingress.enabled=true
```

### 3) Kustomize example (`kustomize-cdng/`)

`base/` contains a simple `Deployment` (`rohan-helloworld`) using `harness/todolist-sample:latest`. `overlays/dev` demonstrates referencing the base. `patch.yaml` shows how a patch could inject an image and replicas using Harness variables.

Apply the dev overlay:

```bash
kubectl apply -k /workspace/kustomize-cdng/overlays/dev
```

To use `patch.yaml`, add it to the appropriate `kustomization.yaml` under `patches` and re-apply.

### 4) Google Online Boutique demo (`k8s/microservice-demo.yaml`)

All-in-one manifest for the multi-service demo application (frontend, checkout, payment, cart, etc.). Includes a `Service` named `frontend-external` of type `LoadBalancer`.

Deploy:

```bash
kubectl apply -f /workspace/k8s/microservice-demo.yaml
```

Note: A cloud load balancer may be provisioned depending on your cluster. Ensure your environment supports `Service` type `LoadBalancer`.

### 5) NGINX traffic shifting (`traffic-shifting-nginx/`)

Demonstrates blue/green and weighted routing using NGINX Ingress Controller CRDs (`VirtualServer`, `VirtualServerRoute`). The backend exposes endpoints for a primary and stage service, and the frontend UI visualizes/links the routing targets.

- Set weights via values files:
  - `25-values.yaml`: 75% primary / 25% stage
  - `50-values.yaml`: 50% / 50%
  - `80-values.yaml`: 80% / 20%
- Values include: `host`, `endpoint`, `primaryName`, `stageName`, `primaryEndpoint`, `stageEndpoint`, `splitTraffic`, and a `frontend` block for UI settings.

These manifests use Go-style templating (e.g., `{{ .Values.* }}`) and are intended to be rendered by Harness (or another compatible templating tool) before applying to the cluster.

### 6) AWS ECS Fargate task definition (`ecs/taskdefinition.json`)

Sample ECS task definition configured for Fargate with CloudWatch logs. Fields like `<+service.name>`, `<+artifact.image>`, and `<+serviceVariable.memory>` are Harness expressions resolved at deploy time.

Use within a pipeline that renders the JSON and registers the task definition with ECS.

### 7) Kubernetes Job (`jobs/pi.yaml`)

Simple batch Job that prints 2000 digits of π and is cleaned up after `ttlSecondsAfterFinished: 100` seconds.

Run:

```bash
kubectl apply -f /workspace/jobs/pi.yaml
```

## Notes and Tips

- Harness expressions: Strings like `<+ ... >` are resolved by Harness CDNG at runtime and should not be committed with concrete values unless for local testing.
- Rendering templated files locally: The `cdng/` and `traffic-shifting-nginx/` directories use templating. Render them with Harness or your templating engine of choice before applying with `kubectl`.
- NGINX CRDs: Ensure the NGINX Ingress Controller (k8s.nginx.org) CRDs are installed before applying `VirtualServer` or `VirtualServerRoute` resources.

## Cleanup

```bash
# Helm
helm uninstall myapp -n demo

# Kustomize (delete applied resources)
kubectl delete -k /workspace/kustomize-cdng/overlays/dev

# Microservices demo
kubectl delete -f /workspace/k8s/microservice-demo.yaml

# Job
kubectl delete -f /workspace/jobs/pi.yaml
```

## Maintainer

Rohan Gupta (Team: ACM)
