#include <iostream>

class CppBase {
public:
    void cpp_method() {
        std::cout << "This is a method from CppBase class." << std::endl;
    }
};

class CppDerived : public CppBase {
public:
    void cpp_method() {
        std::cout << "This is a method from CppDerived class." << std::endl;
    }
};

class CppMixin {
public:
    void cpp_mixin_method() {
        std::cout << "This is a method from CppMixin class." << std::endl;
    }
};
