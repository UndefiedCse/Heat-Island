echo Making directory
cd ..
mkdir -p data
cd data
mkdir -p dsm
mkdir -p dtm
cd dtm
# For bigger size map use commented command, Phase 5 = no loss data, phase 3 some loss data (smaller file)
echo Downloading DTM data
# curl -O 'https://srsp-open-data.s3-eu-west-2.amazonaws.com/lidar/phase-5/dtm/27700/gridded/NT27SW_50CM_DTM_PHASE5.tif?'
# curl -o 'NT27SE_50CM_DTM_PHASE3.tif' 'https://srsp-open-data.s3.eu-west-2.amazonaws.com/lidar/phase-3/dtm/27700/gridded/NT27SE_50CM_DTM_PHASE3.tif?'
# curl -o 'NT16NE_50CM_DTM_PHASE3.tif' 'https://srsp-open-data.s3.eu-west-2.amazonaws.com/lidar/phase-3/dtm/27700/gridded/NT16NE_50CM_DTM_PHASE3.tif?'
echo Finish downloading DTM
cd ..
cd dsm
echo Downloading DSM data
# curl -O 'https://srsp-open-data.s3-eu-west-2.amazonaws.com/lidar/phase-5/dsm/27700/gridded/NT27SW_50CM_DSM_PHASE5.tif?'
# curl -o 'NT27SE_50_DSM_PHASE3.tif' 'https://srsp-open-data.s3.eu-west-2.amazonaws.com/lidar/phase-3/dsm/27700/gridded/NT27SE_50CM_DSM_PHASE3.tif?'
# curl -o 'NT16NE_50CM_DSM_PHASE3.tif' 'https://srsp-open-data.s3.eu-west-2.amazonaws.com/lidar/phase-3/dsm/27700/gridded/NT16NE_50CM_DSM_PHASE3.tif?'
echo Finish downloading DSM