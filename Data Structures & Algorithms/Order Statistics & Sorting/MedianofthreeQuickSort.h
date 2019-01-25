//
// Created by Sanjana on 24-04-2018.
//

#ifndef UNTITLED_MEDIANOFTHREEQUICKSORT_H
#define UNTITLED_MEDIANOFTHREEQUICKSORT_H
#include <stdlib.h>
#include <time.h>
#include <stdio.h>
#include <cstdlib>
#include <iostream>
#include <ctime>
#include <fstream>
#include <chrono>
#include "GenerateInput.h"
using namespace std;
using get_time = chrono::steady_clock ;
using namespace std;

class MedianofthreeQuickSort {
public:
    static float calc_median(float arr[], int n);
    static void print_Array_median(float arr[], int size);
    static int partition_median(float arr[], int low, int high);
    static void quickSort_median(float arr[], int low, int high);
    static double quickSortmedian(float *arr, int low, int high);
};


#endif //UNTITLED_MEDIANOFTHREEQUICKSORT_H
