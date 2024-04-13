import logging
import click
import numpy as np
from PIL import Image, ImageDraw
import deeplake
import json

logging.basicConfig(level=logging.INFO)


def visualize(deeplake_path: str, saved_path: str, anotation_path: str) -> None:
    """
    Visualize an image

    Parameters:
        deeplake_path (str): Path to the deeplake dataset
        saved_path (str): Saved path for visualize result
    """
    logging.info("Load Deep Lake dataset")
    ds = deeplake.load(deeplake_path)
    print(ds)
    logging.info("Load successfully")
    # ds.visualize()
    
    for ind, image in enumerate(ds.images):
        print("========index===========", ind)
        # Draw bounding boxes for the fourth image
        img = Image.fromarray(image.numpy())
        
        # draw = ImageDraw.Draw(img)
        # (w,h) = img.size
        box = ds.boxes[ind].numpy()
        
        name = f"celeb_{ind}"
        x1 = int(box[0][0])
        y1 = int(box[0][1])
        x2 = x1 + int(box[0][2])
        y2 = y1 + int(box[0][3])
        # draw.rectangle([x1,y1,x2,y2], width=2)

        img.save(saved_path + f"/{name}.jpg")
        
        json_ano = {"label": "face",
                    "object_id":f"{ind}",
                    "box": f"[{x1}, {y1}, {x2}, {y2}]",
                    "confidence": str(1.0)}
        # Serializing json
        json_object = json.dumps(json_ano, indent=4)
        
        # Writing to sample.json
        with open(f"{anotation_path}/{name}.json", "w") as outfile:
            outfile.write(json_object)
        
        logging.info(f"Image saved at {saved_path + '/test_img.jpg'}")

if __name__ == "__main__":
    visualize(deeplake_path="hub://activeloop/celeb-a-val", saved_path="images", anotation_path="anotations")