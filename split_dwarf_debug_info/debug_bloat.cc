// Deliberately header-free so the only paths that can leak into the build
// outputs come from how the compiler is invoked, not from system headers.
//
// Every Layer<T, N> is a distinct type with its own members and out-of-line
// member functions, so -g emits a structure type, template parameters,
// subprograms, lexical blocks, and locals for each of the
// kTagCount * kDepth instantiations.

namespace debug_bloat {

constexpr int kTagCount = 24;
constexpr int kDepth = 300;

template <int I>
struct Tag {};

template <typename A, typename B>
struct Pair {};

template <int I>
using TagType = Pair<Tag<I>, Pair<Tag<I * 3>, Tag<I * 7>>>;

template <typename T, int N>
struct Layer {
  // Nested types cost nothing in .text, but each one is described in full by
  // the debug info of every instantiation.
  enum class Phase {
    kUninitialized,
    kFilling,
    kFilled,
    kAccumulating,
    kAccumulated,
    kPoisoned,
  };

  struct Metadata {
    Phase phase;
    int generation;
    int depth;
    unsigned flags;
    long created_at;
    long updated_at;
    long checksum;
    double load_factor;
    double decay;
    const char* owner;
    const char* reason;
    Layer* self;
  };

  Layer<T, N - 1> inner;
  long values[N % 11 + 1];
  double weights[N % 7 + 1];
  const char* label;
  Metadata metadata;

  void Fill(long seed) {
    for (long& value : values) {
      value = seed++;
    }
    for (double& weight : weights) {
      weight = static_cast<double>(seed) * 0.5;
    }
    label = "layer";
    metadata.phase = Phase::kFilled;
    metadata.self = this;
    inner.Fill(seed);
  }

  long Accumulate(long seed) const {
    long total = seed;
    for (long value : values) {
      total = total * 31 + value;
    }
    for (double weight : weights) {
      total += static_cast<long>(weight * N);
    }
    return inner.Accumulate(total) ^ N;
  }
};

template <typename T>
struct Layer<T, 0> {
  void Fill(long) {}
  long Accumulate(long seed) const { return seed; }
};

template <int I>
Layer<TagType<I>, kDepth> layers;

template <int I>
long RunAll(long seed) {
  layers<I>.Fill(seed);
  long result = layers<I>.Accumulate(seed);
  if constexpr (I > 0) {
    result += RunAll<I - 1>(seed);
  }
  return result;
}

}  // namespace debug_bloat

extern "C" long debug_bloat_entry(long seed) {
  return debug_bloat::RunAll<debug_bloat::kTagCount - 1>(seed);
}
