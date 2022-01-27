import yaml
import dns.resolver
import requests
from flask import Flask, redirect, jsonify

config = yaml.safe_load(open('config.yaml'))
secretKey = config['secretKey']
rootDomain = config['rootDomain']
bindAddress = config['bindAddress']
rootRedirect = config['rootRedirect']
port = config['port']
nameservers = config['nameservers']

app = Flask(__name__, subdomain_matching=True)
app.config.update(
    SERVER_NAME=f"{rootDomain}:{port}",
    SECRET_KEY=secretKey
)

@app.route("/")
def index():
    return redirect(rootRedirect)

@app.route("/", subdomain="<hnsdomain>")
def hnsredirect(hnsdomain):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = nameservers
    answer = resolver.resolve(hnsdomain)
    for a in answer:
        endpoint = a.to_text()
    headers = {'Host': hnsdomain}
    return requests.request('GET', "http://" + endpoint, headers=headers, allow_redirects=True, stream=True).content

if __name__ == '__main__':
    import fastwsgi
    fastwsgi.run(wsgi_app=app, host=bindAddress, port=port)