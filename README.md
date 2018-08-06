# Zalora SRE coding test

## Building
```bash
cd ~

git clone https://github.com/nhamlh/zapi.git && cd zapi

docker build -t zapi .
```

## Start the web server
```bash
docker run -d -p 5000:5000 -e LISTEN_HOST=0.0.0.0 zapi
```

## Available environment variables
| Name         | Description                      |
|--------------|----------------------------------|
|FILESTORE_PATH| The path to store uploaded files |
|ENV           | Running environment              |
|LISTEN_HOST   | Listening interface              |
|LISTEN_PORT   | Listening port                   |

