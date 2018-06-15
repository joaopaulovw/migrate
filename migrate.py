import json
import mysql.connector
import sys
from termcolor import colored


def migrate(db_from, db_to):
    config = json.load(open('config.json'))
    tables = json.load(open(config['scheme']))

    config_db_from = config['connections'][db_from]
    config_db_to = config['connections'][db_to]

    from_db = config_db_from['database']
    to_db = config_db_to['database']

    answer = input('Are you sure you want to migrate data from "{}" to "{}"? [y/N] '
                   .format(from_db, to_db))

    if answer.lower() == 'y':
        print('{} {}'.format(colored('>', 'blue'), 'migrate'))
        print()

        try:
            for table in tables:
                print('{}... {}'.format(table['table'], 'migrating'))

                con = mysql.connector.connect(**config_db_from)
                cursor = con.cursor()

                columns = ''

                for column in table['columns']:
                    columns += '`' + column + '`, '

                columns = columns.strip(', ')

                query = 'SELECT {} FROM {}'.format(columns, table['table'])

                cursor.execute(query)

                con2 = mysql.connector.connect(**config_db_to)
                cursor2 = con2.cursor()

                count = 0

                for line in cursor:
                    v = ''

                    for l in line:
                        v += '%s, '

                    v = v.strip(', ')

                    insert = 'INSERT INTO {} ({}) VALUES ({})'.format(table['table'], columns, v)
                    cursor2.execute(insert, line)
                    count += 1

                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                print('{}... {}'.format(table['table'], 'done'))
                print('    {} line(s) insert(s)'.format(count))
                print()

                con2.commit()
                cursor2.close()
                con2.close()

                cursor.close()
                con.close()

        except Exception as e:
            print(colored('    error: {}'.format(str(e)), 'red'))
            print()

        print('finished')


def main(argv):
    f = None
    t = None

    for i in range(1, len(argv)):
        arg = argv[i]

        if arg in ('-f', '-t') and i == len(argv) - 1:
            print(colored('error: missing args', 'red'))
            sys.exit()
        elif arg == '-h':
            print('migrate -f <fromdb> -t <todb>')
            sys.exit()
        elif arg == "-f":
            f = argv[i + 1]
        elif arg == "-t":
            t = argv[i + 1]

    config = json.load(open('config.json'))

    if f not in config['connections']:
        print(colored('error: connection "{}" not found in config file'.format(f), 'red'))
        sys.exit()
    elif t not in config['connections']:
        print(colored('error: connection "{}" not found in config file'.format(t), 'red'))
        sys.exit()

    migrate(f, t)


if __name__ == '__main__':
    main(sys.argv)
