#include <iostream>
#include <climits>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <algorithm>
using namespace std;

#define MAX_M 100
#define MAX_N 100
#define T 500

typedef struct UE {
	double reqQuality;
	double quality;
	vector<int> rssi;
}UE;

typedef struct AP {
	double timeSlot;
}AP;

/*
int_m: # of AP
int_n: # of UE
int_t: maximum time slot
*/
int int_m, int_n, int_t;

/*
Optimized value

double_optimizedDifference: optimized difference
bool_optimizedP: optimized p
*/
double double_optimizedDifference;
bool bool_optimizedP[MAX_N + 1][MAX_M + 1];

/*
Relation between UE and AP

bool_r: whether reachable or not
bool_p: status of connection
*/
bool bool_r[MAX_N + 1][MAX_M + 1], bool_p[MAX_N + 1][MAX_M + 1];

vector<UE> vector_ue;
vector<AP> vector_ap;

int int_bitrates[] = { 240,360,480,720,1080 };

void init();

void testCase(int i);
void setConnection(int i);
UE makeUE();

void printInfo();
int calQuality(int int_ue, double double_availableTimeSlot, double double_maxTimeSlot);
void dfs(int int_ue);
void printResult();

int main() {

	// For random value
	srand((unsigned)time(NULL));

	for (int i = 1; i <= 2; i++) {
		// Initialize variables
		init();

		// Call test case
		testCase(i);

		// Print info
		printInfo();

		// Start to find optimalized value
		dfs(1);

		// Print result
		printResult();
	}

	getchar();

	return 0;
}

void init() {

	// Initialize difference of quality
	double_optimizedDifference = LDBL_MAX;

	// Initialize UE and AP
	vector_ue.clear();
	vector_ap.clear();

	// For convenience
	vector_ue.push_back({ 0 });
	vector_ap.push_back({ 0 });

	// Initialize status of connection
	for (int i = 1; i <= int_n; i++) {
		for (int j = 1; j <= int_m; j++)
			bool_optimizedP[i][j] = bool_p[i][j] = bool_r[i][j] = false;
	}
}

void testCase(int i) {

	cout << "Test Case " << i << endl;

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
	for (int i = 1; i <= int_n; i++)
		vector_ue.push_back(makeUE());
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

	ue.reqQuality = int_bitrates[rand() % 5];
	vector_rssi.push_back(0);
	for (int i = 1; i <= int_m; i++)
		vector_rssi.push_back(-(rand() % 70 + 30));
	ue.rssi = vector_rssi;

	return ue;
}

void printInfo() {
	cout << "==========================================" << endl;
	for (int i = 1; i <= int_n; i++) {
		cout << "UE " << i << "(wants " << vector_ue[i].reqQuality << "bps) can be associated with";
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

int calQuality(int int_ue, double double_availableTimeSlot, double double_maxTimeSlot) {
	// Not implemented detaily

	// When there is enough time slot
	if (double_availableTimeSlot == double_maxTimeSlot)
		return vector_ue[int_ue].reqQuality;

	double double_tempQuality = vector_ue[int_ue].reqQuality * double_availableTimeSlot / double_maxTimeSlot;
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
void dfs(int int_ue) {

	// End of DFS
	if (int_ue == int_n + 1) {
		// Calculate difference of quality
		double double_difference = 0;
		for (int i = 1; i <= int_n; i++)
			double_difference += max(vector_ue[i].reqQuality - vector_ue[i].quality, (double)0);

		// If optimized value is needed to changed
		if (double_difference < double_optimizedDifference) {
			double_optimizedDifference = double_difference;
			for (int i = 1; i <= int_n; i++) {
				for (int j = 1; j <= int_m; j++)
					bool_optimizedP[i][j] = bool_p[i][j];
			}
		}
	}

	for (int i = 1; i <= int_m; i++) {

		// When cannot connect AP
		if (bool_r[int_ue][i] == false)
			continue;

		// When AP's time slot is full
		if (vector_ap[i].timeSlot == int_t)
			continue;

		bool_p[int_ue][i] = true;
		// Save values to restore later
		double double_ueQuality = vector_ue[int_ue].quality;
		double double_apTimeSlot = vector_ap[i].timeSlot;
		double double_ueTimeSlot = -vector_ue[int_ue].reqQuality / vector_ue[int_ue].rssi[i];
		// AP has enough time slot
		if (double_ueTimeSlot + vector_ap[i].timeSlot <= int_t) {
			vector_ue[int_ue].quality = calQuality(int_ue, double_ueTimeSlot, double_ueTimeSlot);
			vector_ap[i].timeSlot += double_ueTimeSlot;
		}
		// AP has small time slot
		else {
			vector_ue[int_ue].quality = calQuality(int_ue, int_t - vector_ap[i].timeSlot, double_ueTimeSlot);
			// If find bitrate in MPD
			if (vector_ue[int_ue].quality)
				vector_ap[i].timeSlot = int_t;
		}

		// When Success, Check next UE
		if (vector_ue[int_ue].quality)
			dfs(int_ue + 1);

		bool_p[int_ue][i] = false;
		// Retore values
		vector_ue[int_ue].quality = double_ueQuality;
		vector_ap[i].timeSlot = double_apTimeSlot;
	}
}

void printResult() {
	if (double_optimizedDifference == DBL_MAX)
		cout << "Fail to optimize" << endl;
	else {
		cout << "Optimized difference of quality: " << double_optimizedDifference << endl;
		cout << "Optimized connection:" << endl;
		for (int i = 1; i <= int_n; i++) {
			cout << "UE " << i << " is associated with AP ";
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