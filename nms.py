import torch

from iou import intersection_over_union

def nms(
        bboxes,
        iou_threshold,
        threshold,
        box_format="corners"
):
    #Predictions = [[1,0.9,x1,y1,x2,y2]]

    assert type(bboxes) == list

    bboxes = [box for box in bboxes if box[1] > threshold] # Keep boxes above a probability threshold
    bboxes = sorted(bboxes, key=lambda x: x[1], reverse=True) # Sort boxes with the highest probability in the beginning
    bboxes_after_nms = []

    while bboxes:
        chosen_box = bboxes.pop(0) # choose box with highest score

        bboxes = [box for box in bboxes 
                    if box[0] != chosen_box[0] # if they are not of the same class
                    or intersection_over_union(
                        torch.tensor(chosen_box[2:]), # Remove first two elements (only need xy coordinates)
                        torch.tensor(box[2:]),
                        box_format=box_format,
                    )
                    < iou_threshold
        ]

        bboxes_after_nms.append(chosen_box)

    return bboxes_after_nms