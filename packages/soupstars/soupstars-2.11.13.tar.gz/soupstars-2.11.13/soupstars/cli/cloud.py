import click
import os
import sys
import textwrap
import getpass
from importlib import import_module

from .printers import jsonify, pythonify, tableify
from ..config import Config
from ..resources import (
    UsersResource, StatusResource, AuthResource, ParsersResource,
    ProfileResource, RunsResource, ParserResource, ResultsResource,
    TopResource
)


@click.group()
@click.option('--token', '-t', help="Token to use. Default None")
@click.option('--host', '-h', default=None, help="Host to use")
@click.pass_context
def cloud(context, token, host):
    """
    Commands to interact with SoupStars cloud.
    """

    context.obj = Config(token=token, host=host)


@cloud.command()
@click.pass_obj
def health(config):
    """
    Print the status of the SoupStars api
    """

    status = StatusResource(config=config)
    resp = status.get()
    jsonify(resp.json())


@cloud.command()
@click.pass_obj
def register(config):
    """
    Register a new account on SoupStars cloud
    """

    email = input('Email: ')
    password = getpass.getpass(prompt='Password: ')
    password2 = getpass.getpass(prompt='Confirm password: ')

    if password != password2:
        print("Passwords did not match.")
        return

    users = UsersResource(config=config)
    resp = users.post(email=email, password=password)

    if resp.ok:
        auth = AuthResource(config=config)
        resp = auth.post(email=email, password=password)
        config.token = resp.json()['access_token']
        config.save()
    jsonify(resp.json())


@cloud.command()
@click.pass_obj
def login(config):
    """
    Log in with an existing email
    """

    email = input('Email: ')
    password = getpass.getpass(prompt='Password: ')
    auth = AuthResource(config=config)
    resp = auth.post(email=email, password=password)
    if resp.ok:
        config.token = resp.json()['access_token']
        config.save()

    jsonify(resp.json())


@cloud.command()
@click.pass_obj
def whoami(config):
    """
    Print the email address of the current user
    """

    profile = ProfileResource(config=config)
    resp = profile.get()
    if resp.ok:
        jsonify(resp.json().get('email'))
    else:
        jsonify(resp.json())


@cloud.command()
@click.pass_obj
def ls(config):
    """
    Show the parsers uploaded to SoupStars cloud
    """

    parsers = ParsersResource(config=config)
    resp = parsers.get()
    if resp.ok:
        headers = ['Name', 'Last updated']
        rows = [(p['name'], p['updated_at']) for p in resp.json()]
        tableify(headers, rows)
    else:
        jsonify(resp.json())



@cloud.command()
@click.argument('module')
@click.option('--name', '-n', help="Name of the crawler. If not given, uses the module's file name.")
@click.pass_obj
def push(config, module, name):
    """
    Push a parser to Soup Stars cloud. Must be an importable module, eg `myparser` or `examples.parsers.myparser`
    """

    parsers = ParsersResource(config=config)
    module = import_module(module)
    module_contents = open(module.__file__, 'r').read()
    name = name or module.__name__.split('.')[-1]
    parsers.post
    resp = parsers.post(name=name, module=module_contents)
    jsonify(resp.json())


@cloud.command()
@click.argument('name')
@click.option('--force', is_flag=True, default=False, help="Overwrite existing module if it exists")
@click.pass_obj
def pull(config, name, force):
    """
    Pull a parser from Soup Stars cloud into a local module.
    """

    parser = ParserResource(config=config, name=name)
    resp = parser.get()
    filename = resp.json()['name'] + '.py'
    module = resp.json()['module']
    if os.path.exists(filename) and not force:
        jsonify(f"{filename} already exists. Use --force to overwrite.")
    else:
        with open(filename, 'w') as o:
            o.write(module)
        jsonify(f"Finished writing module to {o.name}")


@cloud.command()
@click.argument('name')
@click.pass_obj
def run(config, name):
    """
    Run a parser on Soup Stars cloud
    """

    resp = RunsResource(config).post(parser_name=name)
    jsonify(resp.json())


@cloud.command()
@click.argument('name')
@click.pass_obj
def show(config, name):
    """
    Print the contents of a parser on Soup Stars cloud
    """

    parser = ParserResource(config=config, name=name)
    resp = parser.get()
    if resp.ok:
        pythonify(resp.json()['module'])
    else:
        jsonify(resp.json())


@cloud.command()
@click.pass_obj
def recent(config):
    """
    Print recent pages that have been parsed
    """

    results = ResultsResource(config=config)
    resp = results.get()
    if resp.ok:
        headers = ['Created', 'Status', 'URL']
        rows = [(r['created_at'], r['status_code'], r['url']) for r in resp.json()]
        tableify(headers, rows)
    else:
        jsonify(resp.json())


@cloud.command()
@click.pass_obj
def top(config):
    """
    Print recently active runs
    """

    top = TopResource(config=config)
    resp = top.get()
    if resp.ok:
        headers = ['Started', 'Parser', 'State']
        rows = []
        for r in resp.json():
            started = r['created_at']
            parser = r['parser']['name']
            if r['stopped_at']:
                state = "Finished"
            elif r['started_at']:
                state = "Running"
            elif not r.get('instance'):
                state = "Booting"
            else:
                state = "Received"
            rows.append([started, parser, state])
        tableify(headers, rows)
    else:
        jsonify(resp.json())
