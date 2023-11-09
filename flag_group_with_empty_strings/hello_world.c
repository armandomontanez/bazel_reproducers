#include <stdio.h>

#include "xy_foo.h"

#ifndef SOMETHING
#error `SOMETHING` is not defined!
#endif  // SOMETHING

int main() {
    printf("Hello, world!\n");
    printf("The answer is %d\n", xy_foo());
    return 0;
}