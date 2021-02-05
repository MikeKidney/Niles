from os import rename, listdir
from os.path import isfile, join


def find_files(directory_to_search: str, file_extension: str) -> list:
    """
    Checks directory for files of the chosen type.

    :return a list containing all the filenames of the chosen type.
    """
    return [directory_to_search + "\\" + f for f in listdir(directory_to_search)
            if isfile(join(directory_to_search, f)) if f[-4:] == file_extension]


def separator_symbols(length=80, separator="-") -> str:
    """
    multiplies the separator with the length.

    :return 'str' that divides lines to produce a good looking
            output.
    """
    return separator * length


def path_name_type(file_name: str,
                   chosen_dir: str,
                   file_extension: str) -> tuple:
    """
    splits a string containing of file path and file name into two
    separated strings one of which is the path and the other the file.

    :return a tuple that contains the string for 1. path, 2. file and
            3. the file extension.
    """
    path_length = len(chosen_dir) + 1
    path = file_name[:path_length]
    file = file_name[path_length:-len(file_extension)]
    filetype = file_extension
    return path, file, filetype


if __name__ == "__main__":
    new_name_list = []
    files_to_process = []
    old_path_name = "_"
    # User chooses a path where the files are in:
    while True:
        chosen_directory = input("Directory path (C:\\path_of_directory): ")
        chosen_file_type = ".mp3"   # could be changed to input.
        try:
            files_to_process = find_files(chosen_directory, chosen_file_type)
        except FileNotFoundError:
            print(separator_symbols(49, "*"))
            print("Could not find the directory.")
        except OSError:
            print("WinError 123")
        if files_to_process:
            break
        else:
            print(separator_symbols(49, "*"))
            print("There are no valid files in the chosen directory.")
            print(separator_symbols(49, "*"))
            print("1 - Try again")
            print("0 - Exit")
            chosen_answer = input()
            if chosen_answer == "0":
                break
    if files_to_process:
        print(separator_symbols(10 + len(chosen_directory)))
        print("Files in", chosen_directory + ":")
        print(separator_symbols(10 + len(chosen_directory)))
    for entry in files_to_process:
        print(entry)
    print(separator_symbols(10 + len(chosen_directory)))

    # Main options menu:
    while True and files_to_process and not new_name_list:
        print(separator_symbols())
        print("Do you want to remove or add anything to the filenames?")
        print("1 - remove a string")
        print("2 - remove a slice")
        print("3 - add a string")
        print("0 - exit")
        print(separator_symbols())
        add_or_remove = input("Choose an option: ")
        print(separator_symbols())

        if add_or_remove != "3" and not "0":
            print("Here is an example of the current file names:")
            _, f_name, _2 = path_name_type(files_to_process[0],
                                           chosen_directory,
                                           chosen_file_type)
            print(f_name)
            print(separator_symbols())

        if add_or_remove == "0":
            break
        elif add_or_remove == "1":  # remove string
            remove_strsq = input("Please type in the exact string sequence\n"
                                 "you want to remove from the filenames:")
            for old_path_name in files_to_process:
                index_of_cut = old_path_name.find(remove_strsq)
                if index_of_cut != -1:
                    new_name_beginning = old_path_name[:index_of_cut]
                    new_name_end = old_path_name[index_of_cut +
                                                 len(remove_strsq):]
                    new_name = new_name_beginning + new_name_end
                    new_name_list.append(new_name)
            else:
                if new_name_list:
                    print(separator_symbols(60))
                    print("Here is a last comparison of "
                          "the old and new filename:")
                    print(old_path_name)
                    print(new_name_list[-1])
                    break
                else:
                    print("No file contains the chosen string.")
                    break

        elif add_or_remove == "2":  # remove a slice
            f_path, f_name, f_type = path_name_type(files_to_process[0],
                                                    chosen_directory,
                                                    chosen_file_type)
            print("The filename with the index numbers below:")
            print(separator_symbols(40))
            for character in f_name:
                print(character + " ", end="")
            print()
            for i in range(len(f_name)):
                if i < 10:
                    print(str(i) + " ", end="")
                elif i >= 10:
                    print(str(i), end="")
            print()
            print(separator_symbols(40))
            while True:
                not_valid = False
                slice_start = input(
                    "Please enter index to start "
                    "the slice you want to keep: ")
                try:
                    slice_start = int(slice_start)
                except ValueError:
                    not_valid = True
                print("If you want the slice to the end of "
                      "each file type 'end'")
                slice_end = input(
                    "Please enter index to end slicing (including): ")
                try:
                    if slice_end != "end":
                        slice_end = int(slice_end)
                    elif slice_end == "end":
                        pass
                except ValueError:
                    not_valid = True
                if not_valid:
                    print("Please enter valid numbers.")
                    pass
                elif slice_end == "end":
                    print(separator_symbols(60))
                    print("This is how the new filename looks like:")
                    print(f_name[slice_start:])
                    print("1 - Confirm change")
                    print("2 - Change the slice again")
                    print("0 - Cancel")
                    ok = input()
                    if ok == "1":
                        for old_path_name in files_to_process:
                            path_s, file_s, type_s = \
                                path_name_type(old_path_name,
                                               chosen_directory,
                                               chosen_file_type)
                            new_name_list.append(path_s +
                                                 file_s[slice_start:] +
                                                 type_s)
                    break
                else:
                    slice_end = int(slice_end) + 1
                    print(separator_symbols(60))
                    print("This is how the new filename looks like:")
                    print(f_name[slice_start:slice_end])
                    print("1 - Confirm change")
                    print("2 - Change the slice again")
                    print("0 - Cancel")
                    ok = input()
                    if ok == "1":
                        for old_path_name in files_to_process:
                            path_s, file_s, type_s = \
                                path_name_type(old_path_name,
                                               chosen_directory,
                                               chosen_file_type)
                            new_name_list.append(path_s +
                                                 file_s[slice_start:slice_end] +
                                                 type_s)
                        break
                    elif ok == "2":
                        pass
                    elif ok == "0":
                        files_to_process = []
                        break

        elif add_or_remove == "3":  # adds a string
            str_to_add = input("Please enter the string you want to add: ")
            print("1 - add string in front")
            print("2 - add string to the end")
            print("0 - cancel")
            start_or_end = input()
            if start_or_end == "1":     # add to front
                for old_path_name in files_to_process:
                    path_s, file_s, type_s = path_name_type(old_path_name,
                                                            chosen_directory,
                                                            chosen_file_type)
                    new_name_list.append(path_s + str_to_add + file_s + type_s)
            elif start_or_end == "2":   # add to the end
                for old_path_name in files_to_process:
                    new_name_list.append(old_path_name[:-len(chosen_file_type)]
                                         + str_to_add + chosen_file_type)
            else:
                break
            print(separator_symbols(60))
            print("This is how the new filename will look like:")
            print(new_name_list[0])
            print(separator_symbols(60))
        else:
            print("Please enter a valid option. Thank you.")

    # file names are getting changed
    if new_name_list and files_to_process:
        final_call = input("Do you really want to change the filenames? (y/n): ")
        if final_call == "y":
            try:
                for index, old_name in enumerate(files_to_process):
                    new_name = new_name_list[index]
                    rename(old_name, new_name)
                print(separator_symbols(42, "*"))
                print("Your files have been successfully renamed.")
                print(separator_symbols(42, "*"))
            except FileNotFoundError:
                print(separator_symbols(60, "X"))
                print("Not all the files contain the chosen sequence of string.")
                print(separator_symbols(60, "X"))
            except FileExistsError:
                print(separator_symbols(60, "X"))
                print("All the files still must have individual names.")
                print(separator_symbols(60, "X"))
        else:
            print("Thank you for your time, have a wonderful day.")
