#include <stdio.h>
#include <stdlib.h>

typedef struct {
    unsigned char r;
    unsigned char g;
    unsigned char b;
} int8_triple;

typedef struct {
    int m;
    int n;
    int8_triple * element;
} matrix;


int compose_cpu(matrix *m_1, matrix *m_2, matrix *m_out) {
    int m = m_1->m;
    int n = m_1->n;
    if ((m != m_2->m) || (n != m_2->n))
        return -1;
    for (int i=0; i<m; ++i) {
        for (int j=0; j<n; ++j) {
            int idx = i * n + j;
            m_out->element[idx].r = m_1->element[idx].r + m_2->element[idx].r;
            m_out->element[idx].g = m_1->element[idx].g + m_2->element[idx].g;
            m_out->element[idx].b = m_1->element[idx].b + m_2->element[idx].b;
        }
    }
    
    return 0;
}

