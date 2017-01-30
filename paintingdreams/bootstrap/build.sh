#!/bin/bash

if [ ! -d bower_components ]; then
    bower install
    cd bower_components/bootstrap
    npm install
    cd ../..
fi

cd bower_components/bootstrap/less

if [ ! -f variables.original.less ]; then
    mv variables.less variables.original.less
fi
ln -sf ../../../custom/variables.less variables.less

if [ ! -f bootstrap.original.less ]; then
    mv bootstrap.less bootstrap.original.less
fi
ln -sf ../../../custom/bootstrap.less bootstrap.less

ln -sf ../../../custom/paintingdreams.less paintingdreams.less

cd ..
grunt dist
