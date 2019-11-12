#include <stdio.h>
#include <stdlib.h>
#include <gsl/gsl_matrix.h>

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

gsl_matrix_uchar * m_1 = NULL;
gsl_matrix_uchar * m_2 = NULL;

int form_gsl_matricies(matrix *m1, matrix *m2) {
    int m = m1->m;
    int n = m1->n;
    if ((m != m2->m) || (n != m1->n))
        return -1;
    m_1 = gsl_matrix_uchar_alloc(m, n * 3);
    m_2 = gsl_matrix_uchar_alloc(m, n * 3);
    for (int i=0; i<m; ++i) {
        for (int j=0; j<n; ++j) {
            int idx = i * n + j;
            gsl_matrix_uchar_set(m_1, i, 3*j, m1->element[idx].r);
            gsl_matrix_uchar_set(m_1, i, 3*j + 1, m1->element[idx].g);
            gsl_matrix_uchar_set(m_1, i, 3*j + 2, m1->element[idx].b);

            gsl_matrix_uchar_set(m_2, i, 3*j, m2->element[idx].r);
            gsl_matrix_uchar_set(m_2, i, 3*j + 1, m2->element[idx].g);
            gsl_matrix_uchar_set(m_2, i, 3*j + 2, m2->element[idx].b);
        }
    }

    return 0;
}

int compose_gsl(matrix *mout, int inside) {
    if (!mout)
        return -1;
    int m = mout->m;
    int n = mout->n;
    gsl_matrix_uchar_add(m_1, m_2);
    if (inside)
        return 0;
    for (int i=0; i<m; ++i) {
        for (int j=0; j<n; ++j) {
            int idx = i * n + j;
            mout->element[idx].r = gsl_matrix_uchar_get(m_1, i, 3*j);
            mout->element[idx].g = gsl_matrix_uchar_get(m_1, i, 3*j + 1);
            mout->element[idx].b = gsl_matrix_uchar_get(m_1, i, 3*j + 2);
        }
    }

    return 0;
}

int free_gsl_matricies() {
    gsl_matrix_uchar_free(m_2);
    gsl_matrix_uchar_free(m_1);

    return 0;
}

