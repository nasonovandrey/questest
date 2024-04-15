# Introduction
This tool allows you to run pytests with ipdb debugger while inserting breakpoints on the fly. This workflow makes sense if you practice "user-scenario-oriented development". In this practice every test should represent an actual "battlefield" scenario your code can encounter in the hands of the user. This makes tests very informative and allows you to have a built-in "literate programming" of sorts: scenarios are tests, but they can also function as tutorials, so they represent both validation of your code and documentation for your code.

# Installation
For this tool to work you have to have `ncurses` installed. This is one way to do it if you are on a `apt`-based distro:
```bash
sudo apt-get install libncurses5-dev libncursesw5-dev
```

After that and cloning this repo you should be good to go with `pip install .`.

# Shortcomings

This tool does not allow you to:
1. Use interactive search while inputting the path to your test.
2. To configure debugger you want to use.
3. To run itself on Windows.
4. To configure an indentation level.
These are just some major features, but I'm sure there's more. Still, it works great for me. If you want anything here, you are welcome to add it.
