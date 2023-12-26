import urllib.request
import pandas as pd
import os

print('Welcome to python-pokedex')
x = True

opts = {
    'dex_url': 'https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon.csv',
    'drop_extra_columns': True,
    'filename': 'pokedex.csv',
    'dex_keyword': 'pokedex',
    'prompt': 'python-pokedex:'
}

opts_original = opts.copy()

commands = {
    'exit': 'Exit the program.',
    'help': 'Print all available commands.',
    'pull-dex': 'Pull PokeDex from the internet',
    'change_opts': 'Change opts: Type opts that needs to be changed and type new value after.',
    'list_opts': 'Lists all the available options'
}

print('Type help for help. ')

while x:
    i = input(opts.get('prompt') + '~> ')  # Prompt
    if i == 'exit':  # Exits program
        break

    elif i == 'help':  # Gets help
        print('Welcome to python-pokedex. This is an implementation of the Pokemon PokeDex in Python, with many '
              'commands for specific tasks, like only using 1 generation\'s PokeDex, or the Global PokeDex. The '
              'PokeDex\'s are stored in .csv files that contain their pokemon\'s name, type, and its stats. The '
              'available commands to the program are: \n')
        for key, value in commands.items():
            print(key, '- ', value)

    elif i == 'pull-dex':  # Pull Pokédex
        url = opts.get('dex_url')
        filename = opts.get('filename')
        print('Credit to veekun for the PokeDex .csv dataset.\n Pulling .csv PokeDex file from: ', url, '...')
        urllib.request.urlretrieve(url, 'pokedex1.csv')

        if url == 'https://raw.githubusercontent.com/veekun/pokedex/master/pokedex/data/csv/pokemon.csv' and opts.get(
                "drop_extra_columns") is True:
            df = pd.read_csv('pokedex1.csv')
            df = df.drop(columns=['Ability I', 'Ability II', 'Hidden Ability', 'EV Worth', 'Gender', 'Egg Group I',
                                  'Egg Group II'])
            df.to_csv(filename)
        print("Done downloading the file.")

    elif i == 'list_opts':
        print(opts)

    elif i == 'change_opts':  # Options change
        print('Usage: (command) (new value)')
        j = input('python-pokedex: change_set ~> ')
        j = j.split()
        j1 = j[0]
        j2 = j[1]
        opts[j1] = j2

    elif i == 'dex':  # Dex Mode
        def is_dex(var):
            if opts.get('dex_keyword') in var and '.csv' in var:
                return True
            else:
                return False


        print('\n')

        dexes_filter = filter(is_dex, os.listdir())
        n = 1
        dexes = {}
        for i in dexes_filter:
            print(n, '. ', i)
            dexes[n] = i
            n = n + 1
        try:
            dex_num = int(input('Please type the corresponding number to the dex to be used: '))
        except:
            print('Not an option listed. ')
        else:
            dex_s = dexes[dex_num]
            print('Dex "', dex_s, '" is being be used. ')
            dex = pd.read_csv(dex_s)
            y = True
            print('Type help for help. \n')
            while y:
                j = input(opts.get('prompt') + ' dex_mode: ' + dex_s + ' ~> ')

                if 'head' in j:
                    j_split = j.split(' ')
                    print(dex.head(int(j_split[1])))

                elif 'list' in j:
                    if 'columns' in j:
                        print(dex.columns)
                    elif 'column' in j:
                        if len(j.split(' ')) == 3:
                            print(dex[j.split(' ')[2]])
                        elif len(j.split(' ')) == 4:
                            print(dex[j.split(' ')][0:int(j.split(' '))])

    elif i == 'reset_opts':  # Reset options
        opts = opts_original.copy()
        print('Successfully reset the options to original.')

    else:  # If user types wrong command
        print('Unsupported command. Please type "help" for a list of commands.')
