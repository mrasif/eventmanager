# Deploy using kubernetes

- Update configmap and secrets with configuration details and secrets
- Update ingress host name as per your domain name
- Update deployment tag in `deployments.yaml`
- Run `kubectl create ns eventmanager`
- Run `kubectl apply -f configmap.yaml`
- Run `kubectl apply -f secret.yaml`
- Run `kubectl apply -f deployment.yaml`
- Run `kubectl apply -f service.yaml`
- Run `kubectl apply -f ingress.yaml`

Point your loadbalancer address to your DNS provider.