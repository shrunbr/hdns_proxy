import yaml
import dns.resolver
import requests
from flask import Flask, redirect, request, render_template, url_for    

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

@app.route("/", subdomain="<hnsdomain>", methods=['POST', 'GET'])
def hnsredirect(hnsdomain):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = nameservers
    try:
        answer = resolver.resolve(hnsdomain)
    except dns.resolver.NXDOMAIN:
        return render_template('non_existent_query.html', domain=hnsdomain, rootRedirect=rootRedirect)
    for a in answer:
        endpoint = a.to_text()
    headers = {'Host': hnsdomain}
    args = request.args.to_dict()
    url = f"http://{endpoint}"
    return requests.request('GET', url, headers=headers, allow_redirects=True, stream=True, params=args).content

@app.route("/<path:path>", subdomain="<hnsdomain>", methods=['POST', 'GET'])
def hnsredirect_path(hnsdomain, path):
    resolver = dns.resolver.Resolver()
    resolver.nameservers = nameservers
    try:
        answer = resolver.resolve(hnsdomain)
    except dns.resolver.NXDOMAIN:
        return render_template('non_existent_query.html', domain=hnsdomain, rootRedirect=rootRedirect)
    for a in answer:
        endpoint = a.to_text()
    headers = {'Host': hnsdomain}
    args = request.args.to_dict()
    url = f"http://{endpoint}/{path}"
    return requests.request('GET', url, headers=headers, allow_redirects=True, stream=True, params=args).content

if __name__ == '__main__':
    import fastwsgi
    fastwsgi.run(wsgi_app=app, host=bindAddress, port=port)