# ROSHAN RAJ
# roshar1@uci.edu
# 90439894

# admin.py

from Profile import Profile
import sys
from pathlib import Path
from Profile import Post
from ds_client import send


def list_f(directory):
    """
    List files in the specified directory.

    Args:
        directory (str): The directory path to list files from.

    Returns:
        None
    """
    try:
        directory_path = Path(directory)
        entries = list(directory_path.iterdir())

        entries = [item for item in entries if item.is_file()]
        for item in entries:
            print(str(item))

    except FileNotFoundError:
        print(f"{directory} doesn't exist. Enter a valid path!")


def list_s(directory, search_name):
    """
    List files in the specified directory.

    Args:
        directory (str): The directory path to list files from.
        search_name (str): The file name.

    Returns:
        None
    """
    try:
        directory_path = Path(directory)
        entries = list(directory_path.iterdir())

        entries = [item for item in entries if search_name in item.name]
        for item in entries:
            print(str(item))

    except FileNotFoundError:
        print(f"{directory} doesn't exist. Enter a valid path!")


def list_e(directory, file_extension):
    """
    List files in the specified directory.

    Args:
        directory (str): The directory path to list files from.
        file_extension (str): The file extension.

    Returns:
        None
    """
    try:
        directory_path = Path(directory)
        entries = list(directory_path.iterdir())

        entries = [item for item in entries if item.is_file() and item.suffix == f'.{file_extension}']
        for item in entries:
            print(str(item))

    except FileNotFoundError:
        print(f"{directory} doesn't exist. Enter a valid path!")


def list_r(directory):
    """
    List files in the specified directory and the files within the directories in the main directory.

    Args:
        directory (str): The directory path to list files from.

    Returns:
        None
    """
    try:
        directory_path = Path(directory)
        entries = list(directory_path.iterdir())

        entries = [item for item in entries if item.is_dir() or item.is_file()]
        entries.sort(key=lambda x: (x.is_dir(), x))
        for item in entries:
            if item.is_dir():
                print(str(item))
                list_r(item)
            if item.is_file():
                print(str(item))

    except FileNotFoundError:
        print(f"{directory} doesn't exist. Enter a valid path!")


def list_r_f(directory):
    """
    Recursively list all files in the specified directory and its subdirectories.

    Args:
        directory (str): The directory path to start listing files from.

    Returns:
        None
    """
    try:
        directory_path = Path(directory)
        entries = list(directory_path.iterdir())
        entries = [item for item in entries if item.is_dir() or item.is_file()]
        entries.sort(key=lambda x: (x.is_dir(), x))

        for item in entries:
            if item.is_file():
                print(str(item))
            if item.is_dir():
                list_r_f(item)

    except FileNotFoundError:
        print(f"{directory} doesn't exist. Enter a valid path!")

def list_r_e(directory, file_extension):
    """
    Recursively list all files with the specified extension in the specified directory and its subdirectories.

    Args:
        directory (str): The directory path to start listing files from.
        file_extension (str): The extension of files to be listed.

    Returns:
        None
    """
    try:
        directory_path = Path(directory)
        entries = list(directory_path.iterdir())

        entries = [item for item in entries if item.is_dir() or (item.is_file() and item.suffix == f'.{file_extension}')]
        entries.sort(key=lambda x: (x.is_dir(), x))

        for item in entries:
            if item.is_file():
                print(str(item))
            if item.is_dir():
                list_r_e(item, file_extension)
    except FileNotFoundError:
        print(f"{directory} doesn't exist. Enter a valid path!")

def list_r_s(directory, search_name):
    """
    Recursively list all files with the specified name in the specified directory and its subdirectories.

    Args:
        directory (str): The directory path to start listing files from.
        search_name (str): The name of files to be listed.

    Returns:
        None
    """
    try:
        directory_path = Path(directory)
        entries = list(directory_path.iterdir())

        entries = [item for item in entries if item.is_dir() or (item.is_file())]
        for item in entries:
            if item.is_file():
                if search_name in item.name:
                    print(str(item))
            if item.is_dir():
                list_r_s(item, search_name)

    except FileNotFoundError:
        print(f"{directory} doesn't exist. Enter a valid path!")

def list_l(directory):
    """
    List files and directories in the specified directory.

    Args:
        directory (str): The directory path to list files and directories from.

    Returns:
        None
    """
    try:
        directory_path = Path(directory)
        entries = list(directory_path.iterdir())

        entries.sort(key=lambda x: (x.is_dir(), x))
        for item in entries:
            print(str(item))

    except FileNotFoundError:
        print(f"{directory} doesn't exist. Enter a valid path!")


def delete_dsu_file(path):
    """
    Delete a .dsu file if it exists.

    Args:
        path (str): The path to the .dsu file to be deleted.

    Returns:
        None
    """
    try:
        if path.suffix == '.dsu' and path.is_file():
            path.unlink()
            print(f"{path} DELETED")
        else:
            print("ERROR")

    except Exception as e:
        print(f"Error deleting file: {e}")


def read_dsu_file(path):
    """
    Read the contents of a .dsu file.

    Args:
        path (str): The path to the .dsu file to be read.

    Returns:
        None
    """
    try:
        if path.suffix == '.dsu' and path.is_file():
            with open(path, 'r') as dsu_file:
                content = dsu_file.read()
                if not content.strip():
                    print("EMPTY")
                else:
                    content = content.strip()
                    print(content)
        else:
            print("ERROR")

    except Exception as e:
        print(f"Error reading file: {e}")


def create_new_file(path, filename):
    """
    Create a new .dsu file with the given filename.

    Args:
        path (str): The directory path where the .dsu file will be created.
        filename (str): The name of the new .dsu file.

    Returns:
        Profile: The profile object associated with the new .dsu file, if created successfully.
    """
    try:
        file_path = Path(path) / f"{filename}.dsu"

        if file_path.exists() and file_path.is_file():
            print(f"Loading existing file: {file_path}")
            profile = Profile()
            path1 = f"{path}/{filename}.dsu"
            profile.load_profile(path1)
            return profile

        with open(file_path, 'w'):
            pass
        print(f"{path}/{filename}.dsu created")

        username = input("Enter username: ")
        password = input("Enter password: ")
        bio = input("Enter bio: ")

        profile = Profile(dsuserver=None, username=username, password=password)
        profile.bio = bio
        file = f"{path}/{filename}.dsu"
        profile.save_profile(file)

        return profile

    except Exception as e:
        print(f"Error creating/loading file: {e}")
        return None


def load_file(directory_path):
    """
    Load a .dsu file and return the associated profile.

    Args:
        directory_path (str): The path to the .dsu file to be loaded.

    Returns:
        Profile: The profile object loaded from the .dsu file, if successful.
    """
    try:
        directory_path = Path(directory_path)
        if directory_path.suffix == '.dsu' and directory_path.is_file():
            print("Loaded the file!")
            profile = Profile()
            file = f"{directory_path}"
            profile.load_profile(file)
            return profile

        else:
            print("ERROR")
            return None

    except Exception as e:
        print(f"Error reading file: {e}")
        return None



def edit_file(profile: Profile, filepath, x=True):
    """
    Edit the content of a DSU file.

    Args:
        profile (Profile): The profile object associated with the DSU file.
        filepath (str): The path of the DSU file to be edited.
        x (bool, optional): Flag to control the loop. Defaults to True.

    Returns:
        None
    """
    try:
        while x:
            user_input = input("Edit the code (Q to exit): ")
            if user_input[0] == 'Q':
                break
            elif user_input[0] == 'E':
                options = user_input[1:].split()
                if '-usr' in options:
                    profile.username = options[options.index('-usr') + 1][1:-1]

                if '-pwd' in options:
                    profile.password = options[options.index('-pwd') + 1][1:-1]

                if '-bio' in options:
                    bio_index = options.index('-bio') + 1
                    bio_content = options[bio_index]
                    for i in range(bio_index + 1, len(options)):
                        bio_content += ' ' + options[i]
                        if '"' in options[i]:
                            break
                    profile.bio = bio_content[1:-1]

                if '-addpost' in options:
                    addpost_index = options.index('-addpost') + 1
                    addpost_content = options[addpost_index]
                    for i in range(addpost_index + 1, len(options)):
                        addpost_content += ' ' + options[i]
                        if '"' in options[i]:
                            break
                    post_online = input("Do you want to post this online? (y/n): ").lower()

                    if post_online == 'y':
                        try:
                            dsuserver = input("Enter the server address without quotation marks: ")
                            profile.dsuserver = dsuserver
                            print(profile.dsuserver)
                            port = 3021
                            username = profile.username
                            password = profile.password

                            if profile.bio is not None:
                                bio = profile.bio
                                send(dsuserver, port, username, password, addpost_content[1:-1], bio)
                            else:
                                send(dsuserver, port, username, password, addpost_content[1:-1])

                            print("Posted online successfully!")

                        except Exception as e:
                            print(f"Error: {e}")
                    elif post_online == 'n':
                        profile.dsuserver = None

                    profile.add_post(Post(entry=addpost_content[1:-1]))
                    profile.save_profile(filepath)
                    print("Post added successfully!")


                if '-delpost' in options:
                    post_id = int(options[options.index('-delpost') + 1])
                    profile.del_post(post_id - 1)

                profile.save_profile(filepath)

            elif user_input[0] == 'P':
                try:
                    options = user_input[1:].split()
                    if '-usr' in options:
                        print(f"Username: {profile.username}")
                    if '-pwd' in options:
                        print(f"Password: {profile.password}")
                    if '-bio' in options:
                        print(f"Bio: {profile.bio}")
                    if '-posts' in options:
                        print("Posts:")
                        for i, post in enumerate(profile._posts):
                            print(f"{i + 1} post: {post.entry}")
                    if '-post' in options:
                        post_id = int(options[options.index('-post') + 1])
                        if 1 <= post_id <= len(profile._posts):
                            print(f"Post {post_id}: {profile._posts[post_id - 1].entry}")
                        else:
                            print(f"Error: Invalid post ID {post_id}")
                    if '-all' in options:
                        print(f"Username: {profile.username}")
                        print(f"Password: {profile.password}")
                        print(f"Bio: {profile.bio}")
                        print("Posts:")
                        for i, post in enumerate(profile._posts):
                            print(f"{i + 1} post: {post.entry}")

                except Exception:
                    print(f"Error printing data.")

            else:
                print("Please create or open a DSU file before editing.")

    except Exception as e:
        print(f"Error editing DSU file: {e}")


def admin():
    """
    Main function for administrative tasks in PyJournal.

    Returns:
        None
    """

    while True:
        user_input = input()
        if user_input[0] == 'L':
            path = user_input[1:].split()[0]
            options = user_input[1:].split()[1:]
            if '-r' in options and '-f' in options and '-s' not in options and '-e' not in options:
                list_r_f(path)
            elif '-r' in options and '-s' in options and '-f' not in options and '-e' not in options:
                list_r_s(path, options[options.index('-s') + 1])
            elif '-r' in options and '-e' in options and '-s' not in options and '-f' not in options:
                list_r_e(path, options[options.index('-e') + 1].lstrip("."))
            elif not options:
                list_l(path)
            elif options[0] == '-r':
                list_r(path)
            elif options[0] == '-f':
                list_f(path)
            elif options[0] == '-s':
                list_s(path, options[options.index('-s') + 1])
            elif options[0] == '-e':
                list_e(path, options[options.index('-e') + 1].lstrip("."))
        elif user_input[0] == 'Q':
            sys.exit(0)
        elif user_input[0] == 'C':
            try:
                if user_input.split()[2] == '-n':
                    directory_path = user_input.split()[1]
                    name = user_input.split()[3]
                    profile = create_new_file(directory_path, name)
                    if profile:
                        new_directory = f"{directory_path}/{name}.dsu"
                        print(new_directory)
                        edit_file(profile, new_directory)
                else:
                    print("ERROR")
            except Exception:
                print("ERROR")
        elif user_input[0] == 'D':
            file_path = Path(user_input[2:])
            delete_dsu_file(file_path)
        elif user_input[0] == 'R':
            file_path = Path(user_input[1:].split()[0])
            read_dsu_file(file_path)
        elif user_input[0] == 'O':
            path = user_input.split()[1]
            profile1 = load_file(path)
            if profile1:
                edit_file(profile1, path)
        else:
            print("ERROR")
