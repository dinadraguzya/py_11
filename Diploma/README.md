# Diploma project: Spy Games

The script is designed to display the list of user's VK groups, the members of which don't include user's friends.

The script takes a JSON file as a parameter. The file should contain the following data:
```bash
{ "user_id": int, "access_token": "string", "version": "5.73" }
```

# Running the Script

To run the script you need to have Python 3.6 installed and running well

```bash
$ python3 find_unique_groups.py <path_to_request_params_file>

Extracting user's groups. Please wait.
- - - - - - - - - - - - - - - - - - - -
Creating a user's group list. Please wait.
. . . . . . . . . . . . . . . 
The execution is finished. Please find a file with the list of unique user's groups at /Users/username/unique_groups.json
```

The output file is located in the same directory as the script. 
The sample output is:

```bash
unique_groups.json

[
    {
        "gid": 57031809,
        "members_count": 64,
        "name": "Домашняя школа"
    },
    {
        "gid": 47465154,
        "members_count": 8629,
        "name": "TOP PEOPLE MORDOR"
    },
    {
        "gid": 33410020,
        "members_count": 83,
        "name": "Газировка Dr Pepper в Нижнем Новгороде"
    },
    .....
 ]
```
