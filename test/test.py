from kubernetes import client, config

# Load kubeconfig
config.load_kube_config()

# Initialize API client
v1 = client.AppsV1Api()

# Namespace and Deployment name
deployment_name = "flask-app-flask-chart"
namespace = "default"

# Fetch Deployment
deployment = v1.read_namespaced_deployment(name=deployment_name, namespace=namespace)

# Check Readiness and Liveness Probes, Resource Requests and Limits
containers = deployment.spec.template.spec.containers
for container in containers:
    readiness_probe = container.readiness_probe
    print (readiness_probe)
    liveness_probe = container.liveness_probe
    print (liveness_probe)    
    resources = container.resources
    print(resources)

    if not readiness_probe:
        raise ValueError(f"Missing readiness probes in container {container.name}")
    
    if not liveness_probe:
        raise ValueError(f"Missing readiness probes in container {container.name}")

    if not resources.requests and not resources.limits:
        raise ValueError(f"Missing resource requests/limits in container {container.name}")

# Print Deployment YAML
#print(deployment)
