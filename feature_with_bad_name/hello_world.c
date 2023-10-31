#include <stdio.h>

#include "xy_foo.h"

#ifndef SOMETHING
#error "This should be defined"
#endif  // SOMETHING

#ifndef ANOTHER
#error "This should be defined"
#endif  // ANOTHER

#ifndef LAST_ONE
#warning "This should be defined"
#endif  // LAST_ONE

int main() {
    printf("Hello, world!\n");
    printf("The answer is %d\n", xy_foo());
    return 0;
}