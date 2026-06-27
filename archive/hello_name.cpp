#include <iostream>
#include <string>

// Simple program that asks for the user's name and prints a greeting.
// Build (Windows, using g++ in cmd):
//   g++ -std=c++17 -O2 -Wall hello_name.cpp -o hello_name
// Run:
//   hello_name
int main() {
    std::cout << "Enter your name: " << std::flush; // flush prompt immediately
    std::string name;
    if (!std::getline(std::cin, name)) {
        std::cerr << "Failed to read name.\n";
        return 1;
    }
    if (name.empty()) {
        std::cout << "Hello, mysterious stranger!" << std::endl;
    } else {
        std::cout << "Hello, " << name << "!" << std::endl;
    }
    return 0;
}
