# conapp - The easy config applier

A simple project for applying config files from repos/tar files

#### Example command:
```
conapp config -u drew887 -b
```

The above will:
  * download a tarball from drew887's config repo on bitbucket *(-b)*
  * take a backup of all the files that are listed in the tarball that
  would be overridden locally on your system
  * untar the repo into your home directory.

### Available commands:

#### `config` Command
Used for downloading and applying configs from either Bitbucket or Github.

  * `list`: Lists out configs that are available locally
  * `apply`: Download and apply a config based on username & repo name
  * `undo`: Apply snapshot taken when a config was last applied.

      IE: `conapp config undo -u drew887` will apply the snapshot taken when
      the `drew887/config` repo was last applied


#### `snapshots` Command
Used for managing local backups created by conapp during the `config` commands

  * `list`: List available backups
  * `delete`: Delete a backup
  * `restore`: Restore a backup
