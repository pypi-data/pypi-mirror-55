# Face Classification

Face classification is a simple package running on top of [face_recognition](https://pypi.org/project/face_recognition/) package which automates the training process and helps in easily getting the prediction. This could be a helpful addition to developers looking forward to adding the face recognition functionality in their projects.

It uses KNN algorithm and the model provided by face_recognition which spits out a vector of 128 length. Face classification has setup all the things to train and predict faces with optimum precision.

## Installing

```bash
pip install face-classification
```

## Setting up locally

```bash
git clone git@gitlab.lftechnology.com:leapfrogai/face-classification.git
```

## Setting up requirements

```bash
pip install -r requirements.txt
```

## A simple example

```py
# To train create a directory with images stored in sub directories and the label as the folder name
from face_classification import train, FaceClassifier, load_image_file, get_face_boundings, get_fae_embeddings

train(train_dir='path_to/directories_containing/sub_folders_with_labels_as_folder_name', 
            model_file_name='model_dir'
)

# Initialize object with path of the saved model in above step
# It can also be initialized without any model to get boundings and embeddings only by not passing any arguements below.
face_classifier = FaceClassifier('model_dir')

image = load_image_file('image/path')

# Get the predictions of all the faces in the image directly
predictions = face_classifier.predict(image)

# For more flexibility we can use the following functionality 
# Get the face boundings of faces in image
boundings = get_face_boundings(image)

# Get the embeddings of the face from the cropped face image from boundings
embeddings = get_face_embeddings(image, boundings)

# Get the prediciton from embeddings
predictions = face_classifier.classify_face(embeddings)
```

## Unsupervised Clustering

Face classification requires well labeled dataset, so to assist with the training, this package includes image clustering module based on unsupervised clustering using [chinese whispers algorithm](https://en.wikipedia.org/wiki/Chinese_Whispers_(clustering_method)).

```py
from face_classification import cluster_faces

# Cluster the given unknown faces and save clusters in their unique folders.
# The threshold_distance is an euclidean distance that determines whether a face falls into a cluster or not.
cluster_faces(path/to/unknown/images/folder, path/to/output/folder, threshold_distance=0.4)
```

## Object-tracking and achieving better FPS

An [example of face recognition using centroid tracking](./examples/webcam_demo_centroid_tracking.ipynb) has been added as a folder ```examples``` we demonstrate how better rate of FPS could be achieved using the object-tracking.

## Relaying frames to another computer using sockets

We have made available a simple socket programming functionality which helps user send frames to-and-fro with any computer.

### Example

```py
import cv2
import time
from face_classification import StreamFrame, ViewStream

# Initialize receiving port and sending IP plus sending port
view = ViewStream(4323)
send = StreamFrame('',4323)

cap = cv2.VideoCapture(0)
time.sleep(1)

while True:
    _,frame = cap.read()

    # Sending frames to the socket one by one 
    send.stream_frame(frame)

    # Receiving frames one by one from the socket
    returned_frame = view.get_frame()

    # Displaying the frames 
    cv2.imshow('frame', returned_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
```

## Relaying only the predictions rather than frames using sockets

User has also the option to send only the predictions rather than sending whole frames, which can come in handy if user requires only  the predictions rather than frames pre-printed with predictions and also if there is need to stream larger frames and bandwith wont allow it in real time.

### Example

```py
import cv2
import time

from face_classification import StreamFrame, RecognitionServer

PORT = 4959

server = RecognitionServer('trained_knn_model_77.clf', PORT)

stream = StreamFrame('',PORT)

cap = cv2.VideoCapture(0)
time.sleep(1)

while True:
    _,frame = cap.read()
    frame = cv2.resize(frame, (320, 240))

    # Sending frames to the socket one by one 
    stream.stream_frame(frame)

    # Taking single frame and returning the predictions to socket
    server.recognize()

    # Receiving frames one by one from the socket
    returned_ = stream.receive()

    print(returned_)
```

## License

Apache License 2
