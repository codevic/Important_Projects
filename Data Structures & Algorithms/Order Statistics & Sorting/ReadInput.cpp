//
// Created by kavya on 5/3/2018.
//

#include "ReadInput.h"

void ReadInput::read_from_input(int choice_of_file, int choice_of_distribution, float array[], int n, int k, string timestamp) {

    int i = 0;
    ifstream inFile;
    string line, num;

    string path = GenerateInput::GetCurrentWorkingDir();
    path +="\\input\\";
    string file = "";

    if(choice_of_distribution == 1 and choice_of_file == 1){
        file = path+"File1_Uniform_"+timestamp+".txt";
    }
    else if(choice_of_distribution == 2 and choice_of_file == 1){
        file = path+"File1_Normal_"+timestamp+".txt";
    }
    else if(choice_of_distribution == 1 and choice_of_file == 2){
        file = path+"File2_Uniform_"+timestamp+".txt";
    }
    else if(choice_of_distribution == 2 and choice_of_file == 2){
        file = path+"File2_Normal_"+timestamp+".txt";
    }
    cout <<"\nReading from file :" << file;
    // for input including k, n and array:
    inFile.open(file);

    if (!inFile) {
        cout << "Unable to open file";
        exit(1); // terminate with error
    }

    if(choice_of_file == 1){
        while( getline(inFile, line) )
        {
            if(i == 0)
                num = line;
            break;
        }
        std::istringstream buf(num);
        std::istream_iterator<std::string> beg(buf), end;
        std::vector<std::string> tokens(beg, end);
        n = stoi(tokens[0]);
        k = stoi(tokens[1]);
    }
    else{
        while( getline(inFile, line) )
        {
            if(i == 0)
                n = stoi(line);
            break;
        }
    }
    i = 1;
    while( getline(inFile, line) ) {
        array[i-1] = stof(line);
        i += 1;
    }
    cout << "\n Read from file" << file;
    cout << "\nk:"<<k<<"\n";
    cout << "\nn:"<<n<<"\n";
    for(int i = 0; i<n;i++)
        cout << "\t"<<array[i];
}


