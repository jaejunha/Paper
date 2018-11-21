#include "handover.h"

void testCase(int i) {

	cout << "Connection " << i << endl;

	// 4 UEs and 3 APs
	int_n = 4;
	int_m = 3;

	// Set connection
	setConnection(i);

	// Time slot of AP is 20
	int_t = 20;

	// Initialize AP vector
	for (int i = 1; i <= int_m; i++)
		vector_ap.push_back({ 0 });

	// Make UE
	for (int i = 1; i <= int_n; i++) {
		vector_sortedUE.push_back(i);
		vector_ue.push_back(makeUE());
	}

	// Sort UE with request bitrate
	sort(vector_sortedUE.begin(), vector_sortedUE.end(), sortUE);

	// Initialize optimized bitrate
	for (int i = 1; i <= int_n; i++)
		vector_optimizedBitrate.push_back({ 0 });

}

void setConnection(int i) {
	switch (i) {
	case 1:
		// UE 1 can be associated with AP 1
		bool_r[1][1] = true;

		// UE 2 can be associated with AP 1 and AP 3
		bool_r[2][1] = true;
		bool_r[2][3] = true;

		// UE 3 can be associated with AP 2 and AP 3
		bool_r[3][2] = true;
		bool_r[3][3] = true;

		// UE 4 can be associated with AP 3
		bool_r[4][3] = true;
		break;
	case 2:
		// UE 1 can be associated with AP 1
		bool_r[1][1] = true;

		// UE 2 can be associated with AP 3
		bool_r[2][3] = true;

		// UE 3 can be associated with AP 2
		bool_r[3][2] = true;

		// UE 4 can be associated with AP 3
		bool_r[4][3] = true;
		break;
	}
}

UE makeUE() {
	UE ue;
	vector<int> vector_rssi;

	ue.reqBitrate = int_bitrates[rand() % 5];
	vector_rssi.push_back(0);
	for (int i = 1; i <= int_m; i++)
		vector_rssi.push_back(-(rand() % 70 + 30));
	ue.rssi = vector_rssi;

	return ue;
}

void dfs(int int_ue) {

	// End of DFS
	if (int_ue == int_n + 1) {
		// Calculate difference of quality
		double double_difference = 0;
		for (int i = 1; i <= int_n; i++)
			double_difference += max(vector_ue[i].reqBitrate - vector_ue[i].bitrate, (double)0);

		cout << "difference: " << double_difference << "\t";
		cout << "[";
		for (int i = 1; i <= int_n; i++) {
			cout << "(UE" << i << "-AP" << vector_ue[i].ap << ", " << vector_ue[i].bitrate << "bps)";
			if (i <= int_n - 1)
				cout << ", ";
		}
		cout << "]" << endl;

		// If optimized value is needed to changed
		if (double_difference < double_optimizedDifference) {
			double_optimizedDifference = double_difference;
			for (int i = 1; i <= int_n; i++) {
				vector_optimizedBitrate[i] = vector_ue[i].bitrate;
				for (int j = 1; j <= int_m; j++)
					bool_optimizedP[i][j] = bool_p[i][j];
			}
		}

		return;
	}

	for (int i = 1; i <= int_m; i++) {

		// When cannot connect AP
		if (bool_r[vector_sortedUE[int_ue]][i] == false)
			continue;

		// When AP's time slot is full
		if (vector_ap[i].timeSlot == int_t)
			continue;

		bool_p[vector_sortedUE[int_ue]][i] = true;
		vector_ue[vector_sortedUE[int_ue]].ap = i;
		// Save values to restore later
		double double_ueQuality = vector_ue[vector_sortedUE[int_ue]].bitrate;
		double double_apTimeSlot = vector_ap[i].timeSlot;
		double double_ueTimeSlot = -vector_ue[vector_sortedUE[int_ue]].reqBitrate / vector_ue[vector_sortedUE[int_ue]].rssi[i];

		// AP has enough time slot
		if (double_ueTimeSlot + vector_ap[i].timeSlot <= int_t) {
			vector_ue[vector_sortedUE[int_ue]].bitrate = calQuality(vector_sortedUE[int_ue], double_ueTimeSlot, double_ueTimeSlot);
			vector_ap[i].timeSlot += double_ueTimeSlot;
		}
		// AP has small time slot
		else {
			vector_ue[vector_sortedUE[int_ue]].bitrate = calQuality(vector_sortedUE[int_ue], int_t - vector_ap[i].timeSlot, double_ueTimeSlot);
			// If find bitrate in MPD
			if (vector_ue[vector_sortedUE[int_ue]].bitrate)
				vector_ap[i].timeSlot = int_t;
		}

		// When Success, Check next UE
		if (vector_ue[vector_sortedUE[int_ue]].bitrate)
			dfs(int_ue + 1);

		vector_ue[vector_sortedUE[int_ue]].ap = 0;
		bool_p[vector_sortedUE[int_ue]][i] = false;
		// Retore values
		vector_ue[vector_sortedUE[int_ue]].bitrate = double_ueQuality;
		vector_ap[i].timeSlot = double_apTimeSlot;
	}
}