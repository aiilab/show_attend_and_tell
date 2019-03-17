import os
import numpy as np
import pandas as pd
import json


def build_dataset(ann_path, save_path):
    annotations = json.load(open(ann_path, "r"))

    # convert dictionary: image path -> image ID
    name2id = {}
    for i in range(len(annotations["images"])):
        name = annotations["images"][i]["file_name"]
        img_id = annotations["images"][i]["id"]
        name2id[name] = img_id

    # convert dictionary: image ID -> caption
    id2cap = {}
    for i in range(len(annotations["annotations"])):
        img_id = annotations["annotations"][i]["image_id"]
        caption = annotations["annotations"][i]["caption"]
        id2cap[img_id] = caption

    # build dataset with two columns (image file path, answer caption)
    dataset_dictlst = {"file_name": [], "caption": []}
    for i in range(len(annotations["images"])):
        file_name = annotations["images"][i]["file_name"]
        if os.path.exists(os.path.join(root_img_dirc, file_name)):
            dataset_dictlst["file_name"].append(file_name)
            img_id = name2id[file_name]
            caption = id2cap[img_id]
            dataset_dictlst["caption"].append(caption)

    # save dataset
    dataset_df = pd.DataFrame(dataset_dictlst)
    dataset_df.to_csv(save_path, index=False)


if __name__ == "__main__":
    # training dataset
    train_path = "../data/annotations/captions_train2014.json"
    save_train_path = "../data/label/train.csv"
    build_dataset(train_path, save_train_path)
    
    # validation dataset
    val_path = "../data/annotations/captions_val2014.json"
    save_val_path = "../data/label/val.csv"
    build_dataset(val_path, save_val_path)