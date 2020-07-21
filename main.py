import sqlite3
from sqlite3 import Error
import requests
from bs4 import BeautifulSoup
from version_shit import sort, vcmp
import tarfile
import os
import sys
from colorama import init, Fore, Style

VERBOSE = False
FORCE = False
ARCHITECTURE = None


def main():
    """
    Main function of the script
    :return:
    """

    global ARCHITECTURE, FORCE, VERBOSE

    if ARCHITECTURE is None:
        if VERBOSE:
            print("Detecting architecture:")

        result = os.popen('uname -m').read()
        if result == "x86_64\n":
            ARCHITECTURE = "amd64"
        else:
            ARCHITECTURE = "x86"

        if VERBOSE:
            print("Architecture detected: " + ARCHITECTURE + "\n")

    if VERBOSE:
        print("Creating connection to sqlite")
    conn = create_connection(r"db.sqlite3")

    currentdb_ver = get_last_version(conn)
    if VERBOSE:
        if get_last_version(conn) is None:
            print("Nothing found in the db so getting the newest version")
        else:
            print("Latest inserted version in db is: " + Fore.CYAN + currentdb_ver)
            print(Style.RESET_ALL)
    if VERBOSE:
        print("Getting all available versions from teamspeak.com")
    url = 'https://files.teamspeak-services.com/releases/server/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    versions = []
    for a in soup.find_all('a', href=True):
        versions.append(a['href'])
    versions = versions[1:len(versions) - 1]  # cut out first and last href
    sort(versions)
    latest_ver = str(versions[len(versions) - 1])
    if VERBOSE:
        print("Available versions are: " + Fore.CYAN + str(versions) + Style.RESET_ALL)
        print("Latest available version on teamspeak.com is: " + Fore.CYAN + latest_ver)
        print(Style.RESET_ALL)

    if currentdb_ver is not None:
        if vcmp(str(currentdb_ver), str(latest_ver)) is False and FORCE is False:
            print("Last inserted version in db is already newest ts3 server version.\n"
                  "You can use the -f option to force update.\n"
                  "For more information call the script with -h.")
            exit(0)
        else:
            if VERBOSE:
                print("Last inserted version in db is older than latest available so updating")

    print("Shutting down teamspeak")
    os.system("../teamspeak3-server_linux_" + ARCHITECTURE + "/ts3server_startscript.sh stop")

    print("\nUpdating Teamspeak")

    URL_TAR = url + latest_ver + "/teamspeak3-server_linux_" + ARCHITECTURE + "-" + latest_ver + ".tar.bz2"

    if VERBOSE:
        print("\nDownloading current version: " + URL_TAR)

    r = requests.get(URL_TAR)
    with open('../ts3.tar.bz2', 'wb') as f:
        f.write(r.content)

    if VERBOSE:
        print("Finished download now extracting")

    tar = tarfile.open("../ts3.tar.bz2", "r:bz2")
    tar.extractall("../")
    tar.close()

    if VERBOSE:
        print("Finished extracting")

    print("\nStarting teamspeak")
    os.system("../teamspeak3-server_linux_" + ARCHITECTURE + "/ts3server_startscript.sh start")

    insert_new_version(conn, currentdb_ver, latest_ver)

    print(Fore.GREEN + "\nFinished thank you for using my script!" + Style.RESET_ALL)


def create_connection(db_file):
    """ create a database connection to the SQLite database
    specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        if conn is not None:
            sql = """
            CREATE TABLE IF NOT EXISTS versions (
                id integer PRIMARY KEY,
                old_version varchar,
                new_version varchar,
                updated_at timestamp default current_timestamp
            );
            """
            create_table(conn, sql)
        return conn
    except Error as e:
        print(e)

    exit(1)


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def get_last_version(conn):
    """
    Query last insereted new_version from versions table
    :param conn: the Connection object
    :return version: last inserted new version
    """
    cur = conn.cursor()
    cur.execute("SELECT new_version FROM versions order by id DESC")

    rows = cur.fetchall()

    for row in rows:
        return row[0]


def insert_new_version(conn, oldver, newver):
    """
    Create a new row in versions
    :param conn:
    :param oldver:
    :param newver:
    :return:
    """

    if VERBOSE:
        print("\nNow inserting new data into the Database")

    sql = '''INSERT INTO versions(old_version,new_version)VALUES('{}','{}')'''.format(oldver, newver)
    if oldver is None:
        if VERBOSE:
            print("No old_version was found in the database so inserting: " + Fore.CYAN + " NULL " + Style.RESET_ALL)
        sql = '''INSERT INTO versions(old_version,new_version)VALUES(NULL,'{}')'''.format(newver)
    if VERBOSE:
        print("SQL Query: " + Fore.YELLOW + " " + sql + Style.RESET_ALL)
        print("\nFinished inserting")
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


if __name__ == '__main__':
    init()
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-h" or sys.argv[i] == "--help":
            print(Fore.CYAN + "A Python 3 script used for updating a Teamspeak3 Server\n\n" + Style.RESET_ALL +
                  "usage: python3 main.py -h | -v | -f\n"
                  "usage: python3 main.py -a [amd64 or x86]\n"
                  "Options:\n"
                  "  -h, --help                              Displays this message\n"
                  "  -v, --verbose                           Prints verbose output\n"
                  "  -f, --force                             Forces an update\n"
                  "  -a, --architecture                      Lets you define the architecure")
            exit(0)
        if sys.argv[i] == "-v" or sys.argv[i] == "--verbose":
            VERBOSE = True
        if sys.argv[i] == "-f" or sys.argv[i] == "--force":
            FORCE = True
        if sys.argv[i] == "-a" or sys.argv[i] == "--architecture":
            if sys.argv[i+1] == "amd64":
                ARCHITECTURE = "amd64"
            elif sys.argv[i+1] == "x86":
                ARCHITECTURE = "x86"
            else:
                print(Fore.RED + "Error:\n"
                                 "" + Style.RESET_ALL + "Unsupported architecture please look up the usage.")
                exit(1)

    print(Fore.GREEN + "########################################################\n"
                       "# flopana's Teamspeak3 Server Updater                  #\n"
                       "# for more information and suggestions go on           #\n"
                       "# https://github.com/flopana/Teamspeak3-Server-Updater #\n"
                       "########################################################\n" + Style.RESET_ALL)

    main()
