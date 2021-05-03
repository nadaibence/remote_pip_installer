# !/bin/bash
while getopts h:c: flag
do
    case "${flag}" in
        h) host=${OPTARG};;
        c) cfg=${OPTARG};;
    esac
done

echo "hostname: $host"
echo "Config location: $cfg"

scriptdir=$(dirname $0)
projdir=$(dirname $scriptdir)

# parancssori argumentumban atadott cfg file-t atmasoljuk a docker compose file context-jebe
rm -r $projdir/cfg
mkdir $projdir/cfg
cp -R $cfg/* $projdir/cfg

docker-compose -f $projdir/docker-compose.yml build --build-arg REMOTE_HOST="${host}" --no-cache -q
docker-compose -f $projdir/docker-compose.yml up
