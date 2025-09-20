# Repo-Context-Packager

Pack Git Repository into a text file for use in LLM

## Instruction for Windows Users:

### Step 1

Check if Python is installed in the system by the following command:

```cmd
python --version
```

or

```cmd
py --version
```

If Python is not installed, visit https://www.python.org/ -> Downlaods -> Windows,
and choose the latest Stable Releases to download and install.

Notes: make sure that the installation path of Python is in Windows PATH

### Step 1.1

Download **requirement.txt** from the repository.

Install dependencies by the following commands:

```cmd
py -m pip install -r requirement.txt
```

### Step 2

Download **pack-repo.py** in **src** directory to your local machine

### Step 3

Run the script by the following command:

```cmd
python pack-repo.py repo-path [-r [DAYS]] [-o] [output-file-name]
```

or

```cmd
py pack-repo.py repo-path [-r [DAYS]] [-o] [output-file-name]
```

## Instruction for Mac/Linux Users:

### Step 1

Check if Python is installed in the system by the following command:

```bash
python3 --version
```

If Python is not installed, visit https://www.python.org/ -> Downlaods -> macOS,
and choose the latest Stable Releases to download and install.

Alternatively, user can check if **brew** is available using command `brew --version`, and use **brew** to install Python with the following command:

```sh
brew install python
```

### Step 1.1

Download **requirement.txt** from the repository.

Install dependencies by the following commands:

```bash
python3 -m pip install -r requirement.txt
```

### Step 2

Download **pack-repo.py** in **src** directory to your local machine

### Step 3

Run the script by the following command:

```bash
python3 pack-repo.py repo-path [-r [DAYS]] [-o] [output-file-name]
```
