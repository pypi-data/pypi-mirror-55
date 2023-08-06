## pyedgeloop
PyEdgeLoop is a fast and simple python package to detect loops, outer boundary and edges in binary images.<br />
This library was initially created to help detect loops and boundaries/edges in word images. It plays an important role in segmentation of cursive handwriting 
segmentation. But it can be used for many other purposes also.

## Installation
pip install pyedgeloop

## Usage
import pyedgeloop as detect <br />
import cv2 <br />
Im = cv2.imread(your_filename)<br />
Loops, Edges, Boundary = detect.DetectLoopsEdges(Im) <br />

## Examples

<b>Here are some examples where we are finding loops and boundary of a handwritten word image-</b> <br /><br />
<b>Input</b> <br /><br />

1 ![alt input1](https://raw.githubusercontent.com/AdityaDutt/Loop-and-Edges-Detector/master/Images/Image1/word1.png)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

2 ![alt input2](https://raw.githubusercontent.com/AdityaDutt/Loop-and-Edges-Detector/master/Images/Image2/word2.png)<br />

<br />

<b> Output </b>  <br /><br /><br />
Loops

1 ![alt output1](https://raw.githubusercontent.com/AdityaDutt/Loop-and-Edges-Detector/master/Images/Image1/Loops.png)<br /><br />

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

2 ![alt output1](https://raw.githubusercontent.com/AdityaDutt/Loop-and-Edges-Detector/master/Images/Image2/Loops.png)<br /><br />

Outer Boundary

1 ![alt output2](https://raw.githubusercontent.com/AdityaDutt/Loop-and-Edges-Detector/master/Images/Image1/Boundary.png)<br /><br />

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

2 ![alt output2](https://raw.githubusercontent.com/AdityaDutt/Loop-and-Edges-Detector/master/Images/Image2/Boundary.png)<br /><br />

Edges

1 ![alt output3](https://raw.githubusercontent.com/AdityaDutt/Loop-and-Edges-Detector/master/Images/Image1/Edges.png)<br /><br />

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

2 ![alt output3](https://raw.githubusercontent.com/AdityaDutt/Loop-and-Edges-Detector/master/Images/Image2/Edges.png)<br /><br />


<b>Here is another example where we need to detect only edges-</b> <br /><br />

<b>Input</b> <br /><br />

![alt input3](https://raw.githubusercontent.com/AdityaDutt/Loop-and-Edges-Detector/master/Images/Image3/leaf.jpeg)<br />

<b>Output Edges</b> <br /><br />

![alt output31](https://raw.githubusercontent.com/AdityaDutt/Loop-and-Edges-Detector/master/Images/Image3/Edges_leaf.png)<br /><br />


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
Aditya Dutt - https://github.com/AdityaDutt 

## License
[MIT](https://choosealicense.com/licenses/mit/)