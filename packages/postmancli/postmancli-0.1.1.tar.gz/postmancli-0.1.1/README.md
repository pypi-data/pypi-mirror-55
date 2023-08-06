# postman-cli

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/08eb8749f36e428b8e350bcbb22b0083)](https://www.codacy.com/manual/RDCH106/postman-cli?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=RDCH106/postman-cli&amp;utm_campaign=Badge_Grade)

Python CLI (postmancli) tool for emails sending using SMTP server.

### What can I do with PFS?

* Send emails using SMTP SSL
* Use it from terminal when it is installed
* Multiplatform execution (it is developed in Python)


### Installation

You can install or upgrade postmancli with:

`$ pip install postmancli --upgrade`

Or you can install from source with:

```bash
$ git clone https://github.com/RDCH106/postman-cli.git --recursive
$ cd postmancli
$ pip install .
```


### Quick example

```bash
$ postmancli -S user:password@smtp.gmail.com:465 -f user@gmail.com -t someone@gmail.com -s postman-cli --text "Hello everyone!@nl@@tab@It seems that this works ..." -a "file.txt" "photo.jpg"
```

The example sends an email with `user@gmail.com` as sender, `someone@gmail.com` as receiver, `postman-cli` as subject, `Hello every...` as text message and 2 attachments (file.txt & photo.jpg).


### Help

Run the following command to see all options available:

`pfs --help` or ` pfs -h`
