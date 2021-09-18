Dawa Sasa
=====
[Dawa Sasa Prod Site](https://dawasasa.co.ke/)


### Docker quick start

Fastest way to get Shuup up and running is to use [Docker](https://www.docker.com).

1. Add your env file based on the sample in `env.example` 
2. Run:
```shell
docker-compose up --build 
```
3. Open [localhost:8001/sa](http://localhost:8001/sa) in a browser,
   log in with username: ``admin`` password: ``admin``
   
### Local Set up
[Shuup Set up Docs](http://shuup.readthedocs.io/en/latest/howto/getting_started.html).

### Documentation

Shuup documentation is available online at [Read the Docs](http://shuup.readthedocs.org/).

Documentation is built with [Sphinx](http://sphinx-doc.org/).

Issue the following commands to build the documentation:

```shell
pip install -r requirements-doc.txt
cd doc && make html
```

To update the API documentation rst files, e.g. after adding new
modules, use command:

```shell
./generate_apidoc.py
```

Additional Material
-------------------

1. [Django-project template](https://github.com/shuup/shuup-project-template).

2. [Provides system](https://shuup.readthedocs.io/en/latest/ref/provides.html).

3. [Core settings](https://shuup.readthedocs.io/en/latest/api/shuup.core.html#module-shuup.core.settings).

4. [Front settings](https://shuup.readthedocs.io/en/latest/api/shuup.front.html#module-shuup.front.settings).

5. [Admin settings](https://shuup.readthedocs.io/en/latest/api/shuup.admin.html#module-shuup.admin.settings).

6. [Extending Shuup](https://shuup.readthedocs.io/en/latest/#extending-shuup).



### Common Commands

1. Install postgres in Mac

```shell
LDFLAGS="-I/opt/homebrew/opt/openssl@1.1/include -L/opt/homebrew/opt/openssl@1.1/lib" pip install psycopg2
```
2. Generate static resources
```shell
python3 setup.py build_resources
```
3. Use the Django Shell
```shell
python3 -m shuup_workbench shell
```
4. Load initial data
```shell
python3 -m shuup_workbench shuup_init
```
