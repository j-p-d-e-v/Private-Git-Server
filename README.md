# Git Private Repositories

This is a simple way to host your private git repositories. It both supports ssh and http.

```
I might possibly continue developing this like adding frontend UI etc..
```

# Build

```
docker build . -t <your_image_tag>
```

# Configuration
## Environment Variables

You can set the environment variables at the .env file.

- ROOT_PASSWORD - The assigned password for the root account.

## Volumes


- /var/git - Is the default or working directory where the repositories are placed.
- /tmp/ssh-keys - Is the directory where the external machine ssh keys are stored.

# Deploy

The docker-compose.yml will automatically build the image ```git-server:latest```.

To run:
```
docker-compose up -d
```

# Examples

## Clonng

**via HTTP**
```
git clone http://<container_ip>/repositories/<repo_name>
```

Example:

```
git clone http://192.168.0.2:5080/repositories/myrepo
```

**via SSH**

Format:
```
git clone ssh://root@<container_ip>:<port>/var/git/<repo_name>
```

```
git clone ssh://root@192.168.0.2:2/var/git/myrepo
```

# API

The server exposes a swagger documentation. You visit the swagger page at: 
```
http://<ip_domain>:5080/api/docs
```

# Developer
- JP Mateo