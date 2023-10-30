#include <cmath>

extern "C" int xy_foo() {
    return static_cast<int>(std::floor(42.42));
}
