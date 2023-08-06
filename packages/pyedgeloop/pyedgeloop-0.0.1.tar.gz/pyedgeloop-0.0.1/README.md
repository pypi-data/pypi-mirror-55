## pyedgeloop
PyEdgeLoop is a fast and simple python package to detect loops, outer boundary and edges in binary images.

## Installation
pip install pyedgeloop

## Usage
import pyedgeloop as detect <br />
import cv2 <br />
Im = cv2.imread(your_filename)<br />
Loops, Edges, Boundary = detect.DetectLoopsEdges(Im) <br />

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author
Aditya Dutt - https://github.com/AdityaDutt 

## License
[MIT](https://choosealicense.com/licenses/mit/)