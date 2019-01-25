//
// Created by kavya on 4/29/2018.
//
#include "GenerateInput.h"

using namespace std;

string GenerateInput::GetCurrentWorkingDir() {
    char buff[FILENAME_MAX];
    GetCurrentDir( buff, FILENAME_MAX );
    string current_working_dir(buff);
    return current_working_dir;
}

string GenerateInput::generate_file1_uniform(int n, int k, string path, string timestamp){
    ofstream file1;
    string filename = path+"File1_Uniform_"+timestamp+".txt";
    file1.open(filename); // Opening a File or creating if not present
    file1 << n <<" "<< k; // Writing data to file

    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine e(seed);
    std::uniform_real_distribution<float> distr(0,1000);
    float num;
    for (int i=0; i<n; i++) {
        num = distr(e);
        file1 << "\n" <<  ceil(num * pow(10, 2)) / pow(10, 2);//ceil(num) ;
    }
    cout << "\nUniform Data has been written to file1 with n, k and n elements,";
    cout << "\n to file : "<< filename;
    file1.close();
    cout<<"\nGenerate_input: timestamp"<<timestamp;
    return timestamp;
}

string GenerateInput::generate_file2_uniform(int n, string path, string timestamp) {
    ofstream file2;  // Create Object of Ofstream
    string filename = path+"File2_Uniform_"+timestamp+".txt";
    file2.open(filename); // Opening a File or creating if not present
    file2 << n; // Writing data to file

    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine e(seed);
    std::uniform_real_distribution<float> distr(0, 1000);  // range: [0,5]  -- both 1 and 5 are included // default param: [0, INT_MAX]
    float num;
    for (int i = 0; i < n; i++) {
        num = distr(e);
        file2 << "\n" <<  ceil(num * pow(10, 2)) / pow(10, 2);
    }
    cout << "\nUniform Data has been written to file2 with n and n elements,";
    cout << "\n to file : "<< filename;
    file2.close();
    return timestamp;
}

string GenerateInput::generate_file1_normal(int n, int k, string path, string timestamp){

    ofstream file1;  // Create Object of Ofstream
    string filename = path+"File1_Normal_"+timestamp+".txt";
    file1.open(filename); // Opening a File or creating if not present
    file1 << n <<" "<< k; // Writing data to file

    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine e(seed);
    std::normal_distribution<float> distrN(10.0, 3.0);  // mean and standard deviation
    float num;
    for (int i=0; i<n; i++) {
        num = distrN(e);
        file1 << "\n" <<  ceil(num * pow(10, 2)) / pow(10, 2);
    }
    cout << "\nNormal Data has been written to file with n, k and n elements,";
    cout << "\n to file : "<< filename;
    file1.close();
    return timestamp;
}

string GenerateInput::generate_file2_normal(int n, string path, string timestamp) {
    ofstream file2;  // Create Object of Ofstream
    string filename = path+"File2_Normal_"+timestamp+".txt";
    file2.open(filename); // Opening a File or creating if not present
    file2 << n; // Writing data to file

    unsigned seed = std::chrono::system_clock::now().time_since_epoch().count();
    std::default_random_engine e(seed);
    std::normal_distribution<float> distrN(10.0, 3.0);  // mean and standard deviation
    float num;
    for (int i=0; i<n; i++) {
        num = distrN(e);
        file2 << "\n" <<  ceil(num * pow(10, 2)) / pow(10, 2);
    }
    cout << "\nNormal Data has been written to file2 with n and n elements,";
    cout << "\n to file : "<< filename;
    file2.close();
    return timestamp;
}

string GenerateInput::get_date(void)
{
    time_t now;
    char the_date[20];
    the_date[0] = '\0';
    now = time(NULL);
    if (now != -1)
        strftime(the_date, 20, "%d_%m_%Y_%H_%M_%S", gmtime(&now));
    return std::string(the_date);
}

string GenerateInput::generate_input(int n, int k, int choice_of_file, int choice_of_distribution){
    /* 	n -> number of elements in the array
     * choice_of_file = 1 -> input file with k
     * choice_of_file = 2 -> input file without k
     * choice_of_distribution = 1 -> uniform distribution
     * choice_of_distribution = 2 -> normal distribution
     */
    string path = GetCurrentWorkingDir();
    path +="\\input\\";
    string timestamp = get_date();
    if((choice_of_file == 1 or choice_of_file == 2) and (choice_of_distribution == 1 or choice_of_distribution == 2))
    {
        switch(choice_of_file) {
            case 1:
                if (choice_of_distribution == 1)
                    timestamp = generate_file1_uniform(n, k, path, timestamp);
                else
                    timestamp = generate_file1_normal(n, k, path, timestamp);
                break;
            case 2:
                if (choice_of_distribution == 1)
                    timestamp = generate_file2_uniform(n, path, timestamp);
                else
                    timestamp = generate_file2_normal(n, path, timestamp);
                break;
        }
    }
    else
        cout<<"Invalid input! choice_of_file and choice_of_distribution must be either 1 or 2 !";
    return timestamp;
}

void GenerateInput::write_runtime_to_file(int n, float runtime, string filename)
{
    ofstream file1;
    string path = GetCurrentWorkingDir();
    path +="\\runtime\\";
    file1.open(path+filename+"_runtime.txt",ios::app);
    file1 << n <<","<< runtime <<"\n"; // Writing data to file
    cout<<"\nRuntime along with n has been written to the file";
}
