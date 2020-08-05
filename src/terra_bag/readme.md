In order to run this,

source /opt/ros/melodic/setup.zsh
conda deactivate
conda deactivate
source develBridge/setup.zsh
source devel/setup.zsh
rosrun terra_bag get_images.py src/terra_bag/src/small.bag ./out/ /d435i/color/image_raw /t265/odom/sample
