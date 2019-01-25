//
// Created by kavya on 5/3/2018.
//

#ifndef MENU_HEAPSORT_H
#define MENU_HEAPSORT_H
#include <stdio.h>
#include <chrono>
#include <iostream>
#include <algorithm>
#include "GenerateInput.h"

using namespace std;
using get_time = chrono::steady_clock ;

class HeapSort {
public:
    static void heapify(float arr[], int n, int i);

    static void buildHeap(float arr[], int n);

    static double heapSort(float arr[], int n);

    static void printArray(float arr[], int n);
};


#endif //MENU_HEAPSORT_H
