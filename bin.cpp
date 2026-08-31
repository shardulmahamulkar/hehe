#include <iostream> 
#include <vector>   
using namespace std;
vector<int> generateRandomNumbers(int size) {
    vector<int> nums(size);
    for (int i = 0; i < size; ++i) {
        nums[i] = rand() % 100; // Generate random numbers between 0 and 99
    }
    return nums;
}
int main () {
    vector<int> nums = generateRandomNumbers(10);
    sort(nums.begin(), nums.end()); // Sort the numbers for binary search
    int low = 0;
    int high = nums.size() - 1;
    int mid = low + (high - low) / 2;
    int target = rand() % 100; // Random target number between 0 and 99
    cout << target << endl;
    for (int num : nums) {
        cout << num << " ";
    }
    cout << endl;
    while(low <= high){
        if (nums[mid]== target){return mid;}
        else if (nums[mid]< target ){
            low = mid +1;
        }
        else {
            high = mid - 1;
        }
        mid = low + (high - low) / 2;
    }
    return -1; // Target not found
}


int ll (){
    struct Node {
        int data;
        Node* next;
    };
    data-> data = 10;
    data-> next = nullptr;
    
}