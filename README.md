# StereoToNormal
StereoToNomal is a short program written in python that can convert stereo images into a normal. This could be useful for 3D artist that wants to quickly capture ground or wall texture for a 3D environment. 

## How to use StereoToNormal
StereoToNormal can be ran through the command line like any other python program. In order to run it you would type the following command
```python StereoToNormal.py right_image_location left_image_location```

Some optional parameters are able to be used as well. 
| Parameter | Description |
| ----------- | ----------- |
| -g off | disables the gaussian blur.       |
| -b [int]   | changes the block sizr in block matching algorithm        |

## Possible modifications
While I have left them inaccessable when running the code through the command line, some parameters could be edited like **numDisparities**, **sigma**, **lamda**, and the strength of  the gaussian blur under **def blur(img)** that is set to 9. If you enjoy tinkering, look into openCV's docs and mess around with those parameters if you'd like to.

Cheers :)
