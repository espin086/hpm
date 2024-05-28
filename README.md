# hpm
This is a tool that creates the weekly updates that are presented to leadership on our different accounts.

# Installing Software

Ensure you have the secrets.toml in the .streamlit directory.

```bash
ls .streamlit 
```

Should return the following: 

```bash
secrets.toml
```

This file should contain the following keys to be able to access API keys.

```bash
[openai]
key = "{MY OPENAI KEY HERE}"
org = "{MY OPENAI ORG HERE}"
```

Create a virtual environment and activate it.

```bash
python -m venv .venv
source .venv/bin/activate
```

Set up dependencies with Makefile

```bash
make setup
```

Run application with Makefile

```bash
make run
```

