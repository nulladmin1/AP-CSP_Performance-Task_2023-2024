import pandas as pd
import urllib.request
import os
from rich.console import Console
from rich.table import Table

commands = {
    'Exit': 'Exit the program.',
    'Help': 'Print all available commands.',
    'Stats': 'Prints stats from the PokeDex',
}

opts = {
    'dex_url': 'https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon.csv',
    'filename': 'pokedex',
    'default_filename': 'pokedex',
    'dex_keyword': 'pokedex',
}

extra_vars = {
    'exit_print': 'Exiting the program...',
    'error_print': '[red]Not an optional listed.[/] Please try again.'
}

console = Console()


def download_dex(url=opts.get('dex_url'), fn=opts.get('default_filename')):
    if url == opts.get('dex_url'):
        console.print(
            'Credit to [cyan]veekun[/] for the [red]PokeDex .csv dataset[/].\nPulling .csv [red]PokeDex file[/] from[cyan]: ' + url + '[/]...')
    else:
        console.print('Pulling custom .csv [red]Pokedex file from: ' + url + '...')
    urllib.request.urlretrieve(url, fn + '.csv')
    console.print('[cyan]Done[/] downloading the PokeDex .csv file.  ')


def detect_dex(dexes):
    dex_select = Table()

    if len(dexes) == 0:
        dex_select.add_column('Options')
        dex_select.add_row("[red]1.[/] Download PokeDex from Internet ([cyan]veekun[/]'s PokeDex)")
        dex_select.add_row('[red]2.[/] Download custom PokeDex from Internet')
        dex_select.add_row('[red]3.[/] Exit program')

        while True:
            console.print(f'No existing PokeDexes detected.')
            console.print(dex_select)
            x = console.input('Type the [cyan]number[/] of which option should be selected: ')

            if x == '1':
                download_dex()
                return 'default'
            elif x == '2':
                custom_url = console.input('Type the [cyan]url[/] of the [red]PokeDex[/]: ')
                custom_fn = console.input(
                    'Type the [cyan]filename[/] of the [red]PokeDex[/]. Type "default" if default filename should be used (pokedex)').lower()
                if custom_fn == 'default':
                    download_dex(custom_url)
                    return 'default'
                else:
                    download_dex(custom_url, custom_fn)
                    return custom_fn
            elif x == '3':
                console.print(extra_vars['exit_print'])
                quit()
            else:
                console.print(extra_vars['error_print'])
    elif len(dexes) == 1:
        console.print('[red]PokeDex[/] already detected.')
        return dexes[0]
    else:
        console.print('Multiple PokeDexes detected. Please select one: ')

        multiple_dex_select = Table()
        multiple_dex_select.add_column('Detected dexes')
        multiple_dex_select.add_row('1. (Exit)')

        dexes_dict = dict()

        for dexes_select_key in range(len(dexes)):
            dexes_select_value = dexes[dexes_select_key]
            dexes_select_key += 2

            dexes_dict[dexes_select_key] = dexes_select_value

            row_dexes_select = str('[red]' + str(dexes_select_key) + '.[/] ' + dexes_select_value)
            multiple_dex_select.add_row(row_dexes_select)

        console.print(multiple_dex_select)
        while True:
            x = console.input('Type the [cyan]number[/] of which option should be selected: ')
            try:
                x = int(x)
                if x > 1:
                    filename = dexes_dict[x]
                    break
                else:
                    console.print(extra_vars['exit_print'])
                    quit()

            except (ValueError, KeyError):
                console.print(extra_vars['error_print'])

        filename = dexes_dict[x]

        return filename


commands_table_dict = Table(title='Available Commands')
commands_table_dict.add_column('Commands', style='red')
commands_table_dict.add_column('Description', style='cyan')

commands_table = Table()
commands_table.add_column('Commands', style='red')

n = 1

for key, value in commands.items():
    commands_table_dict.add_row(key, value)
    row = '[red]' + str(n) + '.[/] ' + key
    commands_table.add_row(row)
    n = n + 1

console.print('Welcome to the [red]Python PokeDex CLI App[/], coded by [cyan]Shrey Deogade[/]', style='bold')

df = detect_dex(
    [i for i in filter(lambda var: True if opts.get('dex_keyword') in var and '.csv' in var else False, os.listdir())])

if df == 'default':
    file = 'pokedex.csv'
else:
    file = df

dex = pd.read_csv(file)

while True:  # Main Loop
    console.print(commands_table)
    i = console.input('Type the [cyan]number[/] of which command should be executed: ')
    if i == '1':  # Exit
        break
    elif i == '2':  # Help
        console.print(commands_table_dict)
    else:
        console.print('Invalid command', style='bold red')

console.print('Thank you for using the [red]Python PokeDex CLI App.')
