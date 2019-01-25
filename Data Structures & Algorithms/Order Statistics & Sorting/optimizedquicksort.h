//
// Created by kavya on 5/4/2018.
//

#ifndef MENU_OPTIMIZEDQUICKSORT_H
#define MENU_OPTIMIZEDQUICKSORT_H

#include <algorithm>
#include <iostream>
#include "GenerateInput.h"

using namespace std;

class optimizedquicksort {
public:
    void static calcOptimizedQuickSort(float arr[], int l, int r, int k);
    static void insertionSort(float arr[], int low, int n);
    static int Partition (float a[], int low, int high);
    static void QuickSort(float a[], int low, int high);
    static void write_output_file(float arr[], int n);
    static double OptimizedQuickSort(float arr[], int low, int high, int NUM);
};


#endif //MENU_OPTIMIZEDQUICKSORT_H
