#include <pthread.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_LINE 3500000
#define MAX_LEN 2000
#define MAX_THREAD 10
#define MAX_K 10


struct Input {
    char *given, **begin, **end;
    int top_k;
};

struct Node {
    char *str;
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

void* work(void *ptr) {
    struct Input *data = (struct Input *)ptr;
    int i, j;


    char *tmp = (char*)malloc(MAX_LEN * sizeof(char));
    int l;


    struct Node *res = (struct Node *)malloc((data -> top_k) * sizeof(char *));
    for (i = 0; i < data -> top_k; i++) {
        res[i].str = (char *)malloc(MAX_LEN * sizeof(char));
        res[i].sim = 0;
    }

    char **candidate;
    for (candidate = data -> begin; *candidate && candidate != data -> end; candidate++) {

        strcpy(tmp, *candidate);
        l = strlen(tmp);

        for (i = l - 1; i >= 0; i--)
            if ((*candidate)[i] == '/') {
                for (j = i + 1; j < l - 1; j++) {
                    if ((*candidate)[j] == '_')
                        tmp[j - i - 1] = ' ';
                    else 
                        tmp[j - i - 1] = (*candidate)[j];
                }
                tmp[j - i - 1] = 0;
                break;
            }

        double cur_sim = calc_similarity(data -> given, tmp);
        if (cur_sim > res[0].sim) {
            strcpy(res[1].str, res[0].str);
            res[1].sim = res[0].sim;

            strcpy(res[0].str, *candidate);
            res[0].sim = cur_sim;
        }
        else if (cur_sim > res[1].sim) {
            strcpy(res[1].str, *candidate); // with urls
            res[1].sim = cur_sim;
        }
    }
    pthread_exit((void *)res);
}

char** find(const char* given, const char* file_path, int top_k) {

    int i;
    char **all_text = (char **)malloc(MAX_LINE * sizeof(char *));
    int tot = 0;

    FILE *fp = fopen(file_path, "r"); 
    char *tmp = (char*)malloc(MAX_LEN * sizeof(char));
    int l;

    while (~fscanf(fp, "%s", tmp)) {
        l = strlen(tmp);
        all_text[tot] = (char*)malloc((l + 1) * sizeof(char));
        strcpy(all_text[tot], tmp);
        tot++;
    }
    free(tmp);

    all_text[tot] = NULL;
    int per_thread_num = tot / MAX_THREAD + (int)(tot % MAX_THREAD != 0);
    
    pthread_t thread[MAX_THREAD];

    struct Input arg[MAX_THREAD];
    void *retVal[MAX_THREAD];

    for (i = 0; i < MAX_THREAD; i++) {
        arg[i].given = (char *)given;
        arg[i].begin = all_text + per_thread_num * i;
        arg[i].end = all_text + per_thread_num * (i + 1);

        arg[i].top_k = top_k;
        pthread_create(thread + i, NULL, (void *)&work, (void *)(arg + i));
    }

    for (i = 0; i < MAX_THREAD; i++) {
        pthread_join(thread[i], retVal + i);
        struct Node *res = (struct Node *)(retVal[i]);
        printf("%s %lf\n", res[0].str, res[0].sim);
        printf("%s %lf\n", res[1].str, res[1].sim);
    }
    
}

int main() {
    char *s = "1134 Kepler";
    char **res = find(s, "/home/litian/dbpedia/subject.txt", 2);
    return 0;
}

