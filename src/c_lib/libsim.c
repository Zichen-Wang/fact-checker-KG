#include <stdio.h>
#include <string.h>
#include <stdlib.h>

struct Node {
    char* name;
    double sim;
};
    

int min(int x, int y) {
    return x < y ? x : y;
}

int max(int x, int y) {
    return x > y ? x : y;
}

double calc_similarity(const char* given, const char* candidate) {
    int n = strlen(given);
    int m = strlen(candidate);
    int i, j, ret;

    int **f = (int**)malloc((n + 1) * sizeof(int*));
    for (i = 0; i <= n; i++)
        f[i] = (int*)malloc((m + 1) * sizeof(int));

    
    for (i = 0; i <= n; i++)
        f[i][0] = i;
    for (j = 0; j <= m; j++)
        f[0][j] = j;

    for (i = 0; i < n; i++)
        for (j = 0; j < m; j++) {
            if (given[i] == candidate[j])
                f[i + 1][j + 1] = f[i][j];
            else
                f[i + 1][j + 1] = min(f[i + 1][j], min(f[i][j + 1], f[i][j])) + 1;
        }
    
    ret = f[n][m];
    for (i = 0; i <= n; i++)
        free(f[i]);
    free(f);
    return 1 - 1.0 * ret / max(n, m);
}

char** find(const char* given, const char* file_path, int k) {  // find top-k max similarities
    
    FILE *fp = fopen(file_path, "r"); 
    char *tmp = (char*)malloc(2000 * sizeof(char));
    //char *tmp_ = (char*)malloc(2000 * sizeof(char));
    int i, j, l;
    char *ans1 = (char *)malloc(2000 * sizeof(char));
    char *ans2 = (char *)malloc(2000 * sizeof(char));

    double first_max = 0;
    double second_max = 0;

    while (~fscanf(fp, "%s", tmp)) {
        
        l = strlen(tmp);
        //for (i = 0; i < l ; i++) {tmp_[i] = tmp[i];}
        //printf("%s\n", tmp_);
        char *candidate = (char*)malloc((l + 1) * sizeof(char));
        for (i = l - 1; i >= 0; i--)
            if (tmp[i] == '/') {
                for (j = i + 1; j < l - 1; j++) {
                    if (tmp[j] == '_')
                        //tmp[j] = ' ';
                        candidate[j - i - 1] = ' ';
                    else 
                        candidate[j - i - 1] = tmp[j];
                }
                candidate[j - i - 1] = 0;
                break;
            }
        double cur = calc_similarity(given, candidate);
        if (cur > first_max) {
            second_max = first_max;
            first_max = cur;
            strcpy(ans2, ans1);
            strcpy(ans1, tmp);  // with urls
        }
        else if (cur > second_max) {
            second_max = cur;
            strcpy(ans2, tmp); // with urls
        }
        free(candidate);
    }
    char** final = (char **)malloc(sizeof(char *) * k);
    
    i = 0;
    for (i = 0; i < k; i++) {
        final[i] = (char*) malloc(sizeof(char) * 2000);
    }

    strcpy(final[0], ans1);
    strcpy(final[1], ans2);
    
    free(ans1);
    free(ans2);
    free(tmp);

    fclose(fp);

    return final;
}


