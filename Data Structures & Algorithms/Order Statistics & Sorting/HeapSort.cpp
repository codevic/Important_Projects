//
// Created by kavya on 5/3/2018.
//

#include "HeapSort.h"

// To heapify a subtree rooted with node i which is
// an index in arr[]. n is size of heap
void HeapSort::heapify(float arr[], int n, int i)
{
    int largest = i;  // Initialize largest as root
    int l = 2 * i + 1;  // left = 2*i + 1
    int r = 2 * i + 2;  // right = 2*i + 2

    // If left child is larger than root
    if (l < n && arr[l] > arr[largest])
        largest = l;

    // If right child is larger than largest so far
    if (r < n && arr[r] > arr[largest])
        largest = r;

    // If largest is not root
    if (largest != i)
    {
        swap(arr[i], arr[largest]);

        // Recursively heapify the affected sub-tree
        heapify(arr, n, largest);
    }
}

// Build heap (rearrange array)
void HeapSort::buildHeap(float arr[], int n)
{
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);
}

// main function to do heap sort
double HeapSort::heapSort(float arr[], int n)
{
    auto start = get_time::now();
    // Build heap (rearrange array)
    buildHeap(arr, n);

    // One by one extract an element from heap
    for (int i = n - 1; i >= 0; i--)
    {
        // Move current root to end
        swap(arr[0], arr[i]);

        // call max heapify on the reduced heap
        heapify(arr, i, 0);
    }
    auto end = get_time::now();
    auto diff = end - start;
    double time = chrono::duration_cast<chrono::nanoseconds>(diff).count();
    float runtime = time/1000000 ;
    cout<<"\nElapsed time is :  "<< runtime <<" ms "<<endl;
    GenerateInput::write_runtime_to_file(n, runtime, "heap_sort");
    printArray(arr,n);
    return runtime;
}

/* A utility function to print array of size n */
void HeapSort::printArray(float arr[], int n)
{
    cout << "\n";
    ofstream file2;
    string timestamp = GenerateInput::get_date();
    string path = GenerateInput::GetCurrentWorkingDir();
    path +="\\output\\";
    file2.open(path+"heap_sort_"+timestamp+".txt");

    for (int i = 0; i < n; i++) {
        file2 << arr[i] << "\n";
        cout << arr[i] << " ";
    }
    cout << "\nOutput was written to file successfully!!\n";
    file2.close();
}