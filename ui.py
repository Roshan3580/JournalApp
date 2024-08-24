# ROSHAN RAJ
# roshar1@uci.edu
# 90439894

# ui.py

from pathlib import Path
from Profile import Post, DsuProfileError, DsuFileError
from admin import create_new_file, load_file, delete_dsu_file, read_dsu_file
from ds_client import send


def create_ui():
    print("Welcome! Do you want to create or load a DSU file?")
    user_input = input("Type 'c' to create or 'l' to load: ").lower()

    if user_input == 'c':
        create_new_file_ui()
    elif user_input == 'l':
        load_file_ui()
    else:
        print("Invalid input. Please try again.")


def create_new_file_ui():
    try:
        directory_path = input("Enter the directory path: ")
        name = input("Enter the file name: ")
        profile = create_new_file(directory_path, name)
        if profile:
            new_directory = f"{directory_path}/{name}.dsu"
            print(f"Loaded file: {new_directory}")
            edit_file_ui(profile, new_directory)
    except DsuFileError as e:
        print(f'{e}')

    except DsuProfileError as e:
        print(f'{e}')

    except Exception:
        print("ERROR")


def load_file_ui():
    try:
        path = input("Enter the file path: ")
        profile = load_file(path)
        if profile:
            print(f"Loaded file: {path}")
            edit_file_ui(profile, path)
    except DsuFileError as e:
        print(f'{e}')

    except DsuProfileError as e:
        print(f'{e}')

    except Exception:
        print("ERROR")


def delete_file_ui():
    try:
        file_path = input("Enter the file path: ")
        delete_dsu_file(Path(file_path))

    except DsuFileError as e:
        print(f'{e}')

    except Exception:
        print("ERROR")


def read_file_ui():
    try:
        file_path = input("Enter the file path: ")
        read_dsu_file(Path(file_path))
    except DsuFileError as e:
        print(f'{e}')

    except Exception:
        print("ERROR")


def edit_file_ui(profile, filepath):
    try:
        print("To edit username: E -usr 'username'")
        print("To edit password: E -pwd 'password'")
        print("To edit bio: E -bio 'The bio that you want'")
        print("To add a post: E -addpost 'Whatever you want to post in the Journal'")
        print("To delete a post: E -delpost number (to delete first post, put 1 instead of number)")
        while True:
            user_input = input("Edit the code (Q to exit): ").strip()
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
                            dsuserver = input("Enter the server address without quotation marks: ").strip()
                            profile.dsuserver = dsuserver
                            port = 3021
                            username = profile.username
                            password = profile.password
                            if profile.bio is not None:
                                bio = profile.bio
                                send(dsuserver, port, username, password, addpost_content[1:-1], bio)
                            else:
                                send(dsuserver, port, username, password, addpost_content[1:-1])


                        except Exception as e:
                            print(f"Error {e}")
                    elif post_online == 'n':
                        profile.dsuserver = None
                    else:
                        print("Invalid input!")

                    profile.add_post(Post(entry=addpost_content[1:-1]))
                    profile.save_profile(filepath)

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
                    print("ERROR")

            else:
                print("Invalid input!")

    except DsuFileError as e:
        print(f'{e}')

    except Exception:
        print("ERROR")
