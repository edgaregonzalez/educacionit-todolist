# educacionit-todolist

## Todolist Ezequiel:
* Proceso de build y push del chart.
* Vamos a deplegarlos de ArgoCD.
* El fin de semana voy el desafio de frontend.
* Dejar en Discord el link del repo.

## Todolist Alumnos:
* Hacer el fork del repo.
* Esten atentos al nuevo desafio.

## Instalacion del chart a partir de un repositorio remoto:

Para conectarse al repositorio de charts de lo que vimos en la clase de hoy deben ejecutar estos pasos:

1. Agregar el repositorio:
helm repo add educacionit-todolist https://edgaregonzalez.github.io/educacionit-todolist/helm/educacionit-todolist
2. actualizar los repo
helm repo update
3. Crear el namespace
helm create ns todolistrepo
4. Instalar el chart:
helm install todolist-repo educacionit-todolist/educacionit-todolist -n todolistrepo

Para corrobar que todo esta funcionando pueden revisar:
* el dashboard desde minikube dashboard
* pueden ejecutar los comandos de kubectl para ver el estado de la instalacion.