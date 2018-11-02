#include <iostream>
#include <algorithm>
#include <climits>
#include <vector>
using namespace std;

#define MAX_M 100
#define MAX_N 100
#define T 500

typedef struct UE {
	int timeSlot;
	double reqQuality;
	double quality;
	vector<int> rssi;
}UE;

typedef struct AP {
	int timeSlot;
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

void init();

void testCase(int i);
void callCase1();
void callCase2();

double calQuality(int int_ue, int int_availableTimeSlot);
void dfs(int int_ue);
void printResult();

int main() {

	for (int i = 1; i <= 2; i++) {
		// Initialize variables
		init();

		// Call test case
		testCase(i);

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
	switch (i) {
	case 1:
		callCase1();
		break;
	case 2:
		callCase2();
		break;
	}
}

void callCase1() {

	// 4 UEs and 3 APs
	int_n = 4;
	int_m = 3;

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

	// Time slot of AP is 8
	int_t = 8;

	// Initialize AP vector
	for (int i = 1; i <= int_m; i++)
		vector_ap.push_back({ 0 });

	UE ue;
	vector<int> vector_rssi;

	// UE 1
	ue.timeSlot = 4;
	ue.reqQuality = 4;
	vector_rssi.clear();
	vector_rssi.push_back(0);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	ue.rssi = vector_rssi;
	vector_ue.push_back(ue);

	// UE 2
	ue.timeSlot = 6;
	ue.reqQuality = 6;
	vector_rssi.clear();
	vector_rssi.push_back(0);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	ue.rssi = vector_rssi;
	vector_ue.push_back(ue);

	// UE 3
	ue.timeSlot = 4;
	ue.reqQuality = 4;
	vector_rssi.clear();
	vector_rssi.push_back(0);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	ue.rssi = vector_rssi;
	vector_ue.push_back(ue);

	// UE 4
	ue.timeSlot = 5;
	ue.reqQuality = 5;
	vector_rssi.clear();
	vector_rssi.push_back(0);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	ue.rssi = vector_rssi;
	vector_ue.push_back(ue);
}

void callCase2() {

	// 4 UEs and 3 APs
	int_n = 4;
	int_m = 3;

	// UE 1 can be associated with AP 1
	bool_r[1][1] = true;

	// UE 2 can be associated with AP 3
	bool_r[2][3] = true;

	// UE 3 can be associated with AP 2
	bool_r[3][2] = true;

	// UE 4 can be associated with AP 3
	bool_r[4][3] = true;

	// Time slot of AP is 8
	int_t = 8;

	// Initialize AP vector
	for (int i = 1; i <= int_m; i++)
		vector_ap.push_back({ 0 });

	UE ue;
	vector<int> vector_rssi;

	// UE 1
	ue.timeSlot = 4;
	ue.reqQuality = 4;
	vector_rssi.clear();
	vector_rssi.push_back(0);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	ue.rssi = vector_rssi;
	vector_ue.push_back(ue);

	// UE 2
	ue.timeSlot = 6;
	ue.reqQuality = 6;
	vector_rssi.clear();
	vector_rssi.push_back(0);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	ue.rssi = vector_rssi;
	vector_ue.push_back(ue);

	// UE 3
	ue.timeSlot = 4;
	ue.reqQuality = 4;
	vector_rssi.clear();
	vector_rssi.push_back(0);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	ue.rssi = vector_rssi;
	vector_ue.push_back(ue);

	// UE 4
	ue.timeSlot = 5;
	ue.reqQuality = 5;
	vector_rssi.clear();
	vector_rssi.push_back(0);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	vector_rssi.push_back(-30);
	ue.rssi = vector_rssi;
	vector_ue.push_back(ue);
}

double calQuality(int int_ue, int int_availableTimeSlot) {
	// Not implemented detaily

	return (double)int_availableTimeSlot;
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
		int int_apTimeSlot = vector_ap[i].timeSlot;

		// AP has enough time slot
		if (vector_ue[int_ue].timeSlot + vector_ap[i].timeSlot <= int_t) {
			vector_ue[int_ue].quality = calQuality(int_ue, vector_ue[int_ue].timeSlot);
			vector_ap[i].timeSlot += vector_ue[int_ue].timeSlot;
		}
		// Not implemented
		else {
			vector_ue[int_ue].quality = calQuality(int_ue, int_t - vector_ap[i].timeSlot);
			vector_ap[i].timeSlot = int_t;
		}

		// Check next UE
		dfs(int_ue + 1);

		bool_p[int_ue][i] = false;
		// Retore values
		vector_ue[int_ue].quality = double_ueQuality;
		vector_ap[i].timeSlot = int_apTimeSlot;
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
	cout << endl;
}