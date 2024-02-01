export CONTAINER_NAME=notes-backend
export RECOMMENDED_CMD="python3 app.py" 

if [[ $* == *--clean* ]]
then
    echo "Running CLEANUP Function"
    docker compose -f ./docker-compose.yaml down --remove-orphans 
else
    echo "Skipping CLEANUP function (Add --clean to execute)"
fi

# Remainder of script is here 
echo "Building Deployment..."
docker compose -f ./docker-compose.yaml build --pull
docker compose -f ./docker-compose.yaml up -d

echo "Collecting Static Files..."
docker exec -it $CONTAINER_NAME /bin/bash /src/app_collectstatic.sh 

if [[ $* == *--migrations* ]]
then
    echo "Running Migrations"
    docker exec -it $CONTAINER_NAME python3 /src/osm_db.py migrations upgrade
fi

echo "Entering container for live environment..."
echo "Type 'exit' to quit" 
echo "Recommended command: '$RECOMMENDED_CMD'"
docker exec -it $CONTAINER_NAME bash

echo "Do you wish to do a full cleanup? (Selecting No will stop the $CONTAINER_NAME only)"
select response in "Full Cleanup" "Stop $CONTAINER_NAME only";
do 
    if [[ $REPLY == 1 ]]
    then 
        echo "Performing full clean-up of full deployment..."
        docker compose -f ./docker-compose.yaml down
        break 
    fi

    if [[ $REPLY == 2 ]]
    then
        echo "Stopping application container..."
        docker container stop $CONTAINER_NAME
        docker container rm $CONTAINER_NAME
        break
    fi 
done 

echo "Script Complete."