## Invention Assignment - Video Shazam
This is a complete video detection solution that is able to index, query and evaluate the system's ability to find a video from provided recording.

### Installing dependencies
Install necessary dependencies with the following line. It is advised to use virtual environment.
```
pip install -r requierments.txt
```

### Creating the database
The necessary database and SIFT vocabulary can be created with the following command:
```
./indexer.py path/to/video/library
```
The result of this command would be the files `output.db` and `_sift_vocabulary.pkl`.
If a `_sift_vocabulary.pkl` file already exists it will be overridden. The last line is the filename of the result.

### Running a query
To run a query use the command:
```
./query.py path/to/query/video
```
In order to work the script should be in the same directory as `output.db` and `_sift_vocabulary.pkl`.

### Evaluating the system
To evaluate the system run the command:
```
./Evaluation.py path/to/test/videos/
```
The specified directory should have several videos as well as a file `groundTruth.txt` which contains on each line the correct filename that should be returned when running the query.
The files will be processed in lexicographical order.
At the end of the evaluation a score would be given which represents how many videos the system guessed correctly.


