# vcs-uploader


## Getting Started

```bash
usage: vcsup [-h] -f FILE -r REPO [-l {0,1}] -m MESSAGE -v VERSION
                   [-d {0,1}]
                   url

gen vcs-uploader

positional arguments:
  url                   server api base url

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  version's file
  -r REPO, --repo REPO  repo name
  -l {0,1}, --latest {0,1}
                        set to latest?
  -m MESSAGE, --message MESSAGE
                        version descriptions
  -v VERSION, --version VERSION
                        version code
  -d {0,1}, --debug {0,1}
                        debug vcs-uploader
```

## License
Released under the 
[MIT License](https://raw.githubusercontent.com/gen-iot/vcs-uploader/master/License)

