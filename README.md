# VidalCasino 2.0 - Estadísticas Service

Este repositorio contiene el microservicio **estadisticas-service** del proyecto **VidalCasino 2.0**, desarrollado para la evaluación EP3 de Introducción a Herramientas DevOps. Este servicio proporciona métricas, indicadores (KPIs) y estadísticas del casino mediante consultas de solo lectura sobre la base de datos compartida.

---

# Descripción general

**estadisticas-service** permite consultar información estadística tanto de los usuarios como del sistema completo, entregando métricas sobre apuestas, transacciones, usuarios registrados y ganancias del casino.

El microservicio se ejecuta dentro del clúster de **Amazon EKS** y se expone únicamente como servicio interno mediante **ClusterIP**.

El frontend consume este servicio a través de las rutas **/api/estadisticas**, sin exponer el microservicio directamente a Internet.

---

# Arquitectura del sistema

El sistema **VidalCasino 2.0** está compuesto por los siguientes servicios:

- casino-frontend: interfaz web pública mediante LoadBalancer.
- casino-backend: backend principal encargado de la autenticación y lógica del negocio.
- bonos-service: gestión de bonos y promociones.
- apuestas-service: administración de eventos deportivos y apuestas.
- estadisticas-service: generación de estadísticas y dashboards.
- postgres: base de datos compartida.

---

# Tecnologías utilizadas

- Python
- FastAPI
- PostgreSQL
- Docker
- Kubernetes
- Amazon EKS
- Amazon ECR
- GitHub Actions
- Horizontal Pod Autoscaler (HPA)
- AWS Academy Learner Lab

---

# Endpoints disponibles

| Método | Endpoint | Descripción |
|---------|----------|-------------|
| GET | /api/estadisticas/mias | Obtiene las estadísticas del usuario autenticado. |
| GET | /api/estadisticas/globales | Obtiene estadísticas generales del casino. |

La autenticación se realiza mediante el mismo **JWT_SECRET** utilizado por **casino-backend**, validando el token antes de responder las consultas.

---

# Endpoints de salud

El servicio incorpora sondas de salud para Kubernetes:

- /livez
- /readyz

**/livez**

Verifica que el proceso de FastAPI continúa ejecutándose correctamente.

**/readyz**

Comprueba que el servicio se encuentra listo para recibir tráfico y que existe conectividad con la base de datos PostgreSQL.

---

# Despliegue en Kubernetes

Los manifiestos del servicio se encuentran en:

```
k8s/
```

Archivos principales:

```
k8s/deployment.yaml
k8s/service.yaml
k8s/hpa.yaml
```

El servicio se despliega con **2 réplicas** y se expone internamente mediante un **Service de tipo ClusterIP** en el puerto **8006**.

Además, incorpora un **Horizontal Pod Autoscaler (HPA)** que incrementa o reduce automáticamente la cantidad de Pods según la utilización de CPU.

---

# CI/CD

El despliegue automático se encuentra definido en:

```
.github/workflows/deploy.yml
```

El workflow se ejecuta al realizar un **push** sobre la rama **deploy**.

El pipeline realiza las siguientes tareas:

- Descarga del código fuente.
- Configuración de credenciales de AWS Academy.
- Inicio de sesión en Amazon ECR.
- Construcción de la imagen Docker.
- Publicación de la imagen con los tags **latest**, **v1.0.1** y el SHA del commit.
- Conexión al clúster de Amazon EKS.
- Actualización del Deployment.
- Verificación del rollout.
- Validación del estado de los Pods.

---

# Ejecución local

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activarlo:

Linux/Mac

```bash
source .venv/bin/activate
```

Windows

```powershell
.venv\Scripts\activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Configurar las variables de entorno copiando:

```
.env.example
```

como

```
.env
```

---


# Comandos de verificación

```bash
kubectl get deployment estadisticas-service

kubectl get svc estadisticas-service

kubectl get hpa estadisticas-service-hpa

kubectl get pods -l app=estadisticas-service -o wide

kubectl describe deployment estadisticas-service
```

---

# Estado esperado

- Deployment disponible con 2 réplicas.
- Service interno de tipo ClusterIP.
- Horizontal Pod Autoscaler activo.
- Pods en estado Running.
- Imagen desplegada desde Amazon ECR.
- Pipeline de GitHub Actions ejecutado correctamente.
- Servicio respondiendo correctamente a las rutas `/livez`, `/readyz`, `/api/estadisticas/mias` y `/api/estadisticas/globales`.
