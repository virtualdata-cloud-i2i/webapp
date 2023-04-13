## Example 1: web application

Hosting web applications is a common case for clouds. Connect to your VM, and clone the repository containing a simple web application:

```bash
git clone git@github.com:virtualdata-cloud-i2i/webapp.git
```

Enter the repository, and execute:

```bash
cd /path/to/virtualdata
python3 index.py
```

And follow instructions. This application is based on [Dash](https://dash.plotly.com) which makes the server deployment super easy.

### Troubleshooting

If `mylib` is missing, simply install it on your VM by cloning the repository:

```bash
git clone git@github.com:virtualdata-cloud-i2i/myapp.git
```

and executing:

```bash
cd myapp
pip install .
```