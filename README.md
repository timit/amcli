# README

## building docker image

- `docker build -t timit/amcli .`

## running docker image

- `docker run --rm -ti -v {local/path/to/data}:/var/data timit/amcli {parameters}`

- minimal invocation:
    - show usage help: `docker run --rm -ti timit/amcli`
- sample invocations:
    - `docker run --rm -ti -v ~/Desktop:/var/data timit/amcli dist -A='com.gliffy.integration.confluence'`
    - `docker run --rm -ti -v ~/Desktop:/var/data timit/amcli dist -A='com.gliffy.integration.jira'`
    - `docker run --rm -ti -v ~/Desktop:/var/data timit/amcli attr -V='99' -d='7' -u 'username' -p 'password'`
    - `docker run --rm -ti -v ~/Desktop:/var/data timit/amcli attr -V='99' -e='2019-11-19' -d='7' -u 'username' -p 'password'`
    - `docker run --rm -ti -v ~/Desktop:/var/data timit/amcli unin -V='99' -d='7' -u 'username' -p 'password'`

## python script usage notes
the python script uses a couple non-standard packages.  these are pulled into the docker image automatically, but running the script outside of the provided docker image will require installation of these packages locally:

- `pip install -r requirements.txt`

the script accepts command-line arguments.  invoking the script with the `-h` option will show guidances.  some hints on getting started follow:

- required parameters
    - report_mnemonic specified as a positional parameter
        - `dist`: application distribution statistics
        - `attr`: marketing campaign attributions
- optional parameters
    - username specified using `-u`
    - password specified using `-p`
    - specify application key for inclusion `-A`
    - specify vendor key `-V`
    - verbosity level using `-v` or `-vv`, allows viewing of input and processing (mainly for debugging purposes)
    - specify beginning date for reporting using `-b`
    - specify ending date for reporting using `-e`
    - specify number of days to report on using `-d`
