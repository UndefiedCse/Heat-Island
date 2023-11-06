echo Making directory
mkdir -p DSM
mkdir -p DTM
cd DTM
# For bigger size map use commented command
echo Downloading DTM data
curl -o 'NT27SE_50CM_DTM_PHASE3.tif' 'https://srsp-open-data.s3.eu-west-2.amazonaws.com/lidar/phase-3/dtm/27700/gridded/NT27SE_50CM_DTM_PHASE3.tif?'
# curl -o 'NT16NE_50CM_DTM_PHASE3.tif' 'https://srsp-open-data.s3.eu-west-2.amazonaws.com/lidar/phase-3/dtm/27700/gridded/NT16NE_50CM_DTM_PHASE3.tif?'
echo Finish downloading DTM
cd ..
cd DSM
echo Downloading DSM data
curl -o 'NT27SE_50_DSM_PHASE3.tif' 'https://srsp-open-data.s3.eu-west-2.amazonaws.com/lidar/phase-3/dsm/27700/gridded/NT27SE_50CM_DSM_PHASE3.tif?'
# curl -o 'NT16NE_50CM_DSM_PHASE3.tif' 'https://srsp-open-data.s3.eu-west-2.amazonaws.com/lidar/phase-3/dsm/27700/gridded/NT16NE_50CM_DSM_PHASE3.tif?'
echo Finish downloading DSM