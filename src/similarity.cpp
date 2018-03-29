#include <iostream>
#include <fstream>
#include <cstring>

using namespace std;
#define min(x, y) ((x) < (y) ? (x) : (y))
#define max(x, y) ((x) > (y) ? (x) : (y))

double similarity(const char* str1, const char* str2)
{
    int n = strlen(str1);
    int m = strlen(str2);

    int **f = new int* [n + 1];
    for (int i = 0; i <= n; i++)
        f[i] = new int [m + 1];

    
    for (int i = 0; i <= n; i++)
        f[i][0] = i;
    for (int j = 0; j <= m; j++)
        f[0][j] = j;

    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++) {
            if (str1[i] == str2[j])
                f[i + 1][j + 1] = f[i][j];
            else
                f[i + 1][j + 1] = min(f[i + 1][j], min(f[i][j + 1], f[i][j])) + 1;
        }
    //if (f[n][m] > max(n, m))
        //printf("%d %d %d\n", f[n][m], n, m);
    int ret = f[n][m];
    for (int i = 0; i <= n; i++)
        delete [] f[i];
    delete [] f;
    return 1 - 1.0 * ret / max(n, m);
}

int main()
{

    const char* str1 = "1134 Kepler";
    FILE *fp = fopen("../../dbpedia/subject.text", "r");
    //ifstream fin("../../dbpedia/subject.text");

    char *tmp = new char [2000];
    int id = 0;
    while (~fscanf(fp, "%s", tmp))
    {
        int l = strlen(tmp);
        char *str2 = new char [l];
        for (int i = l - 1; i >= 0; i--)
            if (tmp[i] == '/') {
                for (int j = i + 1; j < l - 1; j++)
                    str2[j - i - 1] = tmp[j];
                break;
            }
	    /*
        double res = similarity(str1, str2);
        if(id % 10000 == 0)
            printf("%lf\n", res);
        if(res == 1)
            printf("%s\n", str2);
	    id += 1;
        */
    }
    delete [] tmp;
    fclose(fp);
    return 0;
}
