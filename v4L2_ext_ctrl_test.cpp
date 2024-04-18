#include <iostream>
#include <string>
#include <cstring>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/videodev2.h>

int main() {
    // Open the device
    int fd = open("/dev/video2", O_RDWR);
    if (fd == -1) {
        perror("Opening video device");
        return 1;
    }

    struct v4l2_queryctrl qctrl;

    qctrl.id = V4L2_CTRL_FLAG_NEXT_CTRL;
    while (0 == ioctl(fd, VIDIOC_QUERYCTRL, &qctrl)) {
        if (qctrl.flags & V4L2_CTRL_FLAG_DISABLED) {
            std::cout << "Control " << qctrl.name << " is not supported" << std::endl;
        } else {
            std::cout << "Control " << qctrl.name << " is supported" << std::endl;
        }
        qctrl.id |= V4L2_CTRL_FLAG_NEXT_CTRL;
    }

    if (errno != EINVAL) {
        perror("VIDIOC_QUERYCTRL");
    }

    // Close the device
    close(fd);
    return 0;
}
