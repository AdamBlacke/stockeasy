@ECHO OFF

GOTO %1

:DOCKER
    call env.bat
    echo "starting docker build"
    docker build -f ./container/dockerfile . -t stockeasy:develop
    docker run -v %LOCAL_MOUNT%:/stockeasy -it stockeasy:develop