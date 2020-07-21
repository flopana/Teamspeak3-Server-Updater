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


def main():
    """
    Main function of the script
    :return:
    """
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
    URL = 'https://files.teamspeak-services.com/releases/server/'
    page = requests.get(URL)
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
        if vcmp(str(currentdb_ver), str(latest_ver)) is False:
            print("Last inserted version in db is already newest ts3 server version")
            exit(0)
        else:
            if VERBOSE:
                print("Last inserted version in db is older than latest available so updating")

    print("Shutting down teamspeak")
    os.system("../teamspeak3-server_linux_amd64/ts3server_startscript.sh stop")

    if VERBOSE is False:
        print("Updating Teamspeak")

    URL_TAR = URL + latest_ver + "/teamspeak3-server_linux_amd64-" + latest_ver + ".tar.bz2"

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
    os.system("../teamspeak3-server_linux_amd64/ts3server_startscript.sh start")

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
        print("\nSQL Query: " + Fore.YELLOW + " " + sql + Style.RESET_ALL)
        print("\nFinished inserting")
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


if __name__ == '__main__':
    init()
    print(Fore.GREEN + "##########################################\n"
          "# flopana's Teamspeak3 Server Updater    #\n"
          "##########################################")

    print(Style.RESET_ALL)
    for i in range(len(sys.argv)):
        if sys.argv[i] == "-v":
            VERBOSE = True

    main()