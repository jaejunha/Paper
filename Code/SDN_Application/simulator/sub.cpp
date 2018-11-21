#include "handover.h"

void init() {

	// Initialize difference of quality
	double_optimizedDifference = LDBL_MAX;

	// Initialize UE and AP
	vector_ue.clear();
	vector_sortedUE.clear();
	vector_ap.clear();
	vector_optimizedBitrate.clear();

	// For convenience
	vector_ue.push_back({ 0 });
	vector_sortedUE.push_back(0);
	vector_ap.push_back({ 0 });
	vector_optimizedBitrate.push_back({ 0 });

	// Initialize status of connection
	for (int i = 1; i <= int_n; i++) {
		for (int j = 1; j <= int_m; j++)
			bool_optimizedP[i][j] = bool_p[i][j] = bool_r[i][j] = false;
	}
}

bool sortUE(int i, int j) {
	return vector_ue[i].reqBitrate < vector_ue[j].reqBitrate;
}

int calQuality(int int_ue, double double_availableTimeSlot, double double_maxTimeSlot) {
	// Not implemented detaily

	// When there is enough time slot
	if (double_availableTimeSlot == double_maxTimeSlot)
		return vector_ue[int_ue].reqBitrate;

	double double_tempQuality = vector_ue[int_ue].reqBitrate * double_availableTimeSlot / double_maxTimeSlot;
	int left = 0;
	int max = sizeof(int_bitrates) / sizeof(int) - 1;
	int right = max;
	int mid;

	while (left <= right) {

		mid = (left + right) / 2;

		if (int_bitrates[mid] > double_tempQuality)
			right = mid - 1;
		else {
			if (mid < max) {
				if (double_tempQuality < int_bitrates[mid + 1])
					return int_bitrates[mid];
			}
			left = mid + 1;
		}
	}

	return 0;
}

void printInfo() {
	cout << "==========================================" << endl;
	for (int i = 1; i <= int_n; i++) {
		cout << "UE " << i << "(wants " << vector_ue[i].reqBitrate << "bps) can be associated with";
		int int_count = 0;
		for (int j = 1; j <= int_m; j++) {
			if (bool_r[i][j]) {
				if (int_count++)
					cout << ",";
				cout << " AP " << j << "(" << vector_ue[i].rssi[j] << "dB)";
			}
		}
		cout << endl;
	}
	cout << "------------------------------------------" << endl;
}

void printResult() {
	if (double_optimizedDifference == DBL_MAX)
		cout << "Fail to optimize" << endl;
	else {
		cout << "------------------------------------------" << endl;
		cout << "It took " << (double)(timer_end - timer_start) / 1000 << "sec " << endl;
		cout << "Optimized difference of bitrate: " << double_optimizedDifference << endl;
		cout << "Optimized connection ¡å" << endl;
		for (int i = 1; i <= int_n; i++) {
			cout << "UE " << i << "(" << vector_optimizedBitrate[i] << "bps) is associated with AP ";
			for (int j = 1; j <= int_m; j++) {
				if (bool_optimizedP[i][j]) {
					cout << j << endl;
					break;
				}
			}
		}
	}
	cout << "==========================================" << endl;
	cout << endl;
}