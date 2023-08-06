# `quilt-stack-installer`

CLI to launch a Quilt CFN stack. Uses a configuration file ("Installer Config YAML") to figure out what inputs the user needs to give. 

# Installer Config YAML
The config YAML is created from the default CFN template during `make release` (in `t4/` directory) and is written to s3. `make release-prod` will always write the installer config yaml to a specific s3 location. By default `quilt-stack-installer` will use the config file in that s3 location, but a custom config can be passed in via `quilt-stack-installer install --config-yaml=XXXX` for testing or to launch a specific variant.

The code makes some assumptions about what inputs the user will pass in. This means that the code is coupled to the config yaml. Small changes such as prompt string typos or new arguments won't be a problem, but removing/changing core arguments such as `QuiltWebHost` will require the codebase to be changed. Both the [codebase](quilt_stack_installer/config.py) and the [installer config](../t4/installer_config_template.yaml) have a schema version which allows for this to happen - if the codebase tries to pull a config YAML and the schema doesn't match, it will fail and tell the user to update `quilt-stack-installer`.

## Publishing

```
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```

