# Requirements

Dado el siguiente Sistema:

Una compañía aérea se dedica al negocio de transporte de cargas aéreas entre diferentes orígenes y destinos.

La compañía solo puede transportar paquetes de Clientes.

Por cada paquete transportado la compañía aérea cobra 10$

Debe existir un método que genere un reporte con el total de paquetes transportados y el total recaudado para un día determinado.

Se pide:

* Programar en Python las clases y responsabilidades del sistema, crear los testeos unitarios que consideren necesarios.

* No utilizar ningún framework en la solución (mantener una solución sencilla).

# Create virtual environment and install requirements
* python3 -m venv .venv
* source .venv/bin/activate
* pip install -r requirements.txt

# Run tests with coverage:
* pytest --cov=airline_packaging tests/