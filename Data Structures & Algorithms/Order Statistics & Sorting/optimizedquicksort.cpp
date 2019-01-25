//
// Created by kavya on 5/4/2018.
//

#include "optimizedquicksort.h"

// Number of elements to be sorted
#define N 1000000

// perform insertion sort on arr[]
void optimizedquicksort::insertionSort(float arr[], int low, int n)
{
    // Start from second element (element at index 0
    // is already sorted)
    for (int i = low + 1; i <= n; i++)
    {
        int value = arr[i];
        int j = i;

        // Find the index j within the sorted subset arr[0..i-1]
        // where element arr[i] belongs
        while (j > low && arr[j - 1] > value)
        {
            arr[j] = arr[j - 1];
            j--;
        }
        // Note that subarray arr[j..i-1] is shifted to
        // the right by one position i.e. arr[j+1..i]

        arr[j] = value;
    }
}

int optimizedquicksort::Partition (float a[], int low, int high)
{
    // Pick rightmost element as pivot from the array
    int pivot = a[high];

    // elements less than pivot will be pushed to the left of pIndex
    // elements more than pivot will be pushed to the right of pIndex
    // equal elements can go either way
    int pIndex = low;

    // each time we finds an element less than or equal to pivot, pIndex
    // is incremented and that element would be placed before the pivot.
    for (int i = low; i < high; i++)
    {
        if (a[i] <= pivot)
        {
            swap(a[i], a[pIndex]);
            pIndex++;
        }
    }
    // swap pIndex with Pivot
    swap (a[pIndex], a[high]);

    // return pIndex (index of pivot element)
    return pIndex;
}

void optimizedquicksort::QuickSort(float a[], int low, int high)
{
    // base condition
    if(low >= high)
        return;

    // rearrange the elements across pivot
    int pivot = Partition(a, low, high);

    // recurse on sub-array containing elements that are less than pivot
    QuickSort(a, low, pivot - 1);

    // recurse on sub-array containing elements that are more than pivot
    QuickSort(a, pivot + 1, high);
}

double optimizedquicksort::OptimizedQuickSort(float arr[], int low, int high, int NUM){
    int n = high+1;
    auto start = get_time::now();
    optimizedquicksort::calcOptimizedQuickSort(arr, low, high, NUM);
    auto end = get_time::now();
    auto diff = end - start;
    double time = chrono::duration_cast<chrono::nanoseconds>(diff).count();
    float runtime = time/1000000;
    cout<<"\nElapsed time is :  "<< runtime <<" ms "<<endl;
    GenerateInput::write_runtime_to_file(n, runtime, "hybrid_quiksort");
    optimizedquicksort::write_output_file(arr, n);
    return runtime;
}

void optimizedquicksort::calcOptimizedQuickSort(float arr[], int low, int high, int NUM)
{

    while (low < high)
    {
        // do insertion sort if 10 or smaller
        if(high - low < NUM)
        {
            insertionSort(arr, low, high);
            break;
        }
        else
        {
            int pivot = Partition(arr, low, high);

            // tail call optimizations - recurse on smaller sub-array
            if (pivot - low < high - pivot) {
                calcOptimizedQuickSort(arr, low, pivot-1, NUM);
                low = pivot + 1;
            } else {
                calcOptimizedQuickSort(arr, pivot+1, high, NUM);
                high = pivot - 1;
            }
        }
    }
}

void optimizedquicksort::write_output_file(float arr[], int n){
    ofstream file2;
    string timestamp = GenerateInput::get_date();
    string path = GenerateInput::GetCurrentWorkingDir();
    path +="\\output\\";
    file2.open(path+"hybrid_quiksort_"+timestamp+".txt");
    cout <<"\n";
    for (int i = 0; i < n; i++) {
        file2 << arr[i] << "\n";
        cout <<"\t" <<arr[i];
    }
    cout << "\nOutput was written to file!!\n";
    file2.close();
}