# PFAND Classifier
A CNN multi-class classifier recognising a price category of empty bottles deposits in German Pfand system, trained and tested on own dataset 

## Table of Contents
- [Dataset](https://github.com/marcinstopyra/pfand_clf#dataset)
- [Data preprocessing](https://github.com/marcinstopyra/pfand_clf#Data preprocessing)
- [Data labeling](https://github.com/marcinstopyra/pfand_clf#Data labeling)
- [CNN Classifier](https://github.com/marcinstopyra/pfand_clf#CNN Classifier)
- [TODOs](https://github.com/marcinstopyra/pfand_clf#TODOs)


## Dataset
The dataset contains >650 pictures of bottles/cans/empty slots in the box taken from above. Example samples:
![example sample](./graphics/example_samples.png)

All pictures show a single object in a box or outside, they are all preprocessed by code contained in [dataset_preprocessing_Pfand_clf.ipynb](https://github.com/marcinstopyra/pfand_clf/blob/master/dataset_preprocessing_Pfand_clf.ipynb) notebook (more about preprocessing in next section)


The dataset imperfections:
- Dataset is biased - it consists only photos collected by me and my friends, therefore the bottles on the photos are from drinks popular in our local community. Most of samples contain drinks produced in local area (Baden-Württemberg beers - Stuttgarter Hofbrau, Wulle, Das Echte etc.) and  popular among students (cheap beer brands like Oettinger, Club Mate softdrinks, redbull cans). More samples of new drinks should be added.
- Most of the photos were taken with the same devices - more photos from different devices should be added
- Dataset does not contain any plastic bottles (huge part of 25 cents deposit value category)


## Data preprocessing
Data preprocessing is conducted by the code from [dataset_preprocessing_Pfand_clf.ipynb](https://github.com/marcinstopyra/pfand_clf/blob/master/dataset_preprocessing_Pfand_clf.ipynb) notebook. The raw images are read from a raw_data folder, they are rotated if needed, resized to desired smaller size, cropped and saved in ready_data directory. The preprocessed raw samples are moved from raw_data folder to another backup folder.

## Data labeling
Samples were labeled manually with use of labeling tool created by GitHub user Dida-do [[GH repository](https://github.com/dida-do/public/tree/master/labelingtool)]. The programme was modified to meet the requirements of the project

## CNN Classifier
In the last notebook - [pfand_clf.ipynb](https://github.com/marcinstopyra/pfand_clf/blob/master/pfand_clf.ipynb) the CNN classifier is built. The dataset is split into train and test split containing:
- train set - 80% samples
- test set - 20% samples

The CNN model contains a data ugmentation submodel build of layers:
- RandomFlip
- RandomRotation
- RandomZoom

Final model hyperparameters:
- number of convolutional layers and number of filters in each of them,
- activation function
- batch size
- dropout layers

were optimised through randomized search conducted for 40 randomly chosen parameter sets from the parameter grid. Each of tested models was cross-validated on 3 KFolds.

The final model parameters:
- filters: [32, 64, 128, 256, 512],
- activation: 'relu',
- batch size: 32,
- no dropouts

The training was stopped after 28 epochs because the model started to overfit to training set. The tarining history graphs showed stable rise of validation accuracy and stable decrease in validation loss
![training history](./graphics/training_history.png)

**The test accuracy of final model was: 0.9781**

Confusion matrix was created to show which samples were mispredicted:

![confusion matrix](./graphics/confusion_matrix.png)

Mispredicted samples:

![misprediction](./graphics/mispredicted_samples.png)

## TODOs:
There are few extensions planned for the project:
- automatic labeling of new samples with use of semi-supervised learning (KMean clustering)
- development of an application that would take a picture of a box full of mixed pfand bottles/cans/empty slots, put a grid on it, classify each slot and calculate the summed up value of deposit
- deployment of programme mentioned above in form of web/mobile application