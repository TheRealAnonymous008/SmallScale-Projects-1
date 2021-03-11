#include<iostream>
#include<thread>
#include<random>
#include<mutex>
#include<future>
#include<chrono>
#include<vector>

#define SIZE 100000000

std::vector<int> generateList(){
    std::vector<int> List;
    for(unsigned long long int i = 0; i < SIZE; i++){
        List.push_back(rand() % SIZE + 1);
    }
    return List;
}

void printList(std::vector<int> List){
    for(auto it = List.begin(); it!= List.end(); it++){
        std::cout<<*it<<" ";
    }
    std::cout<<"\n";
}

std::vector<int> mergeUtil(std::vector<int> left, std::vector<int> right){
    int lctr = 0;
    int rctr = 0;
    std::vector<int> mergedList;
    while(lctr < (int) left.size() && rctr < (int) right.size()){
        if(left[lctr] < right[rctr]){
            mergedList.push_back(left[lctr]);
            lctr++;
        }
        else{
            mergedList.push_back(right[rctr]);
            rctr++;
        }
    }

    while(lctr < (int) left.size()){
        mergedList.push_back(left[lctr]);
        lctr++;
    }

    while(rctr < (int) right.size()){
        mergedList.push_back(right[rctr]);
        rctr++;
    }

    return mergedList;
}


void mergeSortList(std::vector<int> &List){
    int n = List.size();
    if(n != 1){
        int mid = n /2;
        std::vector<int> left;
        std::vector<int> right;

        for(int i = 0; i < mid; i++)
            left.push_back(List[i]);
        for(int i = mid; i < n; i++)
            right.push_back(List[i]);

        mergeSortList(left);
        mergeSortList(right);
        List = mergeUtil(left, right);
    }
}

std::vector<int> threadedMergeUtil(std::vector<int> left, std::vector<int> right){
    int lctr = 0;
    int rctr = 0;
    std::vector<int> mergedList;
    while(lctr < (int) left.size() && rctr < (int) right.size()){
        if(left[lctr] < right[rctr]){
            mergedList.push_back(left[lctr]);
            lctr++;
        }
        else{
            mergedList.push_back(right[rctr]);
            rctr++;
        }
    }

    while(lctr < (int) left.size()){
        mergedList.push_back(left[lctr]);
        lctr++;
    }

    while(rctr < (int) right.size()){
        mergedList.push_back(right[rctr]);
        rctr++;
    }

    return mergedList;
}


std::vector<int> threadedMergeSort(std::vector<int> &List, int depth ){
    int n = List.size();
    if(n != 1){
        int mid = n /2;
        std::vector<int> left;
        std::vector<int> right;

        for(int i = 0; i < mid; i++)
            left.push_back(List[i]);
        for(int i = mid; i < n; i++)
            right.push_back(List[i]);

        if(depth <= 3){
            std::future<std::vector<int>> ftl = std::async(threadedMergeSort, std::ref(left), depth + 1);
            std::future<std::vector<int>> ftr = std::async(threadedMergeSort, std::ref(right), depth + 1);
            List = mergeUtil(ftl.get(), ftr.get());
        }
        else{
            mergeSortList(left);
            mergeSortList(right);
            List = mergeUtil(left, right);
        }
    }

    return List;
}




int main(){

    std::vector<int> List;
    List = generateList();

    int val = 0;

    switch(val){
        case 0:     threadedMergeSort(List, 0);    break;
        case 1:     mergeSortList(List);        break;

    }

    return 0;
}
