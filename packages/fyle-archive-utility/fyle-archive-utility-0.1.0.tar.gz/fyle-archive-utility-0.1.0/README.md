# fyle-archive-utility

Command-line tool to download Fyle data.

# Installation

This project requires python 3.7+ , fylesdk  and click library

* You can download this project and use it ( copy in your own project, etc)
* Install it from [pip](https://pypi.org)

      $ pip install fyle-archive-utility

# Usage

To use this archive utility you'll need these Fyle credentials : client ID, client secret and refresh token.

       $ python -m fyle_archive_utility connect
       # Then will ask for Fyle credentials
       
       Please enter the credentials:
       
       client_id: <type> press enter
       client_secret: <type> press enter
       refresh_token: <type> press enter
       base_url: <type> press enter

Once you are connected your credentials will be saved and you can access your data 
                      
Now you are able to access the command line interface for downloading Fyle data

       $ python -m fyle_archive_utility expenses --file_format=csv --path='/Users/sravankumar/Desktop'   // Lists out all the expenses of your org that match the parameters and saves it as a csv file in the given path
       
       $ python -m fyle_archive_utility expenses --file_format=json --path='/Users/sravankumar/Desktop'    // Lists out all the expenses of your org that match the parameters and saves it as a json file in the given path

       $ python -m fyle_archive_utility expenses --state='COMPLETE' --file_format=csv --path='/Users/sravankumar/Desktop'    // Lists out all the expenses of your org that match the parameters and saves it as a csv file in the given path
       
       $ python -m fyle_archive_utility expenses --state='APPROVED' --file_format=json --path='/Users/sravankumar/Desktop'    // Lists out all the expenses of your org that match the parameters and saves it as a json file in the given path

## Contribute

To contribute to this project follow the steps

* Fork and clone the repository.
* Run `pip install -r requirements.txt`
* Setup pylint precommit hook
    * Create a file `.git/hooks/pre-commit`
    * Copy and paste the following lines in the file - 
        ```bash
        #!/usr/bin/env bash 
        git-pylint-commit-hook
        ```
     * Run `chmod +x .git/hooks/pre-commit`
                 
# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details