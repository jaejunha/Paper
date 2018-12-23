package kr.ac.postech.util;

import kr.ac.postech.object.MPD;
import kr.ac.postech.object.UE;

public class Util {
    public static double calQuality(int bitrate) {
        int a = 1, b = 1;
        return a * Math.log(1 + b * bitrate);
    }

    public static int findBitrate(UE ue, double double_availableTimeSlot, double double_maxTimeSlot) {

        // When there is enough time slot
        if (double_availableTimeSlot == double_maxTimeSlot)
            return ue.getReqBitrate();

        double double_tempQuality = ue.getReqBitrate() * double_availableTimeSlot / double_maxTimeSlot;
        int left = 0;
        int max = MPD.bitrates.length - 1;
        int right = max;
        int mid;

        while (left <= right) {

            mid = (left + right) / 2;

            if (MPD.bitrates[mid] > double_tempQuality)
                right = mid - 1;
            else {
                if (mid < max) {
                    if (double_tempQuality < MPD.bitrates[mid + 1])
                        return MPD.bitrates[mid];
                }
                left = mid + 1;
            }
        }

        return 0;
    }
}
