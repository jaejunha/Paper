#pragma once
#ifndef __HANDOVER_H__
#define __HANDOVER_H__

#include <iostream>
#include <climits>
#include <cstdlib>
#include <ctime>
#include <vector>
#include <algorithm>
#include <cmath>

using namespace std;

#define MAX_M 100
#define MAX_N 100
#define T 500

typedef struct UE {
	double reqBitrate;
	double reqQuality;
	double bitrate;
	double quality;
	int ap;
	vector<int> rssi;
}UE;

typedef struct AP {
	double timeSlot;
}AP;

extern int int_m, int_n, int_t;

extern double double_optimizedDifference;
extern bool bool_optimizedP[MAX_N + 1][MAX_M + 1];
extern vector<int> vector_optimizedBitrate;

extern bool bool_r[MAX_N + 1][MAX_M + 1], bool_p[MAX_N + 1][MAX_M + 1];

extern vector<UE> vector_ue;
extern vector<AP> vector_ap;
extern vector<int> vector_sortedUE;

extern int int_bitrates[5];

extern clock_t timer_start, timer_end;

extern bool bool_end;

void init();
bool sortUE(int i, int j);
void testCase(int i);
void setConnection(int i);
UE makeUE();

void printInfo();
double calQuality(int bitRate);
int findBitrate(int int_ue, double double_availableTimeSlot, double double_maxTimeSlot);
void dfs(int int_ue);
void printResult();

#endif