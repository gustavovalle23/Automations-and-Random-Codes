import cv2
import numpy as np
from collections import Counter


def transform_to_paint_by_numbers(image_path, num_colors=5):
    # Read the input image
    image = cv2.imread(image_path)

    # Resize the image for faster processing
    scale_percent = 100  # adjust as needed
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    # Convert the image to a numpy array
    image_np = np.array(resized_image)

    # Apply k-means clustering to segment the image
    pixel_values = image_np.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, center = cv2.kmeans(
        pixel_values, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )

    # Convert the centers to integer values
    center = np.uint8(center)

    # Flatten the labels array and reshape it to the original image shape
    labels = labels.flatten()
    segmented_image = center[labels.flatten()]
    segmented_image = segmented_image.reshape(resized_image.shape)

    # Get the counts of each color segment
    label_counts = Counter(labels)
    total_pixels = resized_image.shape[0] * resized_image.shape[1]

    # Display the colors and their corresponding segment areas
    print("Colors and their corresponding segment areas:")
    for idx, count in label_counts.items():
        color = center[idx]
        color_percentage = (count / total_pixels) * 100
        print(f"{idx+1} - Color {color}: {color_percentage:.2f}%")
        # Find contours for each color segment
        mask = np.uint8(labels == idx)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Calculate centroid of the contour
        if contours:
            M = cv2.moments(contours[0])
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                # Add the color number to the segmented image
                cv2.putText(
                    segmented_image,
                    str(idx + 1),
                    (cX, cY),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2,
                )

    # Display the segmented image
    cv2.imshow("Segmented Image", segmented_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the segmented image
    cv2.imwrite("segmented_image.jpg", segmented_image)


# Example usage
transform_to_paint_by_numbers("input2.png", num_colors=12)
