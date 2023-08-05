"""
Command line reference manager with a single source of truth: the .bib file.
Inspired by beets.
"""

import os
import pkg_resources
import sys

import click
import click_plugins
import pybibs
import pyperclip

from . import cite
from . import internals
from . import query

PATH_OPTION = click.Path(writable=True, readable=True, dir_okay=False)
FILE_OPTION = click.option(
    '--file',
    help='File to link to this entry.',
    type=click.Path(exists=True, readable=True, dir_okay=False),
)
DESTINATION_OPTION = click.option(
    '--destination',
    help='A folder to put the file in.',
    type=click.Path(exists=True, readable=True, dir_okay=True, file_okay=False),
)
SEARCH_TERMS_OPTION = click.argument(
    'search_terms',
    nargs=-1,
    autocompletion=internals.complete_key,
)


@click_plugins.with_plugins(pkg_resources.iter_entry_points('bibo.plugins'))
@click.group(help=__doc__)
@click.version_option()
@click.option('--database', envvar=internals.BIBO_DATABASE_ENV_VAR,
              help='A .bib file.', required=True, type=PATH_OPTION)
@click.pass_context
def cli(ctx, database):
    ctx.ensure_object(dict)
    ctx.obj['database'] = os.path.abspath(database)
    ctx.obj['data'] = internals.load_database(database)


@cli.command('list', short_help='List entries.')
@click.option('--raw', is_flag=True, help='Format as raw .bib entries')
@click.option('--bibstyle', default='plain', help='Citation format')
@click.option('--verbose', is_flag=True, help='Print verbose information')
@SEARCH_TERMS_OPTION
@click.pass_context
def list_(ctx, search_terms, raw, bibstyle, verbose):
    entries = query.search(ctx.obj['data'], search_terms)
    if raw:
        _list_raw(entries)
    else:
        _list_citations(entries, ctx.obj['database'], bibstyle, verbose)


def _list_raw(entries):
    for entry in entries:
        click.echo(pybibs.write_string([entry]))


def _list_citations(entries, database, bibstyle, verbose):
    entries = [e for e in entries if e['type'] != 'string']
    keys = [e['key'] for e in entries]
    exception = None
    try:
        citations = cite.cite(keys, database, bibstyle, verbose)
    except cite.BibtexException as e:
        exception = e

    for entry in entries:
        parts = [
            internals.header(entry),
            cite.fallback(entry) if exception else citations[entry['key']],
        ]
        click.echo('\n'.join(parts))

    if exception is not None:
        parts = [str(exception), 'Using a fallback citation method']
        if exception.use_verbose:
            parts.append('Use --verbose for more information')
        click.secho('. '.join(parts), fg='red')


@cli.command('open', short_help='Open the file linked to an entry.')
@SEARCH_TERMS_OPTION
@click.pass_context
def open_(ctx, search_terms):
    entry = query.get(ctx.obj['data'], search_terms)

    file_field = entry.get('fields', {}).get('file')
    if not file_field:
        click.echo('No file is associated with this entry')
        sys.exit(1)

    internals.open_file(file_field)


@cli.command(short_help='Add a new entry.')
@FILE_OPTION
@DESTINATION_OPTION
@click.pass_context
def add(ctx, destination, **kwargs):
    file_ = kwargs.pop('file')
    file_validation(file_, destination)

    data = ctx.obj['data']
    bib = internals.editor(text=pyperclip.paste())
    entry = pybibs.read_entry_string(bib)

    unique_key_validation(entry['key'], data)

    data.append(entry)

    if file_:
        internals.set_file(data, entry, file_, destination)

    pybibs.write_file(data, ctx.obj['database'])


@cli.command(short_help='Remove an entry or a field.')
@click.argument('key', autocompletion=internals.complete_key)
@click.argument('field', nargs=-1)
@click.pass_context
def remove(ctx, key, field):
    data = ctx.obj['data']
    entry = query.get_by_key(data, key)

    if not field:
        data.remove(entry)
    elif 'fields' in entry:
        for f in field:
            if f in entry['fields']:
                del entry['fields'][f]
            else:
                click.echo('"{}" has no field "{}"'.format(key, f))
    else:
        click.echo('"{}" has no fields'.format(key))

    pybibs.write_file(data, ctx.obj['database'])


@cli.command(short_help='Edit an entry.')
@click.argument('key', autocompletion=internals.complete_key)
@click.argument('field_value', nargs=-1)
@FILE_OPTION
@DESTINATION_OPTION
@click.pass_context
def edit(ctx, key, field_value, destination, **kwargs):
    '''
    FIELD_VALUE

    To set fields: author=Einstein tags=interesting.
    Leave the value empty to open in editor.
    Set the key / type in the same way.
    '''
    file_ = kwargs.pop('file')
    file_validation(file_, destination)

    data = ctx.obj['data']
    entry = query.get_by_key(data, key)

    if entry['type'] == 'string':
        raise click.ClickException('Editing @string entries is unsupported')

    if file_:
        internals.set_file(data, entry, file_, destination)
    for fv in field_value:
        if '=' in fv:
            field, value = fv.split('=')
        else:
            field = fv
            current_value = entry['fields'].get(field, '')
            value = internals.editor(text=current_value).strip()
        if field == 'key':
            unique_key_validation(value, data)
            entry['key'] = value
        elif field == 'type':
            entry['type'] = value
        else:
            entry['fields'][field] = value

    pybibs.write_file(data, ctx.obj['database'])


def file_validation(file_, destination):
    if destination and not file_:
        raise click.BadOptionUsage(
            'destination',
            'Specifying destination without a file is meaningless.',
        )


def unique_key_validation(new_key, data):
    if new_key in (e['key'] for e in data):
        raise click.ClickException('Duplicate key, command aborted')


if __name__ == '__main__':
    cli()
