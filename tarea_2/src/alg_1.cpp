#include <vector>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <chrono>
#include <omp.h> 

struct MatView {
    double* data;
    int stride;
    int size;
    double& at(int i, int j) const { return data[i * stride + j]; }
    MatView sub(int r, int c, int s) const { return { data + r * stride + c, stride, s }; }
};

double det_value(int i, int j, double offset) {
    return std::sin(i * 0.1 + j * 0.3 + offset);
}

void init_matrix(std::vector<double>& M, int N, double offset) {
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            M[i * N + j] = det_value(i, j, offset);
        }
    }
}

void multiply_leaf(const MatView& A, const MatView& B, const MatView& C) {
    int s = C.size;

    #pragma omp parallel for schedule(static)
    for (int i = 0; i < s; ++i) {
        for (int k = 0; k < s; ++k) {
            double a = A.at(i, k);
            for (int j = 0; j < s; ++j) {
                C.at(i, j) += a * B.at(k, j);
            }
        }
    }
}

int main(int argc, char** argv) {
    int N = (argc > 1) ? std::atoi(argv[1]) : 2048;

    std::vector<double> A(N * N), B(N * N), C(N * N, 0.0);
    init_matrix(A, N, 1);
    init_matrix(B, N, 2);

    MatView Av{ A.data(), N, N }, Bv{ B.data(), N, N }, Cv{ C.data(), N, N };

    auto t0 = std::chrono::high_resolution_clock::now();
    multiply_leaf(Av, Bv, Cv);
    auto t1 = std::chrono::high_resolution_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();

    double checksum = 0.0;
    for (double v : C) {
        checksum += v;
    }

    std::printf("N=%d tiempo=%.2f ms checksum=%.6f\n", N, ms, checksum);
    return 0;
}
