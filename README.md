# Evaluación de Plataforma de Registro de Pedidos en Kubernetes

Este repositorio contiene la implementación, orquestación y evaluación experimental de un sistema distribuido diseñado para la asignatura de Sistemas Operativos.

## 🏗️ Arquitectura del Sistema
El proyecto implementa una arquitectura de microservicios básica con separación de cómputo y estado:
- **API REST**: Desarrollada en Python utilizando FastAPI.
- **Capa de Persistencia**: PostgreSQL (imagen `15-alpine`).
- **Contenerización**: Docker.
- **Orquestación**: Kubernetes operando localmente mediante Minikube.
- **Herramienta de Inyección de Tráfico**: Grafana k6.

## 📁 Estructura del Repositorio
- `/app` - Código fuente de la API en Python y `Dockerfile`.
- `/db` - Scripts de inicialización SQL (`init.sql`).
- `/k8s` - Manifiestos declarativos de Kubernetes (`Deployment`, `Service`, `Secret`, `ConfigMap`).
- `/pruebas` - Scripts en JavaScript para pruebas de estrés y concurrencia.

## 🚀 Instrucciones de Despliegue (Entorno Local)

### 1. Prerrequisitos
- Docker Engine en ejecución.
- Minikube y `kubectl` instalados.

### 2. Inicialización del Clúster
```bash
minikube start --driver=docker# Proyecto de Sistemas Operativos - Sistema Distribuido 
