//
// Created by Sanjana on 24-04-2018.
//

#include "MedianofthreeQuickSort.h"
#include "RandomizedQuickSort.h"

void MedianofthreeQuickSort::print_Array_median(float arr[], int size)
{
    ofstream file2;
    string timestamp = GenerateInput::get_date();
    string path = GenerateInput::GetCurrentWorkingDir();
    path +="\\output\\";
    file2.open(path+"quicksort_median_"+timestamp+".txt");
    for (int i = 0; i < size; i++) {
        file2 << arr[i] << "\n";
        cout << arr[i]<<"\t";
    }
    cout << "\nOutput was written to file!!\n";
    file2.close();
}

float MedianofthreeQuickSort::calc_median (float arr[], int n)
{
    srand (time(NULL)); //initialize the random seed
    int a , b, c;
    float first,second,third;
    a = rand() % n;
    b = rand() % n;
    while(a==b){
       b = rand() % n;
    }
    c = rand() % n;
    while(c==a or c==b){
       c = rand() % n;
    }
    first = arr[a];
    second = arr[b];
    third = arr[c];
    float median;
    if (first > second)
    {
        if (first > third)
        {
            if (second > third)
                median = second;
            else
                median = third;
        }
        else
            median = first;
    }
    else
    {
        if (second > third)
        {
            if (third > first)
                median = first;
            else
                median = third;
        }
        else
            median = second;
    }
    return median;
}


int MedianofthreeQuickSort::partition_median(float *arr, int low, int high) {
    float pivot = calc_median(arr, high+1); // pivot
    int i = (low - 1); // Index of smaller element
    for (int j = low; j <= high - 1; j++) {
        // If current element is smaller than or equal to pivot
        if (arr[j] <= pivot) {
            i++;
            RandomizedQuickSort::swap(&arr[i], &arr[j]);
        }
    }
    RandomizedQuickSort::swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

void MedianofthreeQuickSort::quickSort_median(float *arr, int low, int high) {
    if (low < high) {
        int pi = MedianofthreeQuickSort::partition_median(arr, low, high);
        quickSort_median(arr, low, pi - 1);
        quickSort_median(arr, pi + 1, high);
    }
}

double MedianofthreeQuickSort::quickSortmedian(float *arr, int low, int high){
    int n = high + 1;
    auto start = get_time::now();
    MedianofthreeQuickSort::quickSort_median(arr, low, high);
    auto end = get_time::now();
    auto diff = end - start;
    double time = chrono::duration_cast<chrono::nanoseconds>(diff).count();
    printf("\nSorted array: \n");
    print_Array_median(arr,n);
    cout<<"Elapsed time is :  "<< time/1000000 <<" ms "<<endl;
    float runtime= time/1000000;
    GenerateInput::write_runtime_to_file(n, runtime, "quicksort_median");
    return runtime;
}
