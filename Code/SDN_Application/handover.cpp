#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

#define MAX_M 100
#define MAX_N 100
#define T 500

typedef struct UE {
	int t;
	double q;
}UE;

double double_quality[MAX_M + 1][MAX_N + 1][T + 1];
double double_qualityT[MAX_M + 1][MAX_N + 1][T + 1];
int int_m, int_n;
bool p[MAX_M + 1][MAX_N + 1];
vector<UE> vector_ue;

void init();
void copy(bool bool_save);
void handover();

int main() {

	init();
	handover();

	return 0;
}

void init() {
	for (int i = 0; i <= int_m; i++)
		for (int j = 0; j <= int_n; j++)
			for (int k = 0; k <= T; k++)
				double_quality[i][j][k] = 0;
}

void copy(bool bool_save) {
	for (int i = 0; i <= int_m; i++)
		for (int j = 0; j <= int_n; j++)
			for (int k = 0; k <= T; k++) {
				if (bool_save)
					double_quality[i][j][k] = double_qualityT[i][j][k] = 0;
				else
					double_qualityT[i][j][k] = double_quality[i][j][k] = 0;
			}
}

void handover() {

	bool bool_save;
	double double_temp;
	int int_max;

	for (int i = 0; i <= int_n; i++) {
		for (int j = 0; j <= T; j++) {
			int_max = 0;
			for (int k = 0; k <= int_m; k++) {
				bool_save = false;
				copy(bool_save);

				/* 경계값은 건너 뜀 */
				if (!i || !j || !k)
					continue;

				/* AP랑 UE랑 연결 되어 있지 않으면 건너 뜀 */
				if (!p[k][i])
					continue;

				/* 여분의 Time slot이 없는 경우 */
				if (vector_ue[i - 1].t > j)
					double_qualityT[k][i][j] = double_qualityT[k][i - 1][j];

				/* 여분의 Time slot이 있는 경우 */
				else {
					double_temp = double_qualityT[k][i - 1][j - vector_ue[i - 1].t] + vector_ue[i - 1].q;
					if (double_qualityT[k][i - 1][j] < double_temp) {
						if (double_qualityT[k][int_max][j] < double_temp) {
							double_qualityT[k][int_max][j] = double_qualityT[k][int_max - 1][j];
							int_max = i;
							double_qualityT[k][int_max][j] = max(double_qualityT[k][i - 1][j], double_temp);
						}
					}
				}
			}
			bool_save = true;
			copy(bool_save);
		}
	}
}