## Motivation

We cannot trust cloud providers but still want to use their services. We want to be able to easily `mount` and `umount`  partitioned and encrypted binary files.

### Configuration
- Configuration file should be named `.dropconfig`.
- It should contain the fields bellow.
```
{
    "repository":"./repository",
    "devices": [
        {
            "name": "str",
            "input": "./data",
            "mount_point": "./mount"
        }
    ]
}

```
- `repository`: this field contains a path to where all of the assembled binary files are going to be stored.
- `name`: this field contains a name that is going to be used for assembled binary file.
- `input`: this field contains where split binary files are located.
- `mount_point`: this field contains a path to a folder on which the assemble and decrypted binary file is going to be mounted.

### Example usage
```
$ drop generate-config
$ drop mount name_from_dropconfig
$ drop umount name_from_dropconfig
```

### Commands
- `generate-config` is going to create a skeleton `.dropconfig` file that is used by the drop command line.
- `mount` is going to mount a devices with `name_from_dropconfig` on the mount point defined in the `.dropconfig`.
- `umount` is to unmount a device with `name_from_dropconfig` from the mount point defined in the `.dropconfig`.

