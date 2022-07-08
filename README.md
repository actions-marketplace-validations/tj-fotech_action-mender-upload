# mender-artifact-uploader-action

The mender-artifact-uploader-action is a very lightweight Github action which allows you to upload Mender Update Module artifacts using `mender-artifact` 3.7.1 and Python 3.9 via Mender basic auth and Mender's RESTful Management API v1.

## Inputs

### `mender-device-type`

_Description:_
Target device type.

_Required:_ *true*

### `mender-device-release`

_Description:_
Release name.

_Required:_ *true*

### `mender-device-update-module`

_Description:_
Update module name already on the device.

_Required:_ *true*

### `mender-device-update-module-files`

_Description:_
Files to be executed against the given update module.

_Required:_ *true*

### `mender-device-group`

_Description:_
Targeted device group for this artifact.

_Required:_ *true*

### `mender-auth-username`

_Description:_
Mender server basic auth username.

_Required:_ *true*

### `mender-auth-password`

_Description:_
Mender server basic auth password.

_Required:_ *true*

### `mender-server-url`

_Description:_
Mender server url.

_Required:_ *true*

## Example usage

```yaml
on: [push]

jobs:
  push-mender-artifact:
    runs-on: ubuntu-latest
    name: Mender artifact pipeline
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Upload Mender artifact
        uses: Cein-Markey/mender-artifact-uploader-action@v0.2.0-alpha
        id: mender-artifact-upload
        with:
          mender-device-type: raspberrypi3
          mender-device-release: release-v0.1.0
          mender-device-update-module: dockerservice
          mender-device-update-module-files: "foo.txt,bar.txt" #root files from actions/checkout@v3
          mender-device-group: staging
          mender-auth-username: username
          mender-auth-password: password
          mender-server-url: https://hosted.mender.io
```
