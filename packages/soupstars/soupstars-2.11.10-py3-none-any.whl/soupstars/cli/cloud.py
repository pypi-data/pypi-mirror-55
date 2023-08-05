import click
import os
import sys
import textwrap
import getpass

from .printers import jsonify, pythonify
from ..config import Config
from ..resources import UsersResource, StatusResource, AuthResource, ParsersResource, ProfileResource


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
    jsonify(resp.json())


# TODO
# @cloud.command()
@click.option('--module', '-m', required=True, help="Name of the parser to push")
@click.pass_obj
def push(client, module):
    """
    Push a parser to SoupStars cloud
    """

    parsers = ParsersResource(config=config)
    jsonify(resp.json())


# TODO: update the api to allow pulling a parse by name
# @cloud.command()
@click.option('--module', '-m', required=True, help="Name of the parser to pull")
@click.pass_obj
def pull(client, module):
    """
    Pull a parser from SoupStars cloud into a local module
    """

    resp = client.pull(module)
    data = resp.json()
    with open(data['parser']['name'], 'w') as o:
        o.write(data['module'])
    jsonify({"state": "done", "response": data})


# TODO
# @cloud.command()
@click.option('--module', '-m', required=True, help="Name of the parser to create")
@click.pass_obj
def run(client, module):
    """
    Run a parser on SoupStars cloud
    """

    resp = client.run(module)
    jsonify(resp.json())


# TODO
# @cloud.command()
@click.option('--module', '-m', required=True, help="Name of the parser to show")
@click.option('--json/--no-json', default=False, help="Show parser details in JSON")
@click.pass_obj
def show(client, module, json):
    """
    Show the contents of a parser on SoupStars cloud
    """

    resp = client.pull(module)

    if json:
        jsonify(resp.json())
    else:
        pythonify(resp.json()['module'])


# TODO
# @cloud.command()
@click.option('--module', '-m', required=True, help="Name of the parser to test")
@click.pass_obj
def results(client, module):
    """
    Print results of a parser
    """

    resp = client.results(module)
    jsonify(resp.json())
