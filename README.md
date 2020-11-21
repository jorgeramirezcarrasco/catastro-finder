# Catastro Finder

Unofficial Catastro Finder. No API keys required

---

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
from catastro_finder.catastro_finder import CatastroFinder
catastro = CatastroFinder()
```

Get provinces

```bash
provincias = catastro.get_provincias()
# Select one
selected_provincia = provincias[30]
```

Get municipalities

```bash
municipios = catastro.get_municipios(selected_provincia['Codigo'])
# Select one
selected_municipio = municipios[68]
```

Get streets candidates

```bash
via_result = catastro.get_vias(selected_provincia['Codigo'],selected_municipio['Codigo'],"JACINTO")[0]
```

Search a property

```bash
# Choose property number
via_numero = 2
inmueble_results = catastro.search_inmueble(via_result,via_numero,selected_provincia,selected_municipio)
```

## Usage with Zappa as server-less, event-driven python application

Remember to have the credentials in ~/.aws/credentials

Deploy

```bash
zappa deploy dev
```

Update

```bash
zappa update dev
```

Delete

```bash
zappa undeploy dev
```
