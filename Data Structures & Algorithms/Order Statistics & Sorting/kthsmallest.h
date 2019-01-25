//
// Created by kavya on 5/3/2018.
//

#ifndef MENU_KTHSMALLEST_H
#define MENU_KTHSMALLEST_H
#define INT_MAX1 65535.0
#include <string>
#include <iostream>
#include <fstream>
#include "GenerateInput.h"

class kthSmallest
{
public:
    float static calcKthSmallest(float arr[], int l, int r, int k);
    static int partition(float arr[], int l, int r);
    static void swap(float *a, float *b);
    static void write_output_file(float smallest);
    static double KthSmallest(float arr[], int l, int r, int k);
};

#endif //MENU_KTHSMALLEST_H