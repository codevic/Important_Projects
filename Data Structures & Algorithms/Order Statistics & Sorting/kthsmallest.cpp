#include "kthsmallest.h"

// This function returns k'th smallest element in arr[l..r] using
// QuickSort based method.  ASSUMPTION: ALL ELEMENTS IN ARR[] ARE DISTINCT

double kthSmallest::KthSmallest(float *arr, int l, int r, int k){
    int n = r+1;
    auto start = get_time::now();
    float smallest = kthSmallest::calcKthSmallest(arr, l, r, k);
    auto end = get_time::now();
    auto diff = end - start;
    double time = chrono::duration_cast<chrono::nanoseconds>(diff).count();
    float runtime = time/1000000;
    cout<<"\nElapsed time is :  "<< runtime <<" ms "<<endl;
    GenerateInput::write_runtime_to_file(n, runtime, "kth_smallest");
    kthSmallest::write_output_file(smallest);
    return runtime;
}

void kthSmallest::write_output_file(float smallest){
    ofstream file2;
    string timestamp = GenerateInput::get_date();
    string path = GenerateInput::GetCurrentWorkingDir();
    path +="\\output\\";
    file2.open(path+"kth_smallest_"+timestamp+".txt");
    cout <<"\n";
    file2 << smallest << "\n";
    cout <<"\t kth smallest :" <<smallest;
    cout << "\nOutput was written to file!!\n";
    file2.close();
}

float kthSmallest::calcKthSmallest(float arr[], int l, int r, int k)
{
    // If k is smaller than number of elements in array
    if (k > 0 && k <= r - l + 1)
    {
        // Partition the array around last element and get
        // position of pivot element in sorted array
        int pos = partition(arr, l, r);

        // If position is same as k
        if (pos-l == k-1)
            return arr[pos];
        if (pos-l > k-1)  // If position is more, recur for left subarray
            return kthSmallest::calcKthSmallest(arr, l, pos-1, k);

        // Else recur for right subarray
        return kthSmallest::calcKthSmallest(arr, pos+1, r, k-pos+l-1);
    }

    // If k is more than number of elements in array
    return INT_MAX1;
}

void kthSmallest::swap(float *a, float *b)
{
    float temp = *a;
    *a = *b;
    *b = temp;
}

// Standard partition process of QuickSort().  It considers the last
// element as pivot and moves all smaller element to left of it
// and greater elements to right
int kthSmallest::partition(float *arr, int l, int r)
{
    int x = arr[r], i = l;
    for (int j = l; j <= r - 1; j++)
    {
        if (arr[j] <= x)
        {
            swap(&arr[i], &arr[j]);
            i++;
        }
    }
    swap(&arr[i], &arr[r]);
    return i;
}