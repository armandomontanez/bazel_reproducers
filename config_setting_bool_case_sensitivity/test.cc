#include <gtest/gtest.h>

#ifndef CONFIG_IS_SET
#define CONFIG_IS_SET 0
#endif  // CONFIG_IS_SET

constexpr int kVal = CONFIG_IS_SET;

TEST(TestDefine, IsSet) {
  EXPECT_EQ(kVal, 1);
}
