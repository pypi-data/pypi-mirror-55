# TBM - Tunnel Boring Machine
A command line program for managing SSH tunnels.

## Examples

Open them by name:
```
tbm open syncthing
```

Close them by name:
```
tbm close syncthing
```

See open tunnels:
```
tbm list

name       |remote_username  |remote_server            |local_port  |remote_hostname  |remote_port  |ssh_port  |
================================================================================================================
tun1       |shane            |non_saved_tunnel.com     |1997        |localhost        |3794         |78        |
syncthing  |shane_lizard     |server.shane_lizard.com  |3000        |localhost        |8384         |22        |

```

See saved tunnels:
```
tbm list saved

name         |remote_username  |remote_server           |local_port  |remote_hostname  |remote_port  |ssh_port  |
=================================================================================================================
syncthing    |shane_lizard     |server.shane_lizard.com |3000        |localhost        |8384         |22        |
example_tun  |shane            |not_real.com            |2730        |localhost        |1920         |22        |
good_tun     |lizard           |demo.website.com        |1776        |localhost        |4496         |792       |

```
