# ☸️ Kubernetes Deployment for URL Shortener Project

This directory contains Kubernetes manifests for deploying all core services of the URL Shortener system, including:
- `shortener-service` (FastAPI)
- `url-validator` (Safe Browsing via Kafka)
- `redis` (in-cluster cache)
---

## 📂 Structure

```
k8s/
├── redis/
│   ├── deployment.yaml       # Redis pod with password support
│   ├── secret.yaml           # Redis password secret
│   └── service.yaml          # Internal Redis service 
├── shortener/
│   ├── configmap.yaml        # Environment variables
│   ├── deployment.yaml       # Deployment spec
│   ├── secret.yaml           # Secrets like DB password
│   ├── service.yaml          # Exposes the service via NodePort or ClusterIP
│   └── ingress.yaml          # Ingress definition for /api/v1 routing
├── url-validator/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── secret.yaml
│   └── service.yaml          # Optional; not required unless external access needed
├── Makefile                  # Deployment automation
└── README_k8s.md # This file
```

---

## 🚀 How to Deploy

### 1. ✅ Deploy Redis

```bash

kubectl apply -f redis/
```

### 2. ✅ Deploy `shortener-service`

```bash

kubectl apply -f shortener/
```

### 3. ✅ Deploy `url-validator`

```bash

kubectl apply -f url-validator/
```
Or run everything at once:
```bash

make -C k8s all
```
---

## 🌍 Accessing the API

### If using **NodePort** (e.g. `30080`)

```
http://localhost:30080/api/v1
```

### If using **Ingress** with domain-based routing

```plaintext
http://shortener.local/api/v1
```

➡️ Add `127.0.0.1 shortener.local` to your `/etc/hosts` or `C:\Windows\System32\drivers\etc\hosts`.

---

## 🎯 Advanced Ingress Example (versioned APIs)

You can route different versions of your API to different deployments:

```yaml
rules:
  - host: shortener.local
    http:
      paths:
        - path: /api/v1
          pathType: Prefix
          backend:
            service:
              name: shortener-service
              port:
                number: 8000
        - path: /api/v2
          pathType: Prefix
          backend:
            service:
              name: shortener-v2-service
              port:
                number: 8000
```

This allows full separation between versions while using the same domain.

---

## 🔁 Restart deployments (after config/image updates)

```bash
kubectl rollout restart deployment shortener-service
kubectl rollout restart deployment url-validator
```

---

## 📊 Check status & logs

```bash
kubectl get pods
kubectl logs deployment/shortener-service
kubectl logs deployment/url-validator
```

---

## 🧠 Notes

- `BASE_URL` in config should match how your app is accessed externally
- `root_path` in FastAPI should match ingress path (e.g. `/api/v1`)
- Kafka, Redis, PostgreSQL, and MongoDB are expected to run externally in Docker
- Kafka URL must resolve from inside the cluster (e.g. `host.docker.internal`)
- `shortened_urls` table must be present in PostgreSQL

---

## ✨ Next steps (optional ideas)

- Add TLS via `cert-manager` + Ingress annotations
- Add a second Ingress for `url-validator` if it becomes HTTP-facing
- Create a Helm chart to template deployments
- Configure HPA (HorizontalPodAutoscaler)
- Add CI/CD pipeline for automatic Docker push & deploy

---

