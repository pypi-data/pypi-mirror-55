# ImageTransform
Image processing and transformation helper.

Preprocessing input images and adding transformations for better training data and for preparing input images to be used in image classifiers.


## How to use:

Here is the original image that we're gonna use in this example:

![original sample](sample-images/sample.jpg)



#### `center_crop`
##### crops an image from the center by the input size

```python
from image_transform import ImageTransform

transform = ImageTransform('sample-images/sample.jpg')
center_cropped_image = transform.center_crop(150)
center_cropped_image.save('sample-images/center_cropped_image.jpg')
```
![cropped sample](sample-images/center_cropped_image.jpg)



#### `horizontal_flip`
##### flips an image horizontally

```python
from image_transform import ImageTransform

transform = ImageTransform('sample-images/sample.jpg')
horizontally_flipped_image = transform.horizontal_flip()
horizontally_flipped_image.save('sample-images/horizontally_flip_image.jpg')
```
![cropped sample](sample-images/horizontally_flipped_image.jpg)



#### `scale`
##### scales an image shortest's side while keeping the same aspect ratio.

```python
from image_transform import ImageTransform

transform = ImageTransform('sample-images/sample.jpg')
scaled_image = transform.scale(650)
scaled_image.save('sample-images/scaled_image.jpg')
```
![cropped sample](sample-images/scaled_image.jpg)
