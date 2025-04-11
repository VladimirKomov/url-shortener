# 📦 Kubernetes Deployment for URL Shortener

This directory contains Kubernetes manifests for deploying the `shortener-service` and `url-validator` microservices of the URL Shortener project.

---

## 🗂 Structure

```
k8s/
├── shortener/
│   ├── configmap.yaml        # Environment variables
│   ├── deployment.yaml       # Deployment spec
│   ├── secret.yaml           # Secrets like DB password
│   └── service.yaml          # Exposes the service via NodePort or ClusterIP
├── url-validator/
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── secret.yaml
│   └── service.yaml          # Optional; not required unless external access needed
```

---

## 🚀 How to Deploy

### 1. ✅ Deploy `shortener-service`

```bash
kubectl apply -f shortener/secret.yaml
kubectl apply -f shortener/configmap.yaml
kubectl apply -f shortener/deployment.yaml
kubectl apply -f shortener/service.yaml
```

### 2. ✅ Deploy `url-validator`

```bash
kubectl apply -f url-validator/secret.yaml
kubectl apply -f url-validator/configmap.yaml
kubectl apply -f url-validator/deployment.yaml
```

---

## 🌍 Accessing the API

If using **NodePort** (e.g. `30080`), access the API like this:

```
http://localhost:30080/api/v1
```

If using **Ingress** (e.g. with `shortener.local`):

```
http://shortener.local/api/v1
```

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

- `BASE_URL` should match the external access URL, e.g. `http://localhost:30080/api/v1`
- Redis, PostgreSQL, MongoDB, Kafka are currently expected to run **externally in Docker**
- Kafka address should be reachable via `host.docker.internal` from inside the cluster
- `shortened_urls` table must exist in PostgreSQL (use Alembic or manual SQL if needed)

---

## ✨ Next steps (optional ideas)

- Add Ingress with domain routing
- Helm chart for reusable deployment
- HorizontalPodAutoscaler for auto-scaling
- CI/CD for automated rollout

---

Happy shipping 🚀
