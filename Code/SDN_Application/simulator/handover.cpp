#include "handover.h"

/**************************************************************************
int_m: # of AP
int_n: # of UE
int_t: maximum time slot
**************************************************************************/
int int_m, int_n, int_t;

/**************************************************************************
Optimized value

double_optimizedDifference: optimized difference
bool_optimizedP: optimized p
vector_optimizedBitrate: optimized bitrate
**************************************************************************/
double double_optimizedDifference;
bool bool_optimizedP[MAX_N + 1][MAX_M + 1];
vector<int> vector_optimizedBitrate;

/**************************************************************************
Relation between UE and AP

bool_r: whether reachable or not
bool_p: status of connection
**************************************************************************/
bool bool_r[MAX_N + 1][MAX_M + 1], bool_p[MAX_N + 1][MAX_M + 1];

/**************************************************************************
Information of UE and AP

vector_ue: list of UE information
vector_ap: list of AP information
vector_sortedUE: sorted list of ue information in terms of required bitrate
**************************************************************************/
vector<UE> vector_ue;
vector<AP> vector_ap;
vector<int> vector_sortedUE;

/**************************************************************************
MPD bitrates
**************************************************************************/
int int_bitrates[] = { 240,360,480,720,1080 };

/**************************************************************************
To measure time
**************************************************************************/
clock_t timer_start, timer_end;

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

		// Start timer
		timer_start = clock();

		// Start to find optimalized value
		dfs(1);

		// Finish timer
		timer_end = clock();

		// Print result
		printResult();
	}

	getchar();

	return 0;
}