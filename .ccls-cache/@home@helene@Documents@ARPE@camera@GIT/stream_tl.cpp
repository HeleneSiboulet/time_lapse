#include <opencv2/opencv.hpp>
#include <iostream>

int main() {
    // Open the default camera
    cv::VideoCapture capture(0);
    if (!capture.isOpened()) {
        std::cerr << "ERROR: Could not open camera" << std::endl;
        return 1;
    }

    // Set the resolution to 1280x960
    capture.set(cv::CAP_PROP_FRAME_WIDTH, 1280);
    capture.set(cv::CAP_PROP_FRAME_HEIGHT, 960);

    // Define the codec and create VideoWriter object
    int codec = cv::VideoWriter::fourcc('M', 'J', 'P', 'G');
    cv::VideoWriter video("output.avi", codec, 10, cv::Size(1280, 960));

    if (!video.isOpened()) {
        std::cerr << "Could not open the output video file for write\n";
        return -1;
    }

    // Capture and write video
    cv::Mat frame;
    while (true) {
        capture >> frame;
        if (frame.empty()) {
            std::cerr << "ERROR: Could not grab a frame" << std::endl;
            break;
        }

        video.write(frame);

        // Show the frame in a window
        cv::imshow("Webcam", frame);

        // Break out of the loop if the user presses the 'q' key
        if (cv::waitKey(10) == 'q') {
            break;
        }
    }

    // Release the VideoCapture and VideoWriter objects
    capture.release();
    video.release();

    // Close all OpenCV windows
    cv::destroyAllWindows();

    return 0;
}
