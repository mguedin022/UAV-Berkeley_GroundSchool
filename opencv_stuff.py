import cv2
import numpy as np
from pathlib import Path


def detect_blobs_doh(
    image,
    min_sigma=1.0,
    max_sigma=24.0,
    num_scales=18,
    threshold_rel=0.1,
):
    """Detect blob centers as local maxima of the scale-normalized Hessian determinant."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0
    sigmas = np.geomspace(min_sigma, max_sigma, num_scales)
    responses = []

    for sigma in sigmas:
        smoothed = cv2.GaussianBlur(
            gray, (0, 0), sigmaX=float(sigma), sigmaY=float(sigma)
        )
        dxx = cv2.Sobel(smoothed, cv2.CV_32F, 2, 0, ksize=3)
        dyy = cv2.Sobel(smoothed, cv2.CV_32F, 0, 2, ksize=3)
        dxy = cv2.Sobel(smoothed, cv2.CV_32F, 1, 1, ksize=3)
        responses.append((dxx * dyy - dxy * dxy) * float(sigma**4))

    response_volume = np.stack(responses)
    threshold = float(response_volume.max()) * threshold_rel
    candidates = []

    for scale_index, response in enumerate(responses):
        spatial_max = cv2.dilate(response, np.ones((3, 3), dtype=np.uint8))
        is_maximum = response >= spatial_max

        if scale_index > 0:
            lower_scale_max = cv2.dilate(
                responses[scale_index - 1], np.ones((3, 3), dtype=np.uint8)
            )
            is_maximum &= response >= lower_scale_max
        if scale_index + 1 < len(responses):
            upper_scale_max = cv2.dilate(
                responses[scale_index + 1], np.ones((3, 3), dtype=np.uint8)
            )
            is_maximum &= response >= upper_scale_max

        ys, xs = np.where(is_maximum & (response > threshold))
        for x, y in zip(xs, ys):
            candidates.append(
                (float(response[y, x]), int(x), int(y), float(sigmas[scale_index]))
            )

    candidates.sort(reverse=True)
    blobs = []
    for strength, x, y, sigma in candidates:
        radius = sigma * np.sqrt(2.0)
        if any(
            np.hypot(x - other_x, y - other_y)
            < 0.5 * (radius + other_radius)
            for _, other_x, other_y, other_radius in blobs
        ):
            continue
        blobs.append((strength, x, y, float(radius)))

    return blobs


def main():
    image_path = Path(__file__).resolve().parent / "polka_dots_3.jpg"
    image = cv2.imread(str(image_path))
    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    blobs = detect_blobs_doh(image)
    output = image.copy()
    for _, x, y, radius in blobs:
        cv2.circle(output, (x, y), max(1, round(radius)), (0, 0, 255), 2)
        cv2.circle(output, (x, y), 2, (255, 0, 0), -1)

    print(f"Detected {len(blobs)} blobs using the Determinant of Hessian.")
    cv2.imshow("Determinant of Hessian blob detection", output)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
